import os
import shutil

# YOLO 레이블 파일에서 x, y, w, h 값 중 하나라도 1.0을 넘으면 파일 삭제
def delete_files_above_threshold(txt_directory, jpg_directory):
    for txt_filename in os.listdir(txt_directory):
        if txt_filename.endswith(".txt"):
            txt_file_path = os.path.join(txt_directory, txt_filename)
            with open(txt_file_path, 'r') as txt_file:
                lines = txt_file.readlines()
                # 레이블 파일 내용을 줄 단위로 확인하여 x, y, w, h 값이 1.0을 초과하는지 확인
            for line in lines:
                    values = line.strip().split()
                    if len(values) == 5:  # 클래스 인덱스와 x, y, w, h 값이 있는 경우
                        x, y, w, h = map(float, values[1:])  # 첫 번째 값은 클래스 인덱스이므로 무시
                        if x > 1.0 or y > 1.0 or w > 1.0 or h > 1.0:
                            os.remove(txt_file_path)  # txt 파일 삭제
                            jpg_filename = os.path.splitext(txt_filename)[0] + '.jpg'
                            jpg_file_path = os.path.join(jpg_directory, jpg_filename)
                            if os.path.exists(jpg_file_path):
                                os.remove(jpg_file_path)  # 다른 경로의 동일한 이름의 jpg 파일 삭제
                            break  # 하나라도 1.0을 넘는 값이 있으면 삭제 후 다음 파일로 넘어감

# 특정 경로 설정
txt_directory_path = r"E:\datasets\validation\labels"
jpg_directory_path = r"E:\datasets\validation\images"

# 함수 호출
delete_files_above_threshold(txt_directory_path, jpg_directory_path)
