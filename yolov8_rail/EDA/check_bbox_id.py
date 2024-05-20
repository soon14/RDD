import os
import json
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

def draw_text(image, position, text, color, font_size, thickness):
    # Pillow Image로 변환
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_image)
    font_path = r'C:\Users\user\Downloads\Noto_Sans_KR\NotoSansKR-VariableFont_wght.ttf'  # 실제 폰트 파일 경로로 변경하세요.
    font = ImageFont.truetype(font_path, font_size)
    
    # 텍스트 두께를 시뮬레이션하기 위해 여러 번 그리기
    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            if dx != 0 or dy != 0:
                draw.text((position[0] + dx, position[1] + dy), text, font=font, fill=color)
    draw.text(position, text, font=font, fill=color)
    
    # OpenCV 이미지로 변환
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

def get_polygon_center(points):
    x_coords = [point[0][0] for point in points]
    y_coords = [point[0][1] for point in points]
    center_x = int(sum(x_coords) / len(points))
    center_y = int(sum(y_coords) / len(points))
    return center_x, center_y

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
        
def draw_bbox_and_polygon_on_image(json_file, image_path, output_directory, bbox_color=(0, 255, 0), polygon_color=(0, 0, 255), thickness=20, font_path=r'C:\Users\user\Downloads\Noto_Sans_KR\NotoSansKR-VariableFont_wght.ttf'):
    # JSON 파일 열기
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # 이미지 파일 불러오기 (OpenCV)
    image = cv2.imread(image_path)
    
    # OpenCV 이미지에서 Pillow 이미지로 변환
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(image_pil)
    
    # 폰트 설정
    font_size = 20
    font = ImageFont.truetype(font_path, font_size)
    
    # bbox와 polygon 정보 추출하여 그리기
    for annotation in data["annotations"]:
        bbox = annotation.get("bbox")
        polygon = annotation.get("polygon")

        # category_id를 사용하여 name_kor 찾기
        category_id = annotation["category_id"]
        name_kor = None
        for category in data["categories"]:
            if category["id"] == category_id:
                name_kor = category["name_kor"]

        # 글씨 크기와 두께 설정
        font_size = 60  # 기존 크기에서 3배로 키움
        thickness = 3

        # 예제 코드
        if bbox:
            x, y, w, h = bbox
            cv2.rectangle(image, (x, y), (x + w, y + h), bbox_color, thickness)
            # Pillow로 텍스트 그리기 (바운딩박스 오른쪽)
            text_position = (x + w + 10, y)
            image = draw_text(image, text_position, name_kor, (255, 255, 255, 255), font_size, thickness)
            if annotation["status"] == "normal":
                image = draw_text(image, (x + w + 10, y + font_size + 10), "정상", (0, 255, 0), font_size, thickness)
            else:
                image = draw_text(image, (x + w + 10, y + font_size + 10), annotation["status_detail"], (0, 0, 255), font_size, thickness)
        elif polygon:
            points = np.array(polygon, np.int32).reshape((-1, 1, 2))
            cv2.polylines(image, [points], isClosed=True, color=polygon_color, thickness=thickness)
            
            # 폴리곤의 가운데 위치 계산
            center_x, center_y = get_polygon_center(points)
            
            # 텍스트 위치 설정
            text_position_name_kor = (center_x, center_y)
            text_position_status = (center_x, center_y + font_size + 10)
            
            # 텍스트 그리기
            image = draw_text(image, text_position_name_kor, name_kor, (255, 255, 255, 255), font_size, thickness)
            if annotation["status"] == "normal":
                image = draw_text(image, text_position_status, "정상", (0, 255, 0), font_size, thickness)
            else:
                image = draw_text(image, text_position_status, annotation["status_detail"], (0, 0, 255), font_size, thickness)
    # 결과 이미지 저장
    output_image_path = os.path.join(output_directory, os.path.basename(image_path))
    cv2.imwrite(output_image_path, image)

# JSON 파일 경로
json_file = r"E:\225.철도 선로 상태 인식 데이터\01-1.정식개방데이터\Validation\Labeling\VL_도시철도_이상\도시철도_13차 수집 (221110)_탄방역_5132940.json"
# 이미지 파일 경로
image_path = r"C:\Users\user\yolov8_rail\yolov8_rail\5132940.jpg"
# 결과 이미지를 저장할 디렉토리 경로
output_directory = r"C:\Users\user\yolov8_rail\yolov8_rail"


# bbox가 그려진 이미지 생성
draw_bbox_and_polygon_on_image(json_file, image_path, output_directory)