import os

# 검사할 디렉토리 경로 설정
directory_path = r'E:\urban_datasets\validation\labels'

# 디렉토리 내 모든 파일을 순회
for filename in os.listdir(directory_path):
    # 파일 확장자가 .txt인 경우에만 처리
    if filename.endswith(".txt"):
        # 파일 전체 경로 생성
        file_path = os.path.join(directory_path, filename)
        # 파일 열기
        with open(file_path, 'r') as file:
            # 파일 내 각 줄을 순회
            for line in file:
                # 공백으로 구분된 데이터 분리
                data = line.strip().split()
                # 첫 번째 데이터(클래스 번호)가 문자열 '4'인지 확인
                if data[0] == '4':
                    # 조건을 만족하는 파일 이름 출력
                    print(filename)
                    # 한 파일 내 여러 라인에 클래스 4가 있을 수 있으나, 파일 이름은 한 번만 출력하려면
                    # 해당 파일에서 더 이상의 검사를 중지
                    break
