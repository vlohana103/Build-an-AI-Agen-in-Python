import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    working_directory_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))

    valid_file_path = os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs

    if not valid_file_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_file]

    if args != None:
        command.extend(args)
    try:
        sub_run = subprocess.run(command, cwd=working_directory_abs, capture_output=True, text=True, timeout=30)

        if sub_run.returncode != 0:
            return f"Process exited with code {sub_run.returncode}"
        elif sub_run.stderr == "" and sub_run.stdout =="":
            return "No output produced"
        else:
            is_valid = []
            if sub_run.stdout:
                is_valid.append(f"STDOUT: {sub_run.stdout}")
            if sub_run.stderr:
                is_valid.append(f"STDERR: {sub_run.stderr}")
            return "\n".join(is_valid)
    except Exception as e:
        return f"Error: executing Python file: {e}"

        