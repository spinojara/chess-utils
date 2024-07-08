#!/usr/bin/env python3

import argparse
import subprocess
import pathlib

def search(engine, fen, depth):
    engine.stdin.write('ucinewgame\n')
    engine.stdin.write(f'position fen {fen}\n')
    engine.stdin.write(f'go depth {depth}\n')
    engine.stdin.flush()
    
    nodes = 0
    time = 0
    for output in engine.stdout:
        if not output or output.startswith('bestmove'):
            break
        output = output.split()
        if output[0] != 'info' or not 'nodes' in output or not 'time' in output:
            continue

        nodes = int(output[output.index('nodes') + 1])
        time  = int(output[output.index('time') + 1])

    return nodes, time

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('engine', type=str, help='Engine path')
    parser.add_argument('book', type=str, help='Opening epd book')
    parser.add_argument('depth', type=int, help='Search depth')
    parser.add_argument('fens', type=int, help='Max fens', nargs='?', default=-1)

    args = parser.parse_args()

    engine = subprocess.Popen(args.engine, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    total = 0
    nodes = 0
    time = 0
    with open(args.book, 'r') as book:
        for fen in book:
            if args.fens >= 0 and total >= args.fens:
                break
            n, t = search(engine, fen, args.depth)
            nodes += n
            time += t
            total += 1
            print(total)
    engine.terminate()
    print(f'Average nodes: {nodes / total}')
    print(f'Average time:  {time / total} ms')

if __name__ == '__main__':
    main()
