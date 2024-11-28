import concurrent.futures
from find import get_finder

def find_multithreaded(files, pattern, num_of_threads):
    finder = get_finder(pattern)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_of_threads) as executor:
        results = list(executor.map(finder, files))
    zipped = list(zip(files, results))
    return {pattern: list([tup[0] for tup in zipped if tup[1] == 0]), None: list([tup[0] for tup in zipped if tup[1] == -1])} # None - key for skipped/errored files