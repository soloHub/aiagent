import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        work_dir_abs = os.path.abspath(working_directory)
        target_dir_abs = os.path.normpath(os.path.join(work_dir_abs, directory))

        valid_target_dir = os.path.commonpath([work_dir_abs, target_dir_abs]) == work_dir_abs
        if not valid_target_dir:
            return ValueError(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')

        if not os.path.isdir(target_dir_abs):
            return ValueError(f'Error: "{directory}" is not a directory')

        files_info = []
        for filename in os.listdir(target_dir_abs):
            file_path = os.path.join(target_dir_abs, filename)
            is_dir = os.path.isdir(file_path)
            file_size = os.path.getsize(file_path)
            files_info.append(f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(files_info)
    except Exception as e:
        return f'Error listing files: {e}'

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)