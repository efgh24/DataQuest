import math
from multiprocessing import Pool
import functools

with open("english_words.txt") as f:
    words = [word.strip() for word in f.readlines()]
    
def map_char_count(words_chunk):
    char_freq = {}
    for word in words_chunk:
        for c in word:
            if c not in char_freq:
                char_freq[c] = 0
            char_freq[c] += 1
    return char_freq

def reduce_char_count(freq1, freq2):
    for c in freq2:
        if c in freq1:
            freq1[c] += freq2[c]
        else:
            freq1[c] = freq2[c]
    return freq1

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

    char_freq = map_reduce(words, 4, map_char_count, reduce_char_count)
    print(char_freq)
