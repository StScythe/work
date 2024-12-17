from bs4 import BeautifulSoup #Библиотека для парсинга HTML
import requests #Библиотека для выполнения HTTP-запросов
import schedule #Библиотека для планирования задач
import time #Библиотека для работы со временем
import pandas as pd  #Библиотека для работы с табличными данными (DataFrame)
import logging
#import csv  #Библиотека для работы с CSV-файлами

def request_verification(response, URL): #функция для проверки запроса
    if response.status_code != 200: #Если статус-код не 200
        print(f"Ошибка при загрузке страницы {URL}. Код ответа: {response.status_code}") #Вывод сообщения об ошибке

def data_collection(): #Функция сбора данных
    URL = 'https://books.toscrape.com/'
    page = requests.get(URL)
    request_verification(page, URL)
    soup = BeautifulSoup(page.text, "html.parser")
    out_books = []
    i=1
    while i<51:
        i+=1
        books = soup.find_all('article', class_='product_pod')
        for bookSe in books:
            bookURL = URL + bookSe.find('a').get('href') #Формируем URL книги
            print(bookURL) #вывод адреса книги в консоль для наглядного отслеживания происходящего
            response = requests.get(bookURL)
            request_verification(response, bookURL)
            book = BeautifulSoup(response.text, "html.parser")

            name = book.find('h1').text #Название книги
            price_color = book.find('p', class_='price_color').text #Цена
            star_rating = book.find('p', class_='star-rating').get('class')[1] #Рейтинг книги
            instock_availability = book.find('p', class_='instock availability').text.strip() #Остаток
            product_description = book.find('meta', attrs={'name': 'description'})['content'].strip() #Получаем описание книги    
            product_information = {}
            for row in book.find('table', class_='table table-striped').find_all('tr'): #Добавляем цикл по всем строкам таблицы с дополнительной информацией
                        header = row.find('th').text.strip() #Получаем заголовок строки
                        value = row.find('td').text.strip() #Получаем значение строки
                        product_information[header] = value #Добавляем в словарь
            #Создаем словарь с искомыми данными
            out_books.append({'title' : name, 'price_color' : price_color, 'star_rating' : star_rating, 'instock_availability' : instock_availability, 'product_description' : product_description, **product_information})
        
        #Получаем URL следующей страницы каталога
        next = soup.find('li', class_='next')
        try:
            if next.find('a').get('href') == 'catalogue/page-2.html':
                bookURL = URL + next.find('a').get('href')
                page = requests.get(bookURL)
                request_verification(page, bookURL)
                URL = URL + 'catalogue/'
            else:
                bookURL = URL + next.find('a').get('href')
        except AttributeError:
                print("Последняя страница") #AttributeError: 'NoneType' object has no attribute 'find'
        page = requests.get(bookURL)
        request_verification(page, bookURL)
        soup = BeautifulSoup(page.text, "html.parser")
    
    df = pd.DataFrame(out_books) #Создание датафрейма
    #Начальная предобработка. Излишняя для данного кода.
    df = df.dropna() #Удаление строк с пропусками
    df.drop_duplicates(inplace=True) #Удаление дубликатов

    all_books = df.shape[0] #Общее количество книг в собранных данных
    print(f'Общее количество книг:{all_books}') #Вывод общего количества книг в собранных данных
    statistics = df.describe() #Основные статистики по числовым данным
    print(f"Статистика:\n{statistics}") #Вывод основных статистик по числовым данным 

    df.to_csv('books_data.csv', index=False) #Сохранение полученных данных в CSV файл

#Бесконечный цикл с запуском в данное время
schedule.every().day.at("21:06").do(data_collection)
#schedule.every(30).minutes.do(data_collection) 

while True:
    schedule.run_pending() 
    time.sleep(1)
    