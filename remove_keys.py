import os
import re
import json, argparse
import shutil

regex_patterns = [
    r'tvly-\w{28,}',
    r'sk-proj-\w{40,}',
    r"gsk_\w{40,}",
    r'fvUhEjtQfIL7ZpBdnO1zlsITnZABqWighs8gMFEJ',
    r'sk-(ant|proj)-[A-Za-z0-9_\-]+'
    ]

def remove_patterns(content):
    for pattern in regex_patterns:
        content = re.sub(pattern, '', content)
    return content

def remove_keys(folder_path):
    global regex_patterns
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith('.py'): 
                file_path = os.path.join(root, filename)

                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                origin_content=content
                modified = False
                for pattern in regex_patterns:
                    content = re.sub(pattern, '', content)
                if origin_content != content:
                    modified=True

                if modified:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(content)
                    print(f"{file_path} (.py) 처리 완료")
                else:
                    print(f"{file_path} (.py) 변경 사항 없음")

            elif filename.endswith('.ipynb'):
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        notebook = json.load(file)

                    modified = False
                    for cell in notebook.get('cells', []):
                        if cell.get('cell_type') == 'code':
                            new_source = []
                            for line in cell.get('source', []):
                                new_line = remove_patterns(line)
                                new_source.append(new_line)
                            if new_source != cell['source']:
                                cell['source'] = new_source
                                modified = True

                    if modified:
                        with open(file_path, 'w', encoding='utf-8') as file:
                            json.dump(notebook, file, ensure_ascii=False, indent=4)
                        print(f"{file_path} (.ipynb) 처리 완료")
                    else:
                        print(f"{file_path} (.ipynb) 변경 사항 없음")
                except Exception as e:
                    print(f"오류 발생: {file_path} - {e}")

def delete_specified_folders(root_dir):
    # Traverse the directory tree
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # List of directories to delete
        folders_to_delete = ['__pycache__', '.ipynb_checkpoints']
        
        for folder_name in folders_to_delete:
            folder_path = os.path.join(dirpath, folder_name)
            if os.path.exists(folder_path):
                print(f'Deleting folder: {folder_path}')
                shutil.rmtree(folder_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, )

    args = parser.parse_args()
    remove_keys(args.path)
    delete_specified_folders(args.path)