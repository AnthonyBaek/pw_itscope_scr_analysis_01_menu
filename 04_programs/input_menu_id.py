import json
import os

def assign_menu_ids(menus, parent_id=None, level1_counter=0):
    """
    메뉴 항목들에 재귀적으로 menuId를 할당합니다.
    level1_counter는 최상위 레벨(menuLevel 1)의 ID 생성을 위해 사용됩니다.
    """
    counter = 1
    for menu_item in menus:
        current_menu_level = menu_item.get("menuLevel")
        new_id = ""

        if current_menu_level == 1:
            level1_counter += 1
            new_id = f"MN{level1_counter:02d}"
        elif parent_id and (current_menu_level == 2 or current_menu_level == 3):
            new_id = f"{parent_id}.{counter:02d}"
        else:
            # 예상치 못한 경우 또는 parent_id가 없는 하위 레벨 (오류 상황일 수 있음)
            # 또는 menuLevel이 1,2,3이 아닌 경우
            print(f"경고: menuId를 할당할 수 없는 항목입니다. menuLevel: {current_menu_level}, parent_id: {parent_id}, menuName: {menu_item.get('menuName')}")
            # menuId를 비워두거나 기본값을 설정할 수 있습니다. 여기서는 비워둡니다.
            menu_item["menuId"] = ""
            if "children" in menu_item and menu_item["children"]:
                # 자식 노드가 있는 경우, level1_counter는 그대로 전달 (하위에서 사용 안 함)
                assign_menu_ids(menu_item["children"], "", level1_counter=level1_counter) # parent_id를 빈 문자열로 전달하여 하위에서 ID 생성 방지
            continue # 다음 아이템으로
        
        menu_item["menuId"] = new_id
        counter += 1

        if "children" in menu_item and menu_item["children"]:
            # 자식 노드가 있는 경우, level1_counter는 그대로 전달 (하위에서 사용 안 함)
            assign_menu_ids(menu_item["children"], new_id, level1_counter=level1_counter)
    return level1_counter # 다음 최상위 호출을 위해 업데이트된 level1_counter 반환

def process_menu_file():
    script_dir = os.path.dirname(__file__)
    # menu_all.json 파일 경로 직접 지정
    filepath = os.path.join(script_dir, '../01_inputs/menu_json_all/menu_all.json')

    if not os.path.exists(filepath):
        print(f"'{filepath}' 파일을 찾을 수 없습니다.")
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"'{os.path.basename(filepath)}' 파일 JSON 디코딩 중 오류 발생: {e}")
        return
    except Exception as e:
        print(f"'{os.path.basename(filepath)}' 파일 읽기 중 오류 발생: {e}")
        return

    if 'menus' in data and isinstance(data['menus'], list):
        assign_menu_ids(data['menus'])
    else:
        print("Error: 'menus' 키가 없거나 리스트 형식이 아닙니다.")
        return

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"'{os.path.basename(filepath)}' 파일의 menuId를 성공적으로 업데이트했습니다.")
    except Exception as e:
        print(f"'{os.path.basename(filepath)}' 파일 저장 중 오류 발생: {e}")

if __name__ == "__main__":
    process_menu_file() 