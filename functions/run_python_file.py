import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        work_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(work_dir, file_path))

        valid_target_file = os.path.commonpath([work_dir, target_file]) == work_dir
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args:
            command.extend(args)

        result = subprocess.run(
            command, 
            check=True, 
            cwd=work_dir, 
            capture_output=True, 
            text=True, 
            timeout=30,
        )
        output = []
        if result.returncode != 0:
            output.append(f'Process exited with code {result.returncode}')
        if not result.stderr and not result.stdout:
            output.append(f'No output produced\n')
        if result.stdout:
            output.append(f'STDOUT:\n{result.stdout}')
        if result.stderr:
            output.append(f'STDERR:\n{result.stderr}')
 
        return "\n".join(output)
    except Exception as e:
        return f'Error: executing Python file: {e}'


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file relative to the working directory, returning the output or any errors produced during execution",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of string arguments to pass to the Python file when executing",
            ),
        },
        required=["file_path"],
    ),
)