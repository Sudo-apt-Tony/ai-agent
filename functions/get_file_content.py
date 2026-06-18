import os

from google.genai import types

from config import MAX_CHARS

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the content of a specified file relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path inside working directory to file to be parsed.",
            ),
        },
        required=["file_path"],
    ),
)


def get_file_content(working_directory: str, file_path: str) -> str:

    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
    valid_target_file = (
        os.path.commonpath([abs_working_dir, target_file]) == abs_working_dir
    )

    if not valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_file, "r") as f:
            file_content_str = f.read(MAX_CHARS)

            if f.read(1):
                file_content_str += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

            return file_content_str
    except PermissionError:
        print("Error: You do not have permission to read this file.")
    except FileNotFoundError:
        print("Error: The file does not exist.")

    return "Error: Failed to read file. Please confirm working directory and path and try again."
