import json
import os

def update_items_recursively(items, target_value):
    if isinstance(items, list):
        for item in items:
            update_items_recursively(item, target_value)
    elif isinstance(items, dict):
        if 'menuLevel' in items: # menuLevel이 있는 경우에만 isTestTarget 업데이트
            items['isTestTarget'] = target_value
        if 'children' in items and isinstance(items['children'], list):
            update_items_recursively(items['children'], target_value)

def update_test_target(file_prefix):
    # 스크립트 파일의 현재 디렉토리를 기준으로 input_dir 경로 설정
    script_dir = os.path.dirname(__file__)
    input_dir = os.path.join(script_dir, '../01_inputs')
    found_file = False
    for filename in os.listdir(input_dir):
        if filename.startswith(file_prefix) and filename.endswith('.json'):
            filepath = os.path.join(input_dir, filename)
            found_file = True
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                if 'menus' in data:
                    update_items_recursively(data['menus'], True)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                print(f"'{filename}' 파일의 모든 menuLevel 항목에 대해 isTestTarget을 true로 업데이트했습니다.")
                break
            except Exception as e:
                print(f"'{filename}' 파일 처리 중 오류 발생: {e}")
    
    if not found_file:
        print(f"'{file_prefix}'로 시작하는 JSON 파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    prefix = input("파일명을 시작하는 세 자리 숫자를 입력하세요 (예: 016): ")
    if len(prefix) == 3 and prefix.isdigit():
        update_test_target(prefix)
    else:
        print("잘못된 입력입니다. 세 자리 숫자를 입력해야 합니다.") 