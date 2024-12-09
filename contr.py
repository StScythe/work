import cv2
import numpy as np

# Загрузка изображения
img = cv2.imread('test.jpg')
img_gray = cv2.imread('test.jpg', cv2.IMREAD_GRAYSCALE)
cv2.imshow("Оригинальное серое", img_gray)
cv2.waitKey(0)

#Малоконтрастное изображение
ImagelowContrast = img_gray/2
ImagelowContrast = ImagelowContrast.astype('uint8')
cv2.imshow("Малоконтрастное изображение", ImagelowContrast)
cv2.waitKey(0)

#линейная коррекция изображения

# Вычисление минимума и максимума изображения
r_min = np.min(ImagelowContrast)
r_max = np.max(ImagelowContrast)
print(r_min)
print(r_max)
img_corrected = (ImagelowContrast - r_min) * 255.0 / (r_max - r_min)
img_corrected = np.uint8(img_corrected)
cv2.imshow("линейная коррекция изображения", img_corrected)
cv2.waitKey(0)

# Результат обработки методом equalizeHist
img_equalize = cv2.equalizeHist(ImagelowContrast)
cv2.imshow("Результат обработки методом equalizeHist", img_equalize)
cv2.waitKey(0)

#Результат обработки методом clahe
clahe = cv2.createCLAHE(clipLimit = 10, tileGridSize=(8, 8))
img_clahe = clahe.apply(ImagelowContrast)
cv2.imshow("Результат обработки методом Clahe", img_clahe)
cv2.waitKey(0)

cv2.destroyAllWindows()