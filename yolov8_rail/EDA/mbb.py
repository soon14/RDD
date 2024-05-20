import json
import os
from PIL import Image
def create_min_bbox(polygon, image_size):
    x_min = min(polygon[::2])
    y_min = min(polygon[1::2])
    x_max = max(polygon[::2])
    y_max = max(polygon[1::2])
    
    width = x_max - x_min
    height = y_max - y_min

    # 이미지 사이즈와 비교하여 bbox 좌표를 조정
    if x_min < 0:
        x_min = 0
    if y_min < 0:
        y_min = 0
    if x_max > image_size[0]:
        x_max = image_size[0]
    if y_max > image_size[1]:
        y_max = image_size[1]

    width = x_max - x_min
    height = y_max - y_min
    x = (x_min + x_max) / 2
    y = (y_min + y_max) / 2

    return [x, y, width, height]

def adjust_bbox(bbox, image_size): 
    x, y, w, h = bbox
    x_min = x
    y_min = y
    x_max = x + w
    y_max = y + h
    # 이미지 사이즈와 비교하여 bbox 좌표를 조정
    if x_min < 0:
        x_min = 0
    if y_min < 0:
        y_min = 0
    if x_max > image_size[0]:
        x_max = image_size[0]
    if y_max > image_size[1]:
        y_max = image_size[1]

    width = x_max - x_min
    height = y_max - y_min
    x = (x_min + x_max) / 2
    y = (y_min + y_max) / 2

    return [x, y, width, height]
    
def process_annotations(json_data, image_size):
    for annotation in json_data["annotations"]:
        if "bbox" in annotation and annotation["bbox"]:
            x, y, w, h = annotation["bbox"]
            annotation["bbox"] = adjust_bbox([x, y, w, h], image_size)
        if "polygon" in annotation and annotation["polygon"]:
            bbox = create_min_bbox(annotation["polygon"], image_size)
            annotation["bbox"] = bbox
            del annotation["polygon"]
    return json_data

def process_json_file(input_file, image_dir, output_dir):
    with open(input_file, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        # 이미지 파일과 크기 가져오기
        image_name = os.path.splitext(os.path.basename(input_file))[0] + ".jpg"
        image_path = os.path.join(image_dir, image_name)
        image = Image.open(image_path)
        image_size = image.size

        # bbox 조정
        processed_data = process_annotations(json_data, image_size)
    
    output_file = os.path.join(output_dir, os.path.basename(input_file))
    with open(output_file, 'w', encoding='utf-8') as out_file:
        json.dump(processed_data, out_file, indent=4, ensure_ascii=False)

def process_all_json_files(input_directory, image_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for filename in os.listdir(input_directory):
        if filename.endswith(".json"):
            input_file = os.path.join(input_directory, filename)
            process_json_file(input_file, image_directory, output_directory)

input_directory_path = r"E:\rail\data\Validation\LabelingData\NormalRe"
image_directory_path = r"E:\rail\data\Validation\RealData\NormalRe"
output_directory_path = r"E:\rail\data\Validation\LabelingData\NormalMbb"

process_all_json_files(input_directory_path, image_directory_path, output_directory_path)
