import os, subprocess

def run_python_file(working_directory, file_path, args=None):
	try:
		working_dir_abs = os.path.abspath(working_directory)
		target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))


		if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
			return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

		if not os.path.isfile(target_file):
			return f'Error: "{file_path}" does not exist or is not a regular file'

		if not file_path.endswith('.py'):
			return f'Error: "{file_path}" is not a Python file'


		command = ["python", target_file]
		if args:
			command.extend(args)

		command_ran = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
		return_code_output = ""
		if command_ran.returncode != 0:
			return_code_output = f'Process exited with code {command_ran.returncode}\n'
		if not command_ran.stdout and not command_ran.stderr:
			stdout_stderr_output = f'No output produced\n'
		if command_ran.stdout or command_ran.stderr:
			stdout_stderr_output = f'STDOUT:"{command_ran.stdout}"\nSTDERR:"{command_ran.stderr}"'

		output = return_code_output + stdout_stderr_output

		return output


	except Exception as e:
		return f'Error: executing Python file: {e}'
