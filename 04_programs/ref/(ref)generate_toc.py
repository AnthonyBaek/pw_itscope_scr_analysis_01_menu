import json
import os

def parse_menu(menu_item, prefix, output_lines):
    if "level" in menu_item:
        output_lines.append(f"{prefix} {menu_item['name']}")
        if "children" in menu_item:
            for i, child in enumerate(menu_item["children"]):
                parse_menu(child, f"{prefix}.{i + 1}", output_lines)

def main():
    menu_tree_path = "inputs/menutree_by_ai/menuTree"
    output_file = "toc.md"
    all_output_lines = []
    
    file_names = sorted([f for f in os.listdir(menu_tree_path) if f.endswith(".json")])
    
    major_number = 1
    for file_name in file_names:
        file_path = os.path.join(menu_tree_path, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 파일 최상위가 리스트인 경우와 객체인 경우를 모두 처리
                if isinstance(data, list):
                    for item in data:
                        # 최상위 레벨 메뉴 항목에 대해서만 major_number 사용
                        if item.get("level") == 1 : # level 1 항목에 대해서만 major_number 적용
                             parse_menu(item, str(major_number), all_output_lines)
                             major_number+=1
                        else: # level 1이 아닌 다른 level의 아이템들은 이전 major_number를 따름
                            # 이 경우는 일반적으로는 없어야 하지만, 예외 케이스를 위해 추가
                            # 또는 level 1이 아닌 아이템은 무시하도록 처리할 수도 있습니다.
                            # 현재 로직에서는 level 1이 아닌 최상위 아이템은 무시됩니다.
                            pass


                elif isinstance(data, dict):
                     # 최상위 레벨 메뉴 항목에 대해서만 major_number 사용
                    if data.get("level") == 1 : # level 1 항목에 대해서만 major_number 적용
                        parse_menu(data, str(major_number), all_output_lines)
                        major_number +=1
                    else: # level 1이 아닌 다른 level의 아이템들은 이전 major_number를 따름
                        # 이 경우는 일반적으로는 없어야 하지만, 예외 케이스를 위해 추가
                        # 또는 level 1이 아닌 아이템은 무시하도록 처리할 수도 있습니다.
                        # 현재 로직에서는 level 1이 아닌 최상위 아이템은 무시됩니다.
                        pass


        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {file_path}")
        except Exception as e:
            print(f"An error occurred while processing {file_path}: {e}")

    with open(output_file, 'w', encoding='utf-8') as f:
        for line in all_output_lines:
            f.write(line + "\n")

if __name__ == "__main__":
    main() 