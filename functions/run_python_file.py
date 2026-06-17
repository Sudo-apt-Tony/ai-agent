import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        abs_work_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_work_dir, file_path))
        valid_target_file = (
            os.path.commonpath([abs_work_dir, target_file]) == abs_work_dir
        )

        if not valid_target_file:
            print(
                f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            )
        if not os.path.isfile(target_file):
            print(f'Error: "{file_path}" does not exist or is not a regular file')
        if file_path[-2:] != "py":
            print(f'Error: "{file_path}" is not a Python file')

        command = ["python", target_file]
        command.extend(args) if args else command
        complete = subprocess.run(
            command,
            cwd=abs_work_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = ""
        if complete.returncode != 0:
            output += f"Process exited with code {complete.returncode}"
        if not complete.stderr and not complete.stdout:
            output += "No output produced"
        else:
            output += f"STDOUT:\n{complete.stdout}"
            output += f"STDERR:\n{complete.stderr}"

        return output

    except Exception as e:
        print(f"Error: executing Python file: {e}")
        return f"Error: executing Python file: {e}"
