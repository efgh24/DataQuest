import math
from multiprocessing import Pool
import functools

with open("english_words.txt") as f:
    words = [word.strip() for word in f.readlines()]
    
def map_adjacent(words_chunk):
    adj_freq = {}
    for word in words_chunk:
        for i in range(len(word) - 1):
            seq = word[i] + word[i + 1]
            if seq not in adj_freq:
                adj_freq[seq] = 0
            adj_freq[seq] += 1
    return adj_freq


def reduce_adjacent(freq1, freq2):
    for seq in freq2:
        if seq in freq1:
            freq1[seq] += freq2[seq]
        else:
            freq1[seq] = freq2[seq]
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

    pair_freq = map_reduce(words, 4, map_adjacent, reduce_adjacent)
    unique_pairs = [seq for seq in pair_freq if pair_freq[seq] == 1]
    print(unique_pairs)
