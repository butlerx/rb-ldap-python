"""reading files"""


def read_file_to_string(path: str) -> str:
    """
    read file content into string
    trailing newlines are removed
    """
    with open(path, "r") as file:
        return file.read().replace("\n", "")
