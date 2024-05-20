import os
import json
from collections import defaultdict

def count_name_kor_in_json_files(directory_path):
    name_kor_count = defaultdict(int)

    # 디렉토리 내 모든 파일을 순회
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                
                # JSON 파일 열기
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # categories 안의 name_kor 개수 세기
                    if 'categories' in data:
                        for category in data['categories']:
                            if 'name_kor' in category:
                                name_kor_count[category['name_kor']] += 1

    return dict(name_kor_count)



def count_status_detail_condition(directory_path):
    """
    This function counts the occurrences of status_detail and name_kor in all JSON files within the given folder path,
    with the condition that if status_detail is missing, it checks whether the status is not 'abnormal' before counting.

    :param directory_path: The folder path where the JSON files are stored.
    :return: A dictionary that maps (status_detail, name_kor) pairs to their respective counts.
    """
    category_details = defaultdict(lambda: defaultdict(int))

    # Iterate through all files in the folder
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                    # Convert the categories list to a dictionary for faster access by id
                    categories_dict = {category['id']: category['name_kor'] for category in data.get('categories', [])}

                    # Iterate through the annotations and collect status_detail counts for 'abnormal' status
                    for annotation in data.get('annotations', []):
                        if annotation.get('status', '') == 'abnormal':
                            status_detail = annotation.get('status_detail', 'abnormal')
                            category_id = annotation['category_id']
                            name_kor = categories_dict.get(category_id, 'Unknown Category')

                            # Increment the count of the specific status_detail for the category
                            category_details[name_kor][status_detail] += 1

    # Print the results
    for name_kor, details in category_details.items():
        print(f"Category Name Kor: {name_kor}")
        for status_detail, count in details.items():
            print(f"  - Status Detail: {status_detail}, Count: {count}")
            print("\n")


# 함수 사용 예시
directory_path = r'E:\225.철도 선로 상태 인식 데이터\01-1.정식개방데이터\Validation\Labeling\VL_도시철도_이상'
count_status_detail_condition(directory_path)


'''# 사용 예시
directory_path = r'E:\225.철도 선로 상태 인식 데이터\01-1.정식개방데이터\Validation\Labeling\VL_도시철도_정상'
result = count_name_kor_in_json_files(directory_path)
print(result)'''
