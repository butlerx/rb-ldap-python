"""reading files"""


def read_file_to_string(path: str) -> str:
    """
    read file content into string
    trailing newlines are removed

    Args:
        path: of file to read in

    Return:
        Return string with content of the file
    """
    with open(path, "r") as file:
        return file.read().strip()
