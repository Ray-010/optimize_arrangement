import random
from collections import deque


class CreateRoute():
    def __init__(self, width, height, sy, sx, gy, gx) -> None:
        self.area_width = width
        self.area_height = height
        self.start = [sy, sx]
        self.goal = [gy, gx]
        self.area = [[-1]*self.area_width for _ in range(self.area_height)]
        # 探索済み座標のメモ
        self.visualize_area = [["."]*self.area_width for _ in range(self.area_height)]
    
    def bfs_shortest_distance(self, start: list, goal:list) -> None:
        sy, sx = start
        gy, gx = goal
        Q = deque()
        Q.append((sy, sx))
        ok = False
        if self.area[sy][sx] == -1:
            self.area[sy][sx] = 0
        while len(Q) > 0:
            y1, x1 = Q.popleft()
            # obstacle_cnt = 0
            for y2, x2 in [[y1+1, x1], [y1, x1+1], [y1-1, x1], [y1, x1-1]]:
                # エリア範囲を超えるものを無視
                if not (0 <= y2 < self.area_height and 0 <= x2 < self.area_width):
                    continue
                if self.visualize_area[y2][x2] == "#":
                    continue

                # 未探索座標を更新
                if self.area[y2][x2] == -1:
                    self.area[y2][x2] = self.area[y1][x1]+1
                    # ゴール座標についたら終了
                    if y2 == gy and x2 == gx:
                        ok = True
                        break
                    Q.append((y2, x2))
            if ok:
                break
    
    def make_passing_point(self, congestion_rate):
        passing_point_num = self.area_height
        if congestion_rate == 1:
            step_size = 1
        elif congestion_rate == 2:
            step_size = 2
        elif congestion_rate == 3:
            step_size = 3
        
        tmp = []
        step = self.start[0] # y座標
        LR = "right"
        tmp.append(self.start)

        for i in range(passing_point_num):
            # if "#" in self.visualize_area[i] and not congestion_rate==3:
            #     step += 2
            # else:
            
            if LR == "right":
                if self.goal[0] <= step:
                    break
                y, x = step, self.area_width-1
                
                # 障害物に当たるかを確認
                # if self.visualize_area[y][x] == "#":
                #     for x2 in range(x, 0, -1):
                #         if not (self.visualize_area[y][x2] == "#" or self.visualize_area[y+1][x2] == "#"):
                #             x = x2
                #             break

                tmp.append([y, x])
                LR = "left"
            elif LR == "left":
                if self.goal[0] <= step:
                    break
                y, x = step, 0
                # 障害物に当たるかを確認
                # if self.visualize_area[y][x] == "#":
                #     for x2 in range(1, self.area_width-1):
                #         if not (self.visualize_area[y][x2] == "#" or self.visualize_area[y+1][x2] == "#"):
                #             x = x2
                #             break
                
                tmp.append([y, x])
                LR = "right"
            
            step += step_size
        
        tmp.append(self.goal)
        print("Passing Points: ", *tmp)
        print("The Number of Passing Points: ", len(tmp)-2)
        passing_points = []
        for i in range(len(tmp)-1):
            passing_points.append([tmp[i], tmp[i+1]])
        return passing_points
    
    # 経路復元と確定経路以外をリセット
    def reset_map(self, start, goal):
        sy, sx = start
        check_point = goal
        score = self.area[goal[0]][goal[1]]
        # ゴール座標を探索済みにする
        self.visualize_area[goal[0]][goal[1]] = "#"

        while True:
            y1, x1 = check_point
            if y1 == sy and x1 == sx:
                break
            if score == 0:
                break

            #TODO: 探索優先順位を条件によって変える必要があるかも
            for y2, x2 in [[y1-1, x1], [y1, x1+1], [y1, x1-1], [y1+1, x1]]:
                # エリア範囲を超えるものを無視
                if not (0 <= y2 < self.area_height and 0 <= x2 < self.area_width):
                    continue
                
                # 隣接する座標の差分が1になれば探索済みにする
                if score - self.area[y2][x2] == 1:
                    self.visualize_area[y2][x2] = "#"
                    check_point = [y2, x2]
                    score -=1
                    break
        
        # 未確定座標を未探索-1にリセット
        for y in range(self.area_height):
            for x in range(self.area_width):
                if self.visualize_area[y][x] == "#":continue
                self.area[y][x] = -1
        
    # 障害物生成
    def create_obstacle(self, num):
        tmp = []
        for _ in range(num):
            y, x = random.randrange(self.area_height), random.randrange(self.area_width)
            if y == self.start[0] and x == self.start[1]:
                continue
            if y == self.goal[0] and x == self.goal[1]:
                continue
            tmp.append([y, x])
            self.visualize_area[y][x] = "#"
            
        print("Obstacles: ", *tmp)

    def create_pole_arrangement(self) -> list:
        width = self.area_width*2+1
        height = self.area_height*2+1
        pole_area = [[" " for _ in range(width)] for _ in range(height)]

        tmp = []
        
        for i in range(self.area_height):
            for j in range(self.area_width):
                if self.area[i][j] != -1:
                    i2 = i*2+1
                    j2 = j*2+1
                    pole_area[i2][j2] = self.area[i][j]
                    
                    # 次の座標の方向を保存
                    neighbor_dir = []
                    for y, x in [[i+1, j], [i, j+1], [i-1, j], [i, j-1]]:
                        if not (0 <= y < self.area_height and 0 <= x < self.area_width): continue
                        if self.area[y][x] == -1: continue
                        if abs(self.area[y][x] - self.area[i][j]) == 1:
                            neighbor_dir.append([i2+(y-i), j2+(x-j)])
                    # 斜め四方: ポール配置
                    for i3, j3 in [[i2-1, j2-1],[i2-1, j2+1],[i2+1, j2-1],[i2+1, j2+1]]:
                        if pole_area[i3][j3] == "O": continue
                        pole_area[i3][j3] = "O"
                        tmp.append([i3, j3])

                    # 縦: ベルト接続
                    flag = True
                    for i3, j3 in [[i2, j2+1], [i2, j2-1]]:
                        for ny, nx in neighbor_dir:
                            if ny == i3 and nx == j3:
                                pole_area[i3][j3] = " "
                                flag = False
                        if flag:
                            if pole_area[i3][j3] == "|": continue
                            pole_area[i3][j3] = "|"
                        flag = True
                    flag = True
                    # 横: ベルト接続
                    for i3, j3 in [[i2+1, j2], [i2-1, j2]]:
                        for ny, nx in neighbor_dir:
                            if ny == i3 and nx == j3:
                                pole_area[i3][j3] = " "
                                flag = False
                        if flag:
                            if pole_area[i3][j3] == "-": continue
                            pole_area[i3][j3] = "-"
                        flag = True

        # print("pole coordinates: ", *tmp)
        
        return pole_area
