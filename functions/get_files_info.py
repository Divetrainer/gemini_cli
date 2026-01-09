import os

def get_files_info(working_directory, directory="."):

	#validate if working directory is a directory
	if not os.path.isdir(working_directory):
		return f'Error: "{working_directory}" is not a directory'

	working_dir_abs  = os.path.abspath(working_directory)
	target_directory = os.path.normpath(os.path.join(working_dir_abs, directory))

	#validate target directory as a directory
	if not os.path.isdir(target_directory):
		return f'Error: "{directory}" is not a directory'

	#validate we are in the right path
	if os.path.commonpath([working_dir_abs, target_directory]) != working_dir_abs:
		return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

	folder_contents = []
	entries = os.listdir(target_directory)
	for entry in entries:
		full_path = os.path.join(target_directory, entry)
		file_size = os.path.getsize(full_path)
		directory_val = os.path.isdir(full_path)
		folder_contents.append(f'- {entry}: file_size={file_size} bytes, is_dir={directory_val}')
	return"\n".join(folder_contents)
 
