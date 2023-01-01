import random
import time
import numpy as np
from BeltCreation import BeltCreation


# TODO: 2次元配列処理をnumpy配列にして高速化する
# TODO: 障害物対応

def main():
    height, width = random.randint(2, 5), random.randint(2, 5)
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
    pole_route = BeltCreation(width, height, sy, sx, gy, gx)
    
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
