import os.path

import cv2

#########  ##########
Dir = r"D:\Anaconda3\envs\deeplearning\Lib\site-packages\flappy_bird_gym\assets\sprites"
Img_name = "background-night.png"
Height = 288
Width = 512
#########  ##########

path = os.path.join(Dir, Img_name)
img_array = cv2.resize(cv2.imread(path, cv2.IMREAD_COLOR), (Height, Width))
cv2.imwrite(path, img_array)
