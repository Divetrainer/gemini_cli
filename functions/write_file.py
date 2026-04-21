import os
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):
	try:
		if not os.path.isdir(working_directory):
			return f'Error: "{working_directory}" is not a directory'

		working_dir_abs = os.path.abspath(working_directory)
		target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

#		print(target_file)

		if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
			return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

		os.makedirs(os.path.dirname(target_file), exist_ok=True)

		if os.path.isdir(target_file):
			return f'Error: Cannot write to "{file_path}" as it is a directory'

		with open(target_file, "w") as f:
			f.write(content)

		return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


	except Exception as e:
		return f'Error: "{e}"'

schema_write_file = types.FunctionDeclaration(
	name="write_file",
	description="This will modify an existing or create a new file and input text into it",
	parameters=types.Schema(
		required=["file_path", "content"],
		type=types.Type.OBJECT,
		properties={
			"file_path":types.Schema(
				type=types.Type.STRING,
				description="specific file that is being accessed or created",
			),
			"content":types.Schema(
				type=types.Type.STRING,
				description="Information to be written into the file being created or accessed",
			),
		},
	),
)
