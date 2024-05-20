import os
from PIL import Image
import json
import glob
from threading import Thread
import time
from multiprocessing import Pool, cpu_count
import multiprocessing
import shutil
from functools import partial

# 데이터 이름 변경
def rename_files(source_directory):
    files = os.listdir(source_directory)
    cnt_json = 0
    cnt_jpg = 0
    for filename in files:
        
        new_number = filename.split('.')[0][-7:]
                            
        new_file_name = "d" + new_number 
        if filename.endswith(".json"):
            source_file_path = os.path.join(source_directory, filename)
            with open(source_file_path, 'r', encoding='utf-8') as file:
                # JSON 데이터 로드
                data = json.load(file)
                
                destination_file_path = os.path.join(source_directory, new_file_name + ".json") 
                if not os.path.exists(destination_file_path):
                    with open(destination_file_path, 'w', encoding='utf-8') as new_file:
                        json.dump(data, new_file, indent=4, ensure_ascii=False)
                else:
                    pass
            cnt_json += 1
            os.remove(source_file_path)
           
            
        elif filename.endswith(".jpg"):
            source_file_path = os.path.join(source_directory, filename)
                
            # 새로운 폴더에 jpg 파일 이동
            destination_file_path = os.path.join(source_directory, new_file_name + ".jpg")
            if not os.path.exists(destination_file_path):
                shutil.copy(source_file_path, destination_file_path)
            else: 
                pass
            cnt_jpg += 1
            os.remove(source_file_path)
    print(f"Renamed {cnt_json} json files and {cnt_jpg} jpg files in {source_directory}")

# polygon to bbox
def polygon_to_mbbox(json_folder, image_folder):
    # LabelingData 폴더 내의 모든 파일을 순회
    
    for root, dirs, files in os.walk(json_folder):
        for file in files:
            if file.endswith(".json"):
                json_file_path = os.path.join(root, file)
                with open(json_file_path, 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                
                
                image_path = os.path.join(image_folder, os.path.splitext(file)[0] + ".jpg")
                image = Image.open(image_path)
                image_size = image.size

                for annotation in data["annotations"]:
                    if "bbox" in annotation and annotation["bbox"]:
                        x, y, w, h = annotation["bbox"]
                        x_min = max(0, x)
                        y_min = max(0, y)
                        x_max = min(image_size[0], x + w)
                        y_max = min(image_size[1], y + h)
                        width = x_max - x_min
                        height = y_max - y_min
                        x_center = (x_min + x_max) / 2
                        y_center = (y_min + y_max) / 2
                        annotation["bbox"] = [x_center, y_center, width, height]
                    if "polygon" in annotation and annotation["polygon"]:
                        polygon = annotation["polygon"]
                        x_min = min(polygon[::2])
                        y_min = min(polygon[1::2])
                        x_max = max(polygon[::2])
                        y_max = max(polygon[1::2])
                        width = x_max - x_min
                        height = y_max - y_min
                        x_center = (x_min + x_max) / 2
                        y_center = (y_min + y_max) / 2
                        annotation["bbox"] = [x_center, y_center, width, height]
                        del annotation["polygon"]
                
                # 처리된 bbox 반영
                with open(json_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(data, json_file, indent=4, ensure_ascii=False)
                with open(json_file_path, 'r', encoding='utf-8') as json_file:
                    updated_data = json.load(json_file)
                    for annotation in updated_data["annotations"]:
                        if "poly" in annotation:
                            print(f"not updated: {json_file_path}")
    print(f"Processed all json files in {json_folder}")

    
# convert to yolo
def convert_to_yolo(json_folder, image_folder, output_folder):
   
    
    # 출력 폴더가 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # JSON 파일 목록 가져오기
    json_files = [f for f in os.listdir(json_folder) if f.endswith('.json')]
   # print(json_files)

    # 각 JSON 파일에 대해 YOLO 형식으로 변환
    for json_file in json_files:
        try:
            # JSON 파일 경로 설정
            json_file_path = os.path.join(json_folder, json_file)
            # JSON 파일 열기
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 출력 파일 경로 설정
            output_txt_path = os.path.splitext(os.path.basename(json_file_path))[0] + ".txt"
            output_txt_path = os.path.join(output_folder, output_txt_path)
            #print(output_txt_path)
            # 이미지 파일 경로 설정
            image_path = os.path.join(image_folder, os.path.splitext(json_file)[0] + ".jpg")
            
           # print(image_path)

            # 이미지 불러오기
            image = Image.open(image_path)
            image_width, image_height = image.size

            # 출력 파일 열기
            with open(output_txt_path, 'w') as output_file:
                # 각 annotation에 대해 YOLO 형식으로 변환하여 파일에 쓰기
                for annotation in data["annotations"]:
                    if annotation["status"] == "normal":
                        label = 0
                    elif annotation["status"] == "abnormal":
                        if annotation["status_detail"] == "훼손":
                            label = 1
                        elif annotation["status_detail"] == "마모, 절손":
                            label = 2
                        elif annotation["status_detail"] == "너트 풀림":
                            label = 3
                        elif annotation["status_detail"] == "과다도유,파손":
                            label = 4
                    
                    bbox = annotation["bbox"]
                    x, y, w, h = bbox
                    # bbox 값을 이미지 크기에 맞게 정규화
                    normalized_x = round((x / image_width), 8) 
                    normalized_y = round((y / image_height), 8)
                    normalized_w = round((w / image_width), 8)
                    normalized_h = round((h / image_height), 8)

                    # YOLO 형식으로 변환하여 파일에 쓰기
                    output_line = f"{label} {normalized_x} {normalized_y} {normalized_w} {normalized_h}\n"
                    output_file.write(output_line)
        
        except Exception as e:
            print(f"An error occurred while processing '{json_file}': {e}")
    print(f"Converted all json files in {json_folder} to YOLO format")

'''# 라벨링 없는 이미지 삭제
def find_non_matching_files(path1, path2):
    files2 = set(os.path.splitext(filename)[0] for filename in os.listdir(path2))

    # path2에만 있는 파일을 찾아서 삭제
    for filename in files2:
        file_path = os.path.join(path2, filename)
        if not os.path.exists(os.path.join(path1, filename)):
            # 파일을 삭제합니다.
            os.remove(file_path)
            print(f"Deleted '{filename}' from {path2}")
    return "Non-matching files deleted."
    '''

# 이미지 resize
def resize640(image_folder):
    new_height = new_width = 640
    for filename in os.listdir(image_folder):
        try:
            img = Image.open(os.path.join(image_folder, filename)).resize((new_width, new_height))
            img.save(os.path.join(image_folder, filename))
        except Exception as e:
            print(f"Error resizing {filename}: {e}")
    print(f"Resized all images in {image_folder}")

                
if __name__ == '__main__': 
    folder = r"E:\AllRail\datasets"
    start_time = time.time()
    with Pool(cpu_count()) as pool:
        for folder_name in os.listdir(folder):
            print(folder_name) # traning, validation
            dfolder = os.path.join(folder, folder_name)
            json_folder = os.path.join(dfolder, 'Label')
            image_folder = os.path.join(dfolder, 'Real')
            output_folder = os.path.join(dfolder, 'Yolo')

            print(dfolder)
            print(json_folder)
            print(image_folder)
            print(output_folder)
            
            
            if folder_name == 'Training':
                pool.starmap(polygon_to_mbbox, [(json_folder, image_folder)])
                pool.starmap(convert_to_yolo, [(json_folder, image_folder, output_folder)])
                pool.map(resize640, [image_folder])
                
            pool.map(rename_files, [json_folder, image_folder])
            pool.starmap(polygon_to_mbbox, [(json_folder, image_folder)])
            pool.starmap(convert_to_yolo, [(json_folder, image_folder, output_folder)])
            pool.map(resize640, [image_folder])
                
            pool.close()
            pool.join()
    end_time = time.time()
    print(f"전처리 소요 시간: {end_time - start_time}초")
    print(f"cpu코어수 : {cpu_count}")
    print("전처리 완료")