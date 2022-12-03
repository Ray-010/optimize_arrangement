import time
import sys
from create_route import CreateRoute
sys.setrecursionlimit(10000000)


def main():
    width = 8
    height = 8
    sy, sx = 0, 0
    gy, gx = 0, width-1
    pc = CreateRoute(width, height, (sy,sx), (gy,gx))
    
    pretime = time.time()
    dp1 = pc.create_dp()
    dp1 = pc.dp_forward(dp1)
    dp2 = pc.dp_backward(dp1)
    route = pc.find_route(dp2)
    result_route_map = pc.reformat_map(route)
    
    pole_area = pc.create_pole_arrangement(result_route_map)
    newtime = time.time()

    for row in result_route_map:
        print(row)
    for row in pole_area:
        for i in row:
            print(str(i).rjust(4), end="")
        print("")
    print("実行時間：", newtime-pretime)

if __name__ == "__main__":
    main()

