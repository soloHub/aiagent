import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        work_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(work_dir, file_path))

        valid_target_file = os.path.commonpath([work_dir, target_file]) == work_dir
        if not valid_target_file:
            return ValueError(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        
        if os.path.isdir(target_file):
            return ValueError(f'Error: Cannot write to "{file_path}" as it is a directory')

        # Ensure the directory exists
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error writing file: {e}'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file relative to the working directory, creating the file if it does not exist and ensuring it is not a directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)