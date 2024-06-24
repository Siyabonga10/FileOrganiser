from StatusCodes import FileFilterModes, StatusCodes
import os


def sort_by_name(path: str, sub_string: str, new_file_path: str, file_filter_mode: FileFilterModes) -> StatusCodes:
    if not os.access(path, os.W_OK):
        return StatusCodes.BASE_PATH_NOT_FOUND

    # Check if the new folder already exists
    if not os.access(new_file_path, os.F_OK):
        os.mkdir(new_file_path)

    # Ignore casing modes for now
    filter_function = FileFilterModes.get_filter_function(file_filter_mode)
    if not filter_function:
        return StatusCodes.INTERNAL_ERROR

    entries = os.listdir(path)
    selected_entries = []
    for entry in entries:
        if filter_function(entry, sub_string):
            selected_entries.append(entry)

    for selected_file in selected_entries:
        os.rename(os.path.join(path, selected_file), f'{new_file_path}/{selected_file}')

    return StatusCodes.SUCCESS



