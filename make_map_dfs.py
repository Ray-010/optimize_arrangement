import time
import sys
import random
from create_route import CreateRoute
sys.setrecursionlimit(10000000)


def main():
    height = random.randint(2, 10)
    width = random.randint(2, 10)
    sy, sx = 0, random.randint(0,width-1)
    gx = random.randint(0, width-1)
    fill_ratio = random.uniform(0, 0.3)
    if gx == 0 or gx == width-1:
        gy = random.randint(0, height-1)
    else:
        gy = random.choice([0, height-1])
    
    print(sy,sx,gy,gx)

    pc = CreateRoute(width, height, (sy,sx), (gy,gx))
    
    pretime = time.time()
    dp1 = pc.create_dp()
    dp1 = pc.dp_forward(dp1)
    dp2 = pc.dp_backward(dp1, fill_ratio)
    route = pc.find_route_by_bitmemo_dfs(dp2)
    result_route_map = pc.reformat_map(route)
    for row in result_route_map:
        print(row)
    pole_area = pc.create_pole_arrangement(result_route_map)
    newtime = time.time()

    # for row in result_route_map:
    #     print(row)
    for row in pole_area:
        for i in row:
            print(str(i).rjust(4), end="")
        print("")
    print("実行時間：", newtime-pretime)

if __name__ == "__main__":
    main()

