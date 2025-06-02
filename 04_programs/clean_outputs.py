import os
import shutil

def clean_output_folder(folder_path):
    """
    지정된 폴더 및 하위 폴더에서 .md 파일과 .png 파일을 삭제합니다.
    폴더 구조는 유지됩니다.

    Args:
        folder_path (str): 삭제 작업을 수행할 대상 폴더 경로입니다.
    """
    print(f"Cleaning folder: {folder_path}")
    if not os.path.isdir(folder_path):
        print(f"Error: Folder not found at {folder_path}")
        return

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md") or file.endswith(".png"):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                except OSError as e:
                    print(f"Error deleting file {file_path}: {e}")
        
        # 디렉토리는 삭제하지 않으므로 dirs에 대한 별도 처리는 필요 없습니다.
        # 만약 빈 디렉토리도 삭제하고 싶다면 여기서 추가 로직이 필요합니다.
        # 현재 요구사항은 디렉토리 유지이므로 그대로 둡니다.

    print("Cleanup complete. Directories have been preserved.")

if __name__ == "__main__":
    # 현재 스크립트 (04_programs/clean_outputs.py)의 위치를 기준으로 workspace root 경로를 동적으로 계산합니다.
    # 스크립트 파일의 절대 경로 예: C:\workspace_cursor\itscope_online_manual_md\04_programs\clean_outputs.py
    # script_dir: C:\workspace_cursor\itscope_online_manual_md\04_programs
    # workspace_root_derived: C:\workspace_cursor\itscope_online_manual_md
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root_derived = os.path.dirname(script_dir) # 스크립트가 있는 폴더(04_programs)의 부모 폴더를 workspace root로 간주
    
    target_directory_abs = os.path.join(workspace_root_derived, "02_outputs")

    clean_output_folder(target_directory_abs) 