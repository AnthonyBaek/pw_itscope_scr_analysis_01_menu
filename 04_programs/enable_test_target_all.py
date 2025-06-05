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

def update_all_test_target():
    # 스크립트 파일의 현재 디렉토리를 기준으로 input_dir 경로 설정
    script_dir = os.path.dirname(__file__)
    # menu_all.json 파일 경로 직접 지정
    filepath = os.path.join(script_dir, '../01_inputs/menu_json_all/menu_all.json')
    
    if not os.path.exists(filepath):
        print(f"'{filepath}' 파일을 찾을 수 없습니다.")
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if 'menus' in data:
            update_items_recursively(data['menus'], True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"'{os.path.basename(filepath)}' 파일의 모든 menuLevel 항목에 대해 isTestTarget을 true로 업데이트했습니다.")
    except Exception as e:
        print(f"'{os.path.basename(filepath)}' 파일 처리 중 오류 발생: {e}")

if __name__ == "__main__":
    update_all_test_target() 