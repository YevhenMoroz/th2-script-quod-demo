import os


def delete_all_files_with_extension(directory: str, extension: str):
    filtered_files = find_files_by_extension(directory, extension)

    for file in filtered_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)


def find_files_by_extension(directory: str, extension: str):
    files_in_directory = os.listdir(directory)
    return [file for file in files_in_directory if file.endswith(extension)]
