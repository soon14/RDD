import os
import json
import cv2
import numpy as np


def draw_bbox_on_image(json_file, image_dir, output_dir):
    # JSON 파일 열기
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # 이미지 파일 경로 추출
        image_name = os.path.splitext(os.path.basename(json_file))[0] + ".jpg"
        image_path = os.path.join(image_dir, image_name)
        # 이미지 불러오기
        image = cv2.imread(image_path)
        # bbox 정보 추출 및 그리기
        for annotation in data["annotations"]:
            bbox = annotation["bbox"]
            # 바운딩 박스 좌표 추출
            x, y, w, h = bbox
            # 바운딩 박스 그리기
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # 결과 이미지 저장
        output_image_path = os.path.join(output_dir, image_name)
        cv2.imwrite(output_image_path, image)

def draw_bbox_and_polygon_on_image(json_file, image_dir,output_directory,bbox_color=(0, 255, 0), polygon_color=(0, 0, 255), thickness=2):
    # JSON 파일 열기
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # 이미지 파일 경로 추출
        image_name = os.path.splitext(os.path.basename(json_file))[0] + ".jpg"
        image_path = os.path.join(image_dir, image_name)
        # 이미지 파일 불러오기
        image = cv2.imread(image_path)
        
        # bbox와 polygon 정보 추출하여 그리기
        for annotation in data["annotations"]:
            bbox = annotation["bbox"]
            polygon = annotation["polygon"]
            if bbox:
                x, y, w, h = bbox
                print(x,y,w,h)
                print(image.shape)
                cv2.rectangle(image, (x, y), (x + w, y + h), bbox_color, thickness)
                cv2.putText(image, str(annotation["id"]), (x, y+h+5), cv2.FONT_HERSHEY_SIMPLEX, 5, bbox_color, 2)
    # 이어서 bbox를 사용하는 코드 작성
            else:
                points = np.array(polygon, np.int32).reshape((-1, 1, 2))
                cv2.polylines(image, [points], isClosed=True, color=polygon_color, thickness=thickness)
                cv2.putText(image, str(annotation["id"]), (x,y+h+5), cv2.FONT_HERSHEY_SIMPLEX, 5, bbox_color, 2)
        # 결과 이미지 저장
        output_image_path = os.path.join(output_directory, image_name)
        cv2.imwrite(output_image_path, image)


# JSON 파일 경로
json_file = r"E:\rail\data\Training\LabelingData\AbnormalRe\d1010724.json"
# 이미지 파일이 있는 디렉토리 경로
image_directory = r"E:\rail\data\Training\RealData\AbnormalRe"
# 결과 이미지를 저장할 디렉토리 경로
output_directory = r"E:\rail\data\Training\RealData\CheckBbox"

# bbox가 그려진 이미지 생성
draw_bbox_and_polygon_on_image(json_file, image_directory, output_directory)
#draw_bbox_on_image(json_file, image_directory, output_directory)