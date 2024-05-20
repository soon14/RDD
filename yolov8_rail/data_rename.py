import os
import json
import shutil

def rename_and_move_json_files(source_directory, destination_directory):
    # 만약 대상 디렉터리가 없다면 생성
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    
    # 소스 디렉터리 내의 모든 파일 목록을 가져옴
    files = os.listdir(source_directory)
    
    # 각 파일에 대해 처리
    for filename in files:
        try:
            # 파일명이 .json으로 끝나는 경우에만 처리
            if filename.endswith(".json"):
                source_file_path = os.path.join(source_directory, filename)
                # JSON 파일 열기 (UTF-8 인코딩 사용)
                with open(source_file_path, 'r', encoding='utf-8') as file:
                    # JSON 데이터 로드
                    data = json.load(file)
                    
                    # "image" 키가 있는지 확인하고, 그 안에 요소가 있는지 확인
                    if 'image' in data and data['image']:
                        # "file_name" 값을 가져와서 처리
                        file_name = data['image'][0]['file_name']
                        # 파일명에서 확장자 제외하고 마지막부터 7번째 숫자를 선택
                        new_number = file_name.split('.')[0][-7:]
                        
                        # "file_name" 값을 변경하여 새로운 파일명 생성
                        data['image'][0]['file_name'] = "d" + new_number + ".jpg"
                        
                        new_file_name = "d" + new_number 
                        # 새로운 폴더에 JSON 파일 저장
                        destination_file_path = os.path.join(destination_directory, new_file_name + ".json") 
                        with open(destination_file_path, 'w', encoding='utf-8') as new_file:
                            json.dump(data, new_file, indent=4, ensure_ascii=False)
                        
                        # 기존 파일명과 변경된 파일명 출력
                        print(f"Renaming 'file_name' in '{filename}' to '{new_file_name}' and moving to {destination_directory}")
        except Exception as e:
            print(f"An error occurred while processing '{filename}': {e}")

def rename_and_move_jpg_files(source_directory, destination_directory):
    # 만약 대상 디렉터리가 없다면 생성
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    
    # 소스 디렉터리 내의 모든 파일 목록을 가져옴
    files = os.listdir(source_directory)
    
    # 각 파일에 대해 처리
    for filename in files:
        try:
            # 파일명이 .jpg로 끝나는 경우에만 처리
            if filename.endswith(".jpg"):
                source_file_path = os.path.join(source_directory, filename)
                
                # 파일명에서 확장자 제외하고 마지막부터 7번째 글자까지 선택
                new_number = os.path.splitext(filename)[0][-7:]
                
                # 새로운 파일명 생성
                new_file_name = "d" + new_number + ".jpg"
                
                # 새로운 폴더에 jpg 파일 이동
                destination_file_path = os.path.join(destination_directory, new_file_name)
                shutil.copy(source_file_path, destination_file_path)
                
                # 기존 파일명과 변경된 파일명 출력
                print(f"Renaming '{filename}' to '{new_file_name}' and moving to {destination_directory}")
        except Exception as e:
            print(f"An error occurred while processing '{filename}': {e}")



# 파일이 포함된 소스 디렉터리 경로
source_directory_path = r"E:\rail\data\Training\RealData\Normal"
# 새로운 폴더에 저장할 대상 디렉터리 경로
destination_directory_path = r"E:\rail\data\Training\RealData\NormalRe"

# 함수 호출
#rename_and_move_json_files(source_directory_path, destination_directory_path)
rename_and_move_jpg_files(source_directory_path, destination_directory_path)