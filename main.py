import pathlib
import sys
from colorama import Fore, Style
from itertools import chain
import task1, task2
import time


def main():
    try:
        if (len(sys.argv) != 3):
            print(Fore.RED + "Incorrect number of arguments")
            print(Style.RESET_ALL + "usage: python main.py path_to_dir \"pattern\"")
            sys.exit(1)
        directory_path = pathlib.Path(sys.argv[1])
        if (not directory_path.exists()):
            print(Fore.RED + "Path does not exist")
            sys.exit(2)
        if (not directory_path.is_dir()):
            print(Fore.RED + "Path is not a directory")
            sys.exit(3)
        pattern = sys.argv[2]
        
        list_of_files = enumerate_dir(directory_path)
        print(f"{len(list_of_files)} files in directory")

        start_time = time.time()
        res_dict = task1.find_multithreaded(list_of_files, pattern, num_of_threads=4)
        print("Multithreaded version finished in %s seconds" % (time.time() - start_time))
        print("Found pattern in following files:\n"+"\n".join([file.as_posix() for file in res_dict[pattern]]))
        print(f"Skipped {len(res_dict[None])} files")


        start_time = time.time()
        res_dict = task2.find_multiprocess(list_of_files, pattern, num_of_threads=4)
        print("Multiprocess version finished in %s seconds" % (time.time() - start_time))
        print("Found pattern in following files:\n"+"\n".join([file.as_posix() for file in res_dict[pattern]]))
        print(f"Skipped {len(res_dict[None])} files")

    except Exception as err:
        print (f"Unexprected error: {err}")
        sys.exit(9)
    finally:
        print (Style.RESET_ALL)

def enumerate_dir(directory: pathlib.Path):
    files = list([x for x in directory.iterdir() if x.is_file()])
    inner_files = [enumerate_dir(x) for x in directory.iterdir() if x.is_dir()]
    files += chain(*inner_files)
    return files


if __name__ == '__main__':
    main()