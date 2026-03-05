import os

def get_files_info(working_directory, directory="."):
    working_directory_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))


    valid_target_dir = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    try:
        path_list = []
        for file_name in os.listdir(target_dir):
            com_path = os.path.join(target_dir, file_name)
            file_size = os.path.getsize(com_path)
            is_dir = os.path.isdir(com_path)
            path_list.append(f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(path_list)
    except Exception as e:
        return f"Error: {e}"