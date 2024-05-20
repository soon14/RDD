import json
import os
from PIL import Image

def resize_and_normalize_bbox(x, y, w, h, image_width, image_height, resize=[640,640]):
    # 좌표와 크기를 리사이즈된 이미지에 맞게 조정
    normalized_x = round((x / resize[0]) * (resize[0]/image_width), 8) 
    normalized_y = round((y / resize[1]) * (resize[1]/image_height), 8)
    normalized_w = round((w / resize[0]) * (resize[0]/image_width), 8)
    normalized_h = round((h / resize[1]) * (resize[1]/image_height), 8)

    # 정규화된 좌표와 크기 반환
    return normalized_x, normalized_y, normalized_w, normalized_h

def convert_to_yolo(image_dir, json_file_path, output_folder, resize=[640, 640]):
    # JSON 파일 열기
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    # 출력 파일 경로 설정
    output_txt_path = os.path.splitext(os.path.basename(json_file_path))[0] + ".txt"
    output_txt_path = os.path.join(output_folder, output_txt_path)

    # 이미지 파일 경로 추출
    image_name = os.path.splitext(os.path.basename(json_file_path))[0] + ".jpg"
    image_path = os.path.join(image_dir, image_name)

    # 이미지 불러오기
    image = Image.open(image_path)
    image_width, image_height = image.size

    # 출력 폴더 생성
    os.makedirs(output_folder, exist_ok=True)

    # YOLO 형식으로 변환하여 출력 파일에 쓰기
    with open(output_txt_path, 'w') as output_file:
        for annotation in data["annotations"]:
            # status를 기반으로 label 설정
            if annotation["status"] == "normal":
                label = 0
            elif annotation["status"] == "abnormal":
                if annotation["status_detail"] == "훼손":
                    label = 2
                elif annotation["status_detail"] == "마모, 절손":
                    label = 3
                elif annotation["status_detail"] == "너트 풀림":
                    label = 4
                elif annotation["status_detail"] == "과다도유,파손":
                    label = 5
                else:
                    label = 1

            # bbox 값 설정
            bbox = annotation["bbox"]

            # 리사이즈 및 정규화된 bbox 값 계산
            x, y, w, h = bbox
            center_x, center_y, normalized_width, normalized_height = resize_and_normalize_bbox(
                x, y, w, h, image_width, image_height, resize=[640, 640])

            # YOLO 형식으로 변환하여 파일에 쓰기
            output_line = f"{label} {center_x} {center_y} {normalized_width} {normalized_height}\n"
            output_file.write(output_line)


def batch_convert_to_yolo(json_folder, output_folder, image_dir):
    # JSON 파일 목록 가져오기
    json_files = [f for f in os.listdir(json_folder) if f.endswith('.json')]

    # 모든 JSON 파일을 YOLO 형식으로 변환
    for json_file in json_files:
        json_file_path = os.path.join(json_folder, json_file)
        convert_to_yolo(image_dir, json_file_path, output_folder, resize=[640, 640])

json_folder_path = r"E:\rail\data\Validation\LabelingData\NormalMbb"
output_folder_path = r"E:\rail\data\Validation\LabelingData\NormalYolo"
image_directory_path = r"E:\rail\data\Validation\RealData\NormalRe"

batch_convert_to_yolo(json_folder_path, output_folder_path, image_directory_path)
