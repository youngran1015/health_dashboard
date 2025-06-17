import pandas as pd

def check_data_structure():
    """데이터 파일들의 구조를 확인하는 함수"""
    
    files_to_check = [
        'data/socioeconomic/소득_2020_2024.csv',
        'data/health_accessibility/hospitals_2020_2024.csv',
        'data/health_region/activity_2020_2024_kr.csv'
    ]
    
    for file_path in files_to_check:
        try:
            print(f"\n=== {file_path} ===")
            df = pd.read_csv(file_path)
            print("컬럼명:", list(df.columns))
            print("첫 5행:")
            print(df.head())
            print("데이터 형태:", df.shape)
        except Exception as e:
            print(f"오류: {e}")

if __name__ == "__main__":
    check_data_structure()