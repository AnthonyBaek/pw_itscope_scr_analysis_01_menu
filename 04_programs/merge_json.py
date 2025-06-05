import json
import os

# --- 파일 경로 설정 ---
# 입력 JSON 파일들이 있는 폴더 경로
INPUT_FOLDER_PATH = "01_inputs"
# 병합된 JSON 파일을 저장할 경로와 파일명
OUTPUT_FILE_PATH = os.path.join(INPUT_FOLDER_PATH, "menu_all.json")
# --------------------

def merge_json_files():
    """
    INPUT_FOLDER_PATH 내의 JSON 파일들을 병합 규칙에 따라 병합하여
    OUTPUT_FILE_PATH에 저장합니다.
    """
    # 입력 폴더 내의 JSON 파일 목록을 숫자 접두사 기준으로 정렬
    # 001_ 부터 038_ 로 시작하는 파일들을 대상으로 합니다.
    file_prefixes = tuple(f"{i:03d}" for i in range(1, 39))
    
    try:
        all_files_in_input_folder = os.listdir(INPUT_FOLDER_PATH)
    except FileNotFoundError:
        print(f"오류: 입력 폴더 '{INPUT_FOLDER_PATH}'를 찾을 수 없습니다.")
        return

    file_paths = sorted([
        os.path.join(INPUT_FOLDER_PATH, f)
        for f in all_files_in_input_folder
        if f.endswith(".json") and f.startswith(file_prefixes)
    ])

    if not file_paths:
        print(f"'{INPUT_FOLDER_PATH}' 폴더에 병합할 JSON 파일이 없습니다. (001 ~ 038 접두사 확인)")
        return

    json_data_list = []
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data_list.append(json.load(f))
        except FileNotFoundError:
            # 이 경우는 위 file_paths 리스트 생성 로직 상 발생하기 어려우나 방어적으로 처리
            print(f"파일을 찾을 수 없습니다: {file_path}")
            json_data_list.append({"menus": []})
        except json.JSONDecodeError:
            print(f"JSON 디코딩 오류: {file_path}")
            json_data_list.append({"menus": []})
        except Exception as e:
            print(f"파일 읽기 중 오류 발생 ({file_path}): {e}")
            json_data_list.append({"menus": []})


    if not json_data_list:
        print("병합할 JSON 데이터가 없습니다.")
        return

    merged_data = {}
    # 1. `target` 정보는 첫 번째 JSON 파일의 것을 사용합니다.
    if json_data_list[0] and "target" in json_data_list[0]:
        merged_data['target'] = json_data_list[0]['target']
    else:
        merged_data['target'] = {} # 기본값 또는 오류 처리

    merged_data['menus'] = []

    def find_menu(menu_list, menu_name, menu_level):
        for menu_item in menu_list:
            if menu_item.get('menuName') == menu_name and menu_item.get('menuLevel') == menu_level:
                return menu_item
        return None

    def merge_menus_recursive(target_menus, source_menus):
        for source_menu in source_menus:
            # menuName 또는 menuLevel이 없는 경우 건너<0xE3><0x8A><0x99>
            if source_menu.get('menuName') is None or source_menu.get('menuLevel') is None:
                print(f"경고: menuName 또는 menuLevel이 없는 항목 발견, 건너<0xE3><0x8A><0x99>니다: {source_menu}")
                continue

            existing_menu = find_menu(target_menus, source_menu['menuName'], source_menu['menuLevel'])
            if existing_menu:
                # 같은 menuLevel, menuName을 가진 노드가 있으면 children을 재귀적으로 병합
                if 'children' in source_menu and source_menu['children']:
                    if 'children' not in existing_menu or not existing_menu['children']:
                        existing_menu['children'] = []
                    merge_menus_recursive(existing_menu['children'], source_menu['children'])
                
                # isLeaf, isActive, isTestTarget, url, path, includedScreens 등 다른 속성 업데이트
                # source_menu의 값으로 existing_menu를 덮어쓰거나, 필요에 따라 다른 병합 로직 적용
                for key, value in source_menu.items():
                    if key not in ['menuName', 'menuLevel', 'children']: # 이미 처리된 키 제외
                        existing_menu[key] = value
            else:
                # 없으면 새로 추가
                target_menus.append(source_menu)

    for data in json_data_list:
        if data and "menus" in data and isinstance(data["menus"], list): # menus 키가 있고 리스트 타입인지 확인
            merge_menus_recursive(merged_data['menus'], data['menus'])
        else:
            print(f"경고: 'menus' 키가 없거나 리스트 형태가 아니어서 건너<0xE3><0x8A><0x99>니다: {data}")
            
    try:
        with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=4)
        print(f"JSON 파일들을 성공적으로 병합하여 '{OUTPUT_FILE_PATH}' 에 저장했습니다.")
    except IOError:
        print(f"오류: '{OUTPUT_FILE_PATH}' 파일에 쓸 수 없습니다.")
    except Exception as e:
        print(f"파일 저장 중 오류 발생: {e}")

if __name__ == '__main__':
    merge_json_files() 