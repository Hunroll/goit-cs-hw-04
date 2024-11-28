import pathlib
from colorama import Fore, Style

def get_finder(pattern: str):
    def find_in_file(path: pathlib.Path) -> int:
        try:
            text = path.read_text()
            return 0 if pattern in text else 1
        except:
            # mess = Fore.RED + f"Error reading file {path}"+Style.RESET_ALL
            # print(mess)
            return -1
    return find_in_file