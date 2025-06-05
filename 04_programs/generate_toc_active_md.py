import json
import os

def generate_toc_recursive(menu_items, current_prefix, output_lines):
    """
    메뉴 항목들을 재귀적으로 탐색하며 isTestTarget이 true인 경우 목차 라인을 생성합니다.
    숫자형 목차 형식을 사용합니다 (예: 1., 1.1., 1.1.1.).
    """
    item_counter = 1
    for item in menu_items:
        if item.get("isTestTarget") is True:
            # 현재 항목의 전체 숫자 경로 생성
            entry_prefix = f"{current_prefix}{item_counter}."
            
            menu_name = item.get("menuName", "이름 없는 메뉴") 
            output_lines.append(f"{entry_prefix} {menu_name}")
            
            if "children" in item and isinstance(item["children"], list):
                # 자식 노드 호출 시, 현재 entry_prefix를 다음 parent_prefix로 사용
                generate_toc_recursive(item["children"], entry_prefix, output_lines)
            
            item_counter += 1 # isTestTarget이 true인 항목에 대해서만 카운터 증가

def create_toc_for_active_menus():
    """
    menu_all.json을 읽어 isTestTarget이 true인 메뉴에 대한 목차 파일을 생성합니다.
    """
    script_dir = os.path.dirname(__file__)
    input_filepath = os.path.join(script_dir, "../01_inputs/menu_json_all/menu_all.json")
    output_dir = os.path.join(script_dir, "../02_outputs/toc")
    output_filepath = os.path.join(output_dir, "menu_toc_active.md")

    if not os.path.exists(input_filepath):
        print(f"입력 파일 '{input_filepath}'을(를) 찾을 수 없습니다.")
        return

    os.makedirs(output_dir, exist_ok=True) # 출력 디렉토리가 없으면 생성

    output_lines = [] # MD 파일 제목 및 초기 빈 줄 제거

    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if "menus" in data and isinstance(data["menus"], list):
            # 최상위 레벨 호출 시 current_prefix는 빈 문자열로 시작
            generate_toc_recursive(data["menus"], "", output_lines)
        else:
            print("JSON 데이터에서 'menus' 배열을 찾을 수 없거나 형식이 올바르지 않습니다.")
            return

        with open(output_filepath, 'w', encoding='utf-8') as f:
            # 파일의 첫 줄에 불필요한 줄바꿈이 생기지 않도록 수정
            if output_lines:
                f.write("\n".join(output_lines))
                f.write("\n") # 파일 끝에 줄바꿈 추가 (선택적)
        
        print(f"목차 파일이 성공적으로 생성되었습니다: '{output_filepath}'")

    except json.JSONDecodeError:
        print(f"'{input_filepath}' 파일의 JSON 형식이 올바르지 않습니다.")
    except Exception as e:
        print(f"목차 생성 중 오류 발생: {e}")

if __name__ == "__main__":
    create_toc_for_active_menus() 