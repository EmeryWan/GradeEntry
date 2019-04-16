import os

import cv2

path = os.path.join(os.getcwd(), "..", "config", "ecjtu_logo.jpg")
# img = QFileDialog.getOpenFileName(self, 'logo', str(path), 'Image files (ecjtu_logo.png)')
img = cv2.imread(path, flags=1)
cv2.imshow('img', img)
cv2.waitKey(0)