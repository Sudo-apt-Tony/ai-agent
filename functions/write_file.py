import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the input content to the input file relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path inside working directory to file to be parsed.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to the file_path inside the working directory.",
            ),
        },
        required=["file_path"],
    ),
)


def write_file(working_directory: str, file_path: str, content: str) -> str:

    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
    valid_target_file = (
        os.path.commonpath([abs_working_dir, target_file]) == abs_working_dir
    )

    print(f"{target_file}")

    if not valid_target_file:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    try:
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
    except FileExistsError as e:
        print(f"Error: {e}")

    with open(target_file, "w") as w:
        w.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
