import os


def get_files_info(working_directory, directory="."):

	directory_check = os.path.isdir(working_directory)

	if not directory_check:
		raise Exception(f'Error: "{directory}" is not a directory')

	working_dir_abs  = os.path.abspath(working_directory)
	target_directory = os.path.normpath(os.path.join(working_dir_abs, directory))
	valid_target_dir = os.path.commonpath([working_dir_abs, target_directory]) == working_dir_abs


	if valid_target_dir:
#		TODO
		if os.path.isdir(working_directory):
			get_files_info(working_directory, )
		file_size = os.path.getsize(target_directory)
		dir_check = os.path.isdir(target_directory)
		print(f"{working_directory}: file_size={file_size}, is_dir={dir_check}")
	else:
		raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
