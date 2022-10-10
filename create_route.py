import random
from collections import deque


class CreateRoute():
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

    # ポール座標生成
    def create_pole_coordinates(self) -> list:
        poles = []
        idx = 0
        for i in range(self.area_height):
            for j in range(self.area_width):
                # 未探索なら
                if self.area[i][j] != -1:
                    i2 = i*2+1
                    j2 = j*2+1
                    # 斜め四方: ポール配置
                    for i3, j3 in [[i2-1, j2-1],[i2-1, j2+1],[i2+1, j2-1],[i2+1, j2+1]]:
                        if self.pole_area[i3][j3] != " ": continue
                        self.pole_area[i3][j3] = idx
                        poles.append([i3, j3])
                        idx += 1
        return poles

    def create_pole_arrangement(self) -> list:
        # ポール座標生成
        self.pole_c = self.create_pole_coordinates()

        # 拡張マップのスタート座標とゴール座標
        start_c = [self.start[0]*2, self.start[1]*2+1]
        goal_c = [self.goal[0]*2+2, self.goal[1]*2+1]
        
        for i in range(self.area_height):
            for j in range(self.area_width):
                # 未探索なら
                if self.area[i][j] != -1:
                    i2 = i*2+1
                    j2 = j*2+1

                    """
                    i, j: 経路マップの座標
                    i2, j2: 拡張マップの座標
                    """
                    
                    # 経路マップで隣接する座標の方向を保存
                    neighbor_dir = [start_c, goal_c]
                    for y, x in [[i+1, j], [i, j+1], [i-1, j], [i, j-1]]:
                        # マップ範囲外、または未探索の座標を飛ばす
                        if not (0 <= y < self.area_height and 0 <= x < self.area_width): continue
                        if self.area[y][x] == -1: continue
                        
                        if abs(self.area[y][x] - self.area[i][j]) == 1:
                            neighbor_dir.append([i2+(y-i), j2+(x-j)])

                    # 縦横: ベルト
                    flag = True
                    # 右, 左, 上, 下
                    for i3, j3 in [[i2, j2+1], [i2, j2-1], [i2+1, j2], [i2-1, j2]]:
                        # 隣の座標かどうかを判定
                        for ny, nx in neighbor_dir:
                            if ny == i3 and nx == j3:
                                flag = False
                                break
                        if flag:
                            if self.pole_area[i3][j3] == "=": continue
                            self.pole_area[i3][j3] = "="
                        flag = True

        # 無向グラフの隣接リスト    
        adjacency_list = self.create_adjacency_list()
        # 開始位置
        sy1, sx1 = self.start[0]*2, self.start[1]*2
        sy2, sx2 = self.start[0]*2, self.start[1]*2+2
        pole_num1 = self.pole_area[sy1][sx1]
        pole_num2 = self.pole_area[sy2][sx2]

        self.create_belt_way(pole_num1, adjacency_list)
        self.create_belt_way(pole_num2, adjacency_list)

        self.show_pole_way()

    def create_adjacency_list(self) -> list:
        # 無向グラフの隣接リスト
        adjacency_list = [set() for _ in range(len(self.pole_c))]
        width = self.area_width*2+1
        height = self.area_height*2+1

        for idx, (py, px) in enumerate(self.pole_c):
            # 上下方向探索, 上右下左
            tmp = [[1, 0], [0, 1], [-1, 0], [0, -1]]
            for i, j in tmp:
                y, x = py+i, px+j
                # 範囲外は無視
                if not (0 <= y < height and 0 <= x < width): continue

                if self.pole_area[y][x] == "=":
                    pole_idx = self.pole_area[py+i*2][px+j*2]
                    adjacency_list[idx].add(pole_idx)
                    adjacency_list[pole_idx].add(idx)
                    
        # print("Adjacency list", *adjacency_list)
        return adjacency_list

    def create_belt_way(self, p_num:int, adjacency_list:list) -> None:
        Q = deque([p_num])
        done_p = set([p_num])
        while len(Q) > 0:
            p = Q.popleft()
            next_p_num = adjacency_list[p]

            for i in next_p_num:
                # i: 次の座標, p: 前の座標
                if i in done_p: continue
                # 接続方向, iとpの差分で決める
                py, px = self.pole_c[p][0], self.pole_c[p][1]
                iy, ix = self.pole_c[i]
                y = (py-iy)//2
                x = (px-ix)//2
                self.pole_c[i].append([y, x])

                done_p.add(i)
                Q.append(i)
            
    def show_pole_way(self):
        way = ["↑", "↓", "→", "←"]
        tmp = ""
        for pole in self.pole_c:
            if len(pole) <= 2: continue
            y, x = pole[0], pole[1]
            wy, wx = pole[2]

            if wy == -1: # 上
                tmp = way[0]
            elif wy == 1: # 下 
                tmp = way[1]
            elif wx == 1: # 右
                tmp = way[2]
            elif wx == -1: # 左
                tmp = way[3]

            self.pole_area[y+wy][x+wx] = tmp
