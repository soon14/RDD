import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import cv2, numpy

# 이미지 파일 열기
img = Image.open('./dataset/neu-det/train/traindataset/images/rolled-in_scale_151.jpg')

# img = Image.open('./dataset/neu-det/val/images/crazing_97.jpg')
# img = Image.open('./dataset/neu-det/train/origin_images/crazing_97.jpg')

# bounding box 정보 (YOLO 형식: 중심 x, 중심 y,
bbox = [0.69 ,0.6075 ,0.29 ,0.755]
# bbox = [47,102,152,188]
width, height = img.size

# bounding box 정보를 실제 좌표로 변경
x_center, y_center, w, h = bbox
x = (x_center - w/2) * width
y = (y_center - h/2) *height

# 원본 xyxy 바운딩 박스 표기시
# x = x_center 
# y = y_center 

# 이미지에 bounding box 그리기
fig, ax = plt.subplots(1)
ax.imshow(img)

rect = patches.Rectangle((x, y), w*width, h*height, linewidth=2, edgecolor='r', facecolor='none')

# 원본 xyxy 바운딩 박스 표기시
# rect = patches.Rectangle((x, y), w-x_center, h-y_center, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)

plt.show()