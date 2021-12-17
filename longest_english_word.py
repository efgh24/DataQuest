import math
from multiprocessing import Pool
import functools

with open("english_words.txt") as f:
	words = [word.strip() for word in f.readlines()]

def map_max_length(words_chunk):
	return max([len(word) for word in words_chunk])

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

	max_len = map_reduce(words, 4, map_max_length, max)
	print(max_len)
