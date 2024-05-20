import os
import shutil

def find_non_matching_files(path1, path2):
    files1 = set(os.path.splitext(filename)[0] for filename in os.listdir(path1))
    files2 = set(os.path.splitext(filename)[0] for filename in os.listdir(path2))


    #unique_to_path1 = files1.intersection(files2)
    unique_to_path2 = files2 - files1

    return len(unique_to_path2) #unique_to_path2

def find_matching_files_and_copy(path1, path2, output_directory):
    
    if not os.path.exists(output_directory):
            os.makedirs(output_directory)
    
    # path2의 파일 목록을 가져와서 파일 이름만 추출하여 집합으로 만듭니다.
    jpg_files = set(os.path.splitext(filename)[0] for filename in os.listdir(path1))

    # path1의 파일 목록을 가져와서 JSON 파일 중 jpg_files와 이름이 겹치는 파일을 찾습니다.
    for filename in os.listdir(path2):
        
        filename_without_extension = os.path.splitext(filename)[0]
       
        if filename_without_extension in jpg_files:
            
            source_file = os.path.join(path2, filename)
            destination_file = os.path.join(output_directory, filename)
            shutil.copy(source_file, destination_file)
            print(f"File '{filename}' copied to '{output_directory}'")




# 비교할 두 경로 지정
path1 = r"E:\rail\data\Training\LabelingData\NormalRe" #labeling data
path2 = r"E:\rail\data\Training\RealData\NormalRe" #real data
output_directory = r"E:\rail\data\Training\RealData\Normal7212"

# 확장자를 제외하고 파일 이름이 같은 파일을 새로운 경로에 저장
find_matching_files_and_copy(path1, path2, output_directory)
# 결과 출력
print("첫 번째 경로에 있는 파일의 개수:", len(os.listdir(path1)))
print("두 번째 경로에 있는 파일의 개수:", len(os.listdir(path2)))

print("\n겹치는것:", find_non_matching_files(path1, path2))


#print("두 번째 경로에만 있는 파일의 개수:", len(non_matching_files2))
