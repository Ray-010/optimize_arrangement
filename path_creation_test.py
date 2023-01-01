import time
import sys
import random
from PathCreation import PathCreation
sys.setrecursionlimit(10000000)

def main():
    height = width = 3
    fill_ratio = 0

    sy, sx = 0, random.randint(0, width-1)
    while True:
        gy, gx = random.randint(0, height-1), random.randint(0, width-1)
        yx = random.choice([0,1])
        if yx == 0: gy = random.choice([0, height-1])
        else: gx = random.choice([0, width-1])
        if not (gx == sx and gy == sy): break
    pc = PathCreation(width, height, (sy,sx), (gy,gx))
                
    dp1 = pc.create_dp()
    dp1 = pc.dp_forward(dp1)
    dp2 = pc.dp_backward(dp1, fill_ratio)
    route = pc.find_route_by_bfs_dfs(dp2) # bfs再帰経路復元
    print(route)
    result_route_map = pc.reformat_map(route)

    for row in result_route_map:
        print(row)
    for row in dp2:
        print(row)
    

if __name__ == "__main__":
    main()

