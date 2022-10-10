import random
import time
import numpy as np
from create_route import CreateRoute


# TODO: 2次元配列処理をnumpy配列にして高速化する
# TODO: 障害物対応

def main():
    height, width = random.randint(5, 10), random.randint(5, 10)
    sy, sx = 0, random.randint(0, width-1)
    gy, gx = height-1, random.randint(sx, width-1)
    print("Map Size: ", "Height", height, "Width", width)
    print("start:", "sy", sy, "sx", sx)
    print("goal:", "gy", gy, "gx", gx)
    print("CongestionRate: 1.busy", "2.normal", "3.few")

    congestion_rate = 2
    congestion_rate = int(input("Please Input Congestion Rate: "))
    if congestion_rate not in set([1, 2, 3]):
        print("Please input Congestion Rate within 1 to 3")
        return
    
    pre = time.time()

    pole_route = CreateRoute(width, height, sy, sx, gy, gx)
    # 障害物生成
    # pole_route.create_obstacle(5)
    # 経過点生成
    passing_points = pole_route.make_passing_point(congestion_rate)
    
    for path in passing_points:
        start, goal = path
        # 幅優先探索
        pole_route.bfs_shortest_distance(start, goal)
        # 経路復元と確定経路以外を一度リセット
        pole_route.reset_map(start, goal)

    print("Map Route ###########################################################")
    route_only = np.array(pole_route.area)
    print(route_only)

    print("Pole Arrangement ###########################################################")
    pole_route.create_pole_arrangement()
    for row in pole_route.pole_area:
        for i in row:
            print(str(i).rjust(4), end="")
        print("")
    
    now = time.time()
    print("実行時間: ", now-pre)

if __name__ == "__main__":
    main()
