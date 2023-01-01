import time
import sys
import random
from BeltCreation import BeltCreation
sys.setrecursionlimit(10000000)


def main():
    # height = random.randint(2, 10)
    # width = random.randint(2, 10)

    # map_size = [2, 3, 4, 5, 6]
    map_size = [5]
    times = 1

    # fill_ratio = random.uniform(0, 0.3)
    fill_ratio = 0
    for size in map_size:
        height = width = size
        time_record = set()
        for i in range(times):
            sy, sx = 0, random.randint(0, width-1)
            while True:
                gy, gx = random.randint(0, height-1), random.randint(0, width-1)
                yx = random.choice([0,1])
                if yx == 0: gy = random.choice([0, height-1])
                else: gx = random.choice([0, width-1])
                if not (gx == sx and gy == sy): break
            pc = BeltCreation(width, height, (sy,sx), (gy,gx))
            dp1 = pc.create_dp()
            dp1 = pc.dp_forward(dp1)
            cnt = 0
            while True:
                dp2 = pc.dp_backward(dp1, fill_ratio+cnt)
                route = pc.find_route_by_bfs_dfs(dp2)
                cnt += 0.1
                if route: break
                if cnt == 1: break

            result_route_map = pc.reformat_map(route)
            pretime = time.time()
            pole_area = pc.create_pole_arrangement(result_route_map)
            newtime = time.time()
            
            time_record.add(newtime-pretime)

        print("size:", size)
        print("実行平均時間:", sum(time_record)/len(time_record))
        print("最悪実行時間:", max(time_record))
        print("最小実行時間:", min(time_record))
    
    # print("Map:", height, "*", width)
    # print("Start:", sy, sx)
    # print("Goal:", gy, gx)
    # print("Filling Ratio:", fill_ratio)
    for row in pole_area:
        for i in row:
            print(str(i).rjust(4), end="")
        print("")

if __name__ == "__main__":
    main()

