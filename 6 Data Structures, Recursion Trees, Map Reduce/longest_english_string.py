import math
from multiprocessing import Pool
import functools

with open("english_words.txt") as f:
    words = [word.strip() for word in f.readlines()]
    
def map_max_len_str(words_chunk):
    return max(words_chunk, key=len) 

def reduce_max_len_str(word1, word2):
    return map_max_len_str([word1, word2])

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

    max_len_str = map_reduce(words, 4, map_max_len_str, reduce_max_len_str)
    print(max_len_str)
