import math
from multiprocessing import Pool
import functools

with open("english_words.txt") as f:
    words = [word.strip() for word in f.readlines()]
    
def map_average(words_chunk):
    length = 0
    for word in words_chunk:
        length += len(word)
    return length / len(words)

def reduce_average(res1, res2):
    return res1 + res2

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

    average_word_len = map_reduce(words, 4, map_average, reduce_average)
    print(average_word_len)
