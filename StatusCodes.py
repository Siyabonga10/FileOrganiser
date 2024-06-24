from enum import Enum, auto


class FileFilterModes(Enum):
    STARTS_WITH = auto()
    ENDS_WITH = auto()
    CONTAINS = auto()

    @staticmethod
    def get_filter_function(filter_mode):
        filter_function_mapping = {
            FileFilterModes.STARTS_WITH: lambda base_str, sub_str: base_str.startswith(sub_str),
            FileFilterModes.ENDS_WITH: lambda base_str, sub_str: base_str.endswith(sub_str),
            FileFilterModes.CONTAINS: lambda base_str, sub_str: sub_str in base_str
        }
        return filter_function_mapping.get(filter_mode, None)


class StatusCodes(Enum):
    SUCCESS = auto()
    BASE_PATH_NOT_FOUND = auto()
    NEW_PATH_CREATION_FAILED = auto()
    INTERNAL_ERROR = auto()
    UNKNOWN_ERROR = auto()

    @staticmethod
    def get_message(status_code):
        status_code_messages = {
            StatusCodes.SUCCESS: "Files successfully sorted",
            StatusCodes.BASE_PATH_NOT_FOUND: "Could not find the selected base path",
            StatusCodes.NEW_PATH_CREATION_FAILED: "Could not find or create the new specified path",
            StatusCodes.INTERNAL_ERROR: "An internal error occurred, restart application and try again",
            StatusCodes.UNKNOWN_ERROR: "An unknown error occurred"
        }

        return status_code_messages.get(status_code, status_code_messages[StatusCodes.UNKNOWN_ERROR])


