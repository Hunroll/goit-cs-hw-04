from multiprocessing import Pipe, Process
from find import get_finder
import numpy as np

def find_multiprocess(files, pattern, num_of_threads):
    finder = get_finder(pattern)
    chunks = np.array_split(files, num_of_threads)
    pipes = [Pipe() for _ in range(num_of_threads)]
    for i in range(num_of_threads):
        if chunks[i].any():
            w = Process(target=worker, args=(pipes[i][0], ))
            w.start()
            pipes[i][1].send(pattern) # Distribute pattern
            pipes[i][1].send(chunks[i]) # Distribute files
            
    matched = []
    skipped = []
    for i in range(num_of_threads):
        if chunks[i].any():
            results = pipes[i][1].recv()
            zipped = list(zip(chunks[i], results))
            matched = matched + list([tup[0] for tup in zipped if tup[1] == 0])
            skipped = skipped + list([tup[0] for tup in zipped if tup[1] == -1])
    
    return {pattern: matched, None: skipped} # None - key for skipped/errored files


def worker(pipe):
    res = None
    try:
        pattern = pipe.recv()
        files = pipe.recv()
        finder = get_finder(pattern)
        res = [finder(file) for file in files]
        
    except Exception as err:
        print("Unexpected error in thread:", err)
    finally:
        pipe.send(res)
