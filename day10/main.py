import os
import sys
import pathlib

from collections import deque

parent_directory = os.path.abspath('.')
sys.path.append(parent_directory)

import helper

pipes = {
    '|': {1j:1j},
    '-': {1:1},
    'L': {1j:1},
    'J': {1j:-1},
    '7': {1:1j},
    'F': {-1j:1},
}

for p in pipes:
    pd = pipes[p]
    for d in list(pd.keys()):
        pd[-pd[d]] = -d


def solution(input_file):
    result = 0
    coor = 0
    lines = open(input_file, 'r').read().splitlines()
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == 'S':
                coor = j + i * 1j
                break
        else:
            continue
        break

    get_char = lambda coor: lines[int(coor.imag)][int(coor.real)]

    q = deque()
    # find first tiles
    for d in [1,-1,1j,-1j]:
        next_pipe = pipes.get(get_char(coor+d))
        if next_pipe is not None and d in next_pipe:
            q.append((coor+d, d, 1))

    visited = set([coor])
    distances = {coor: 0}
    max_dist = 0
    while True:
        c, d, dist = q.popleft()
        if c in visited:
            break
        next_d = pipes[get_char(c)][d]

        q.append((c+next_d, next_d, dist+1))
        max_dist = dist

        visited.add(c)
        distances[c] = dist

    tile_count = 0
    for j, line in enumerate(lines):
        for i, tile in enumerate(line):
            if tile in visited:
                continue
            c_count = 0
            if i + j*1j not in visited:
                opening = None
                for ii in range(i, len(line)):
                    coor = ii+j*1j
                    c = get_char(coor)

                    if coor not in visited:
                        continue

                    if c == '-':
                        continue

                    if c in ['L','F']:
                        opening = c
                        c_count += 1

                    elif opening is not None:
                        if c in ['J','S'] and opening == 'L':
                            c_count += 1
                        elif c == '7' and opening == 'F':
                            c_count += 1
                        opening = None

                    else:
                        c_count += 1
            
            if c_count % 2 == 1:
                tile_count += 1

    return max_dist, tile_count

def solution2(input_file):
    result = 0
    lines = open(input_file, 'r').read().splitlines()
    for i, line in enumerate(lines):
        pass

    return result

if __name__ == '__main__':
    file_directory = pathlib.Path(__file__).parent.absolute()
    if 1: # run part 1
        print(helper.benchmark(solution)(file_directory / 'test.txt'))
        print('\n*******************************\n')
        print(helper.benchmark(solution)(file_directory / 'input.txt'))
    if 0: # run part 2
        print('\n----------------part2----------------\n')
        print(helper.benchmark(solution2)(file_directory / 'test.txt'))
        print('\n*******************************\n')
        print(helper.benchmark(solution2)(file_directory / 'input.txt'))