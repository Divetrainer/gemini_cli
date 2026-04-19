import os
from config import MAX_CHARS
from google import genai
from google.genai import types

def get_file_content(working_directory, file_path):

	try:
		#directory validation
		if not os.path.isdir(working_directory):
			return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

		working_dir_abs = os.path.abspath(working_directory)
		target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))


		#type validation
		if not os.path.isfile(target_file):
			return f'Error: File not found or is not a regular file: "{file_path}"'

		if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
			return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'


		with open(target_file, "r") as f:
			file_content_string = f.read(MAX_CHARS)
			if f.read(1):
				file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

		return file_content_string

	except Exception as e:
		return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
	name="get_file_content",
	description="lists the contents of the file",
	parameters=types.Schema(
		required=["file_path"],
		type=types.Type.OBJECT,
		properties={
			"file_path":types.Schema(
				type=types.Type.STRING,
				description="specific file type that is being read",
			),
		},
	),
)
