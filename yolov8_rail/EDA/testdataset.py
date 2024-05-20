import os
import shutil
from glob import glob

# 경로 설정
val_images_dir = r'E:\urban_datasets\validation\images'
val_labels_dir = r'E:\urban_datasets\validation\labels'
test_images_dir = r'E:\urban_datasets\test\images'
test_labels_dir = r'E:\urban_datasets\test\labels'

# 테스트 데이터셋 폴더가 없으면 생성
if not os.path.exists(test_images_dir):
    os.makedirs(test_images_dir)
if not os.path.exists(test_labels_dir):
    os.makedirs(test_labels_dir)

# 검증 데이터셋의 이미지 파일 목록 가져오기
val_image_files = glob(os.path.join(val_images_dir, '*.jpg'))

# 검증 데이터셋의 절반을 테스트 데이터셋으로 이동
num_to_transfer = len(val_image_files) // 2
for img_path in val_image_files[:num_to_transfer]:
    # 이미지 파일 이동
    shutil.move(img_path, os.path.join(test_images_dir, os.path.basename(img_path)))
    
    # 대응하는 라벨 파일 경로 생성
    label_path = img_path.replace(val_images_dir, val_labels_dir).replace('.jpg', '.txt')
    # 라벨 파일이 존재하면 이동
    if os.path.exists(label_path):
        shutil.move(label_path, os.path.join(test_labels_dir, os.path.basename(label_path)))

print(f'{num_to_transfer}개의 이미지와 라벨 파일이 {val_images_dir}와 {val_labels_dir}에서 {test_images_dir}와 {test_labels_dir}로 이동되었습니다.')
