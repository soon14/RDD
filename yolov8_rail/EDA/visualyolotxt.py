import cv2
import os

# 클래스 이름 설정
classes = ["normal", "unknownAbnormal", "damage", "wearCutoff", "screwLoose", "overLubricatedBreak"]

# 이미지와 텍스트 파일이 있는 디렉토리 설정
directory_path = r'E:\urban_datasets\validation\ValVisual'

# 디렉토리 내의 모든 파일을 순회
for filename in os.listdir(directory_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):  # 이미지 파일인 경우
        # 이미지 파일 경로
        image_path = os.path.join(directory_path, filename)
        # 해당 이미지에 대응하는 txt 파일 경로
        txt_path = image_path.rsplit('.', 1)[0] + '.txt'
        
        # 이미지 읽기
        image = cv2.imread(image_path)
        h, w, _ = image.shape  # 이미지의 높이와 너비 추출
        
        # 바운딩 박스 정보가 있는 txt 파일 열기
        with open(txt_path, 'r') as file:
            for line in file:
                class_id, x_center, y_center, bbox_width, bbox_height = map(float, line.split())
                class_id = int(class_id)
                
                # YOLO 포맷을 픽셀 좌표로 변환
                x_center, y_center, bbox_width, bbox_height = x_center * w, y_center * h, bbox_width * w, bbox_height * h
                x_min, y_min = int(x_center - bbox_width / 2), int(y_center - bbox_height / 2)
                
                # 바운딩 박스와 클래스 이름 그리기
                cv2.rectangle(image, (x_min, y_min), (int(x_min + bbox_width), int(y_min + bbox_height)), (0, 0, 255), 2)
                cv2.putText(image, classes[class_id], (x_min, y_min +15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        # 결과 이미지 저장
        # 원본 파일명에 "_annotated" 접미사를 붙여 저장 경로를 생성
        save_path = image_path.rsplit('.', 1)[0] + '_annotated.' + image_path.rsplit('.', 1)[1]
        cv2.imwrite(save_path, image)
