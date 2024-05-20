import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import cv2, numpy
import glob, os
from datetime import datetime

# 이미지 파일 열기
img_ori_path = r"E:\datasets\train\images\\"
label_ori_path = r"E:\datasets\train\labels\\"
save_path = r"E:\datasets\check_bbox"
#current_time = datetime.now().strftime("%Y%m%d-%H%M%S")

img_list = [f for f in os.listdir(img_ori_path) if f.endswith('.jpg')]
#save_path = "E:\rail\data\Training\check_bbox_mbb" # current_time

os.makedirs(save_path, exist_ok=True)

    
for img_path in img_list:
    img = Image.open(img_ori_path + img_path)
    img_name = img_path.split(".")[0]
        
    # bounding box 정보 (YOLO 형식: 중심 x, 중심 y,
    with open(f'{label_ori_path}{img_name}.txt', 'r') as f:
        bboxs = [line.strip().split()[1:] for line in f]
        # bbox = bbox[1:]
    # bbox = [0.69 ,0.6075 ,0.29 ,0.755]
    # bbox = [47,102,152,188]
    width, height = img.size

    fig, ax = plt.subplots(1)
    ax.imshow(img)
    # bounding box 정보를 실제 좌표로 변경
    for bbox in bboxs:
        x_center, y_center, w, h = bbox
        x_center, y_center, w, h = float(x_center), float(y_center), float(w), float(h)
        x = ((x_center) - w/2) * width
        y = (y_center - h/2) * height
        print(x_center, y_center, w, h)
        print(x,y,w,h)

    # 원본 xyxy 바운딩 박스 표기시
        # x = x_center 
        # y = y_center 

    # 이미지에 bounding box 그리기

        rect = patches.Rectangle((x, y), w*width, h*height, linewidth=2, edgecolor='r', facecolor='none')
        
    # 원본 xyxy 바운딩 박스 표기시
    # rect = patches.Rectangle((x, y), w-x_center, h-y_center, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

    plt.savefig(f"{save_path}/{img_name}.jpg")
    plt.close(fig)