import math
from multiprocessing import Pool
import functools
import os

file_names = os.listdir("wiki")
articles = [f.replace(".html", "") for f in file_names]

def count_link(jobs_chunk):
    d = {}
    for link in jobs_chunk:
        with open("wiki/"+link+'.html') as f:
            slink = link.lower()
            lines = f.readlines()
            line_count = len(lines)
            for i in range(line_count):
                lower_lines = lines[i].lower().count(slink)
                if lower_lines > 0:
                    if link not in d:
                        d[link] = [i]
                    else:
                        d[link].append(i)  
    return d
                        
def reducer(freq1, freq2):
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

    count_links = map_reduce(articles, 4, count_link, reducer)
    print(count_links)
