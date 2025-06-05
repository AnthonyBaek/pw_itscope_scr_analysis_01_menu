import json
import os
import copy
import re

# 스크립트의 현재 디렉토리 경로
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 입력 JSON 파일 경로 (상대 경로)
INPUT_JSON_RELATIVE_PATH = os.path.join('outputs', 'conversion', 'menu_tree_by_ai_0007.json')
# 출력 분해 디렉토리 경로 (상대 경로)
OUTPUT_DECOMPOSITION_RELATIVE_DIR = os.path.join('outputs', 'decomposition')

# 절대 경로 구성
INPUT_JSON_FILE_PATH = os.path.join(SCRIPT_DIR, INPUT_JSON_RELATIVE_PATH)
OUTPUT_DECOMPOSITION_DIR_PATH = os.path.join(SCRIPT_DIR, OUTPUT_DECOMPOSITION_RELATIVE_DIR)

def sanitize_filename(name):
    """파일명에 유효하지 않은 문자를 제거하거나 대체합니다."""
    # " → "를 "_"로 대체
    name = name.replace(" → ", "_")
    # 알파벳, 숫자, 밑줄, 하이픈이 아닌 모든 문자 제거
    name = re.sub(r'[^\w-]', '', name)
    # 여러 개의 밑줄을 하나로 대체
    name = re.sub(r'_+', '_', name)
    # 앞뒤 밑줄 제거
    name = name.strip('_')
    if not name: # 이름이 정제 후 비어있다면
        return "invalid_name" # 유효하지 않은 이름으로 반환
    return name

def decompose_menu_json(input_file_path, output_dir_path):
    """
    메뉴 JSON 파일을 menuLevel 1과 2를 기준으로 분해합니다.

    - 'target' 섹션을 유지합니다.
    - 'menus' 섹션을 menuLevel 1과 2로 분해합니다.
    - 출력 경로: 전역 상수 OUTPUT_DECOMPOSITION_DIR_PATH 사용
    - 출력 파일명: 순차 번호 (가장 큰 번호 + 1) 및 레벨 2 메뉴의 경로 정보
      (예: 001_L1Name_L2Name.json, 경로의 " → "는 "_"로 대체됨).
    """

    # 1. 출력 디렉토리가 존재하지 않으면 생성
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
        print(f"디렉토리 생성됨: {output_dir_path}")

    # 2. 다음 파일 번호 결정
    existing_files = [f for f in os.listdir(output_dir_path)
                      if f.endswith('.json') and f.split('_')[0].isdigit()]
    next_file_num = 1
    if existing_files:
        max_num = 0
        for f_name in existing_files:
            try:
                num = int(f_name.split('_')[0])
                if num > max_num:
                    max_num = num
            except ValueError:
                pass # 파일명 규칙에 맞지 않는 파일은 무시
        next_file_num = max_num + 1

    # 3. 원본 JSON 파일 읽기
    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"오류: 입력 파일을 찾을 수 없습니다. 경로: {input_file_path}")
        return
    except json.JSONDecodeError:
        print(f"오류: {input_file_path}에서 JSON을 디코딩할 수 없습니다.")
        return

    original_target = data.get("target")
    if original_target is None:
        print("경고: 입력 JSON에 'target' 키가 없습니다. 출력 파일에서는 빈 객체가 됩니다.")
        original_target = {}

    menus_level1_list = data.get("menus", [])
    if not menus_level1_list:
        print("경고: 입력 JSON에 'menus' 배열이 비어있거나 없습니다. 파일이 생성되지 않습니다.")
        return

    # 4. 메뉴 분해 및 파일 생성
    file_counter = 0
    for menu1_item_orig in menus_level1_list:
        if menu1_item_orig.get("menuLevel") == 1 and "children" in menu1_item_orig:
            menu1_children_orig = menu1_item_orig.get("children", [])

            for menu2_item_orig in menu1_children_orig:
                if menu2_item_orig.get("menuLevel") == 2:
                    path_str = menu2_item_orig.get("path")
                    base_filename_part = "UnknownPath" # 알 수 없는 경로 기본값

                    if path_str:
                        path_parts = [part.strip() for part in path_str.split("→")]
                        if len(path_parts) >= 2:
                            base_filename_part = f"{path_parts[0]}_{path_parts[1]}"
                        elif len(path_parts) == 1:
                            base_filename_part = path_parts[0]
                        # path_parts가 분리 후 비어 있다면, path_str이 "→" 등이거나
                        # 구분자로만 구성되었을 가능성이 있음. sanitize_filename이 처리함.
                    else:
                        menu1_name_for_file = menu1_item_orig.get("menuName", "UnknownL1")
                        menu2_name_for_file = menu2_item_orig.get("menuName", "UnknownL2")
                        base_filename_part = f"{menu1_name_for_file}_{menu2_name_for_file}"
                        print(f"경고: 메뉴 항목 '{menu2_item_orig.get('menuName', 'Unnamed L2')}'에 'path'가 없습니다. 파일명에 menuName을 사용합니다: {base_filename_part}")

                    sanitized_base_filename = sanitize_filename(base_filename_part)
                    output_filename = f"{next_file_num:03d}_{sanitized_base_filename}.json"
                    output_file_path = os.path.join(output_dir_path, output_filename)

                    # 원본 데이터 구조를 수정하지 않도록 깊은 복사본 생성
                    # 다음 파일을 위해 반복할 때.
                    menu1_item_copy = copy.deepcopy(menu1_item_orig)
                    menu2_item_copy = copy.deepcopy(menu2_item_orig)

                    # 새로운 L1 메뉴는 현재 L2 메뉴만을 자식으로 가짐
                    menu1_item_copy["children"] = [menu2_item_copy]

                    new_json_content = {
                        "target": copy.deepcopy(original_target), # target도 깊은 복사본인지 확인
                        "menus": [menu1_item_copy]
                    }

                    try:
                        with open(output_file_path, 'w', encoding='utf-8') as outfile:
                            json.dump(new_json_content, outfile, ensure_ascii=False, indent=4)
                        print(f"생성됨: {output_file_path}")
                        file_counter +=1
                    except IOError as e:
                        print(f"파일 쓰기 오류 {output_file_path}: {e}")

                    next_file_num += 1

    if file_counter == 0:
        print("기준에 따라 분해할 menuLevel 1 항목 (menuLevel 2 자식 포함)을 찾을 수 없습니다.")

if __name__ == '__main__':
    # 스크립트가 실행되는 위치를 기준으로 경로를 설정합니다.
    # 이렇게 하면 스크립트가 작업 공간 내 다른 위치로 이동하더라도
    # outputs/conversion 및 outputs/decomposition 폴더를 올바르게 찾을 수 있습니다.

    print(f"입력 파일 읽기 시도: {os.path.abspath(INPUT_JSON_FILE_PATH)}")
    print(f"출력 디렉토리 쓰기 시도: {os.path.abspath(OUTPUT_DECOMPOSITION_DIR_PATH)}")

    if not os.path.exists(INPUT_JSON_FILE_PATH):
        print(f"치명적 오류: 해결된 경로에 입력 파일이 없습니다: {os.path.abspath(INPUT_JSON_FILE_PATH)}")
        print("입력 파일 경로가 올바른지 확인하거나 스크립트의 경로 구성 로직을 조정하십시오.")
    else:
        decompose_menu_json(INPUT_JSON_FILE_PATH, OUTPUT_DECOMPOSITION_DIR_PATH) 