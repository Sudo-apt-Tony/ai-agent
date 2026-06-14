import os


def get_files_info(working_directory: str = os.getcwd(), directory: str = ".") -> str:
    if not os.path.isdir(os.path.join(working_directory, directory)):
        return f'Error: "{directory}" is not a directory.'

    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))

    valid_target_dir = (
        os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
    )

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    dir_info = ""
    if directory == ".":
        dir_info = "Result for current directory:"
    else:
        dir_info = f"Result for '{directory}' directory:"

    accumulator = [dir_info]
    seperator = "\n"
    with os.scandir(target_dir) as td:
        for entry in td:
            name = entry.name
            size = os.path.getsize(os.path.join(target_dir, entry))
            dir_check = entry.is_dir()
            accumulator.append(
                f"  - {name}: file_size={size} bytes, is_dir={dir_check}"
            )
    dir_info = seperator.join(accumulator)

    return dir_info
