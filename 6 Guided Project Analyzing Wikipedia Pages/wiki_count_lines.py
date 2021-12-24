import math
from multiprocessing import Pool
import functools
import os

file_names = os.listdir("wiki")

def count_lines(jobs_chunk):
    count = 0
    for link in jobs_chunk:
        with open("wiki/"+link) as f:
#            count += len(f.read())
            lines = f.readlines()
            line_count = len(lines)
            count += line_count
    return count

def reduce_count_lines(count1, count2):
    return count1 + count2

def make_chunks(data, num_chunks):
    chunk_size = math.ceil(len(data) / num_chunks)
    return [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

if __name__ == "__main__":
    __spec__ = None
    def map_reduce(data, num_processes, mapper, reducer):
        chunks = make_chunks(data, num_processes)
        with Pool(num_processes) as pool:
            chunk_results = pool.map(mapper, chunks)
        return functools.reduce(reducer, chunk_results)

    count_lines = map_reduce(file_names, 4, count_lines, reduce_count_lines)
    print(count_lines)
