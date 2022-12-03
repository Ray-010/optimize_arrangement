import random
from collections import deque


class PathCreationBFS:
    def __init__(self, width, height, sy, sx, gy, gx) -> None:
        self.area_width = width
        self.area_height = height
        self.start = [sy, sx]
        self.goal = [gy, gx]

        # 経路マップ
        self.area = [[-1]*self.area_width for _ in range(self.area_height)]
        # 探索済み座標のメモ
        self.visualize_area = [["."]*self.area_width for _ in range(self.area_height)]
        # ポール座標・経路・ベルト接続を含んだ拡張マップ
        self.pole_area = [[" " for _ in range(self.area_width*2+1)] for _ in range(self.area_height*2+1)]

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
            if LR == "right":
                if self.goal[0] <= step:
                    break
                y, x = step, self.area_width-1

                tmp.append([y, x])
                LR = "left"
            elif LR == "left":
                if self.goal[0] <= step:
                    break
                y, x = step, 0
                
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
    def create_obstacle(self, num) -> None:
        obstacles = []
        for _ in range(num):
            y, x = random.randrange(self.area_height), random.randrange(self.area_width)
            if y == self.start[0] and x == self.start[1]:
                continue
            if y == self.goal[0] and x == self.goal[1]:
                continue
            obstacles.append([y, x])
            self.visualize_area[y][x] = "#"
            
        print("Obstacles: ", *obstacles)