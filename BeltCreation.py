import random
from PathCreation import PathCreation
from collections import deque


class BeltCreation(PathCreation):
    def __init__(self, width, height, start, goal) -> None:
        super().__init__(width, height, start, goal)
        self.width = width
        self.height = height
        self.start = start
        self.goal = goal

        # ポール座標・経路・ベルト接続を含んだ拡張マップ
        self.pole_area = [[" " for _ in range(self.width*2+1)] for _ in range(self.height*2+1)]

    # ポール座標生成
    def create_pole_coordinates(self, route) -> list:
        poles = []
        idx = 0
        for i in range(self.height):
            for j in range(self.width):
                if route[i][j] == -1: continue # 未探索

                i2 = i*2+1
                j2 = j*2+1
                # 斜め四方: ポール配置
                for i3, j3 in [[i2-1, j2-1],[i2-1, j2+1],[i2+1, j2-1],[i2+1, j2+1]]:
                    if self.pole_area[i3][j3] != " ": continue
                    self.pole_area[i3][j3] = idx
                    poles.append([i3, j3])
                    idx += 1
        return poles

    # ポール配置・接続情報を含めたマップ生成
    def create_pole_arrangement(self, route) -> list:
        # ポール座標生成
        self.pole_c = self.create_pole_coordinates(route)

        """
        i, j: 経路マップでの経路の座標
        i2, j2: 拡張マップでの経路の座標
        """
        for i in range(self.height):
            for j in range(self.width):
                if route[i][j] == -1: continue # 未探索
                i2 = i*2+1
                j2 = j*2+1
                # 経路マップで隣接する座標の方向を保存
                # neighbor_dir = [start_c, goal_c]
                neighbor_dir = []
                for y, x in [[i+1, j], [i, j+1], [i-1, j], [i, j-1]]:
                    # マップ範囲外、または未探索の座標を飛ばす
                    if not (0 <= y < self.height and 0 <= x < self.width): continue
                    if route[y][x] == -1: continue
                    if abs(route[y][x] - route[i][j]) == 1:
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
        # スタート・ゴールの出口方向の=を削除
        sy, sx = self.start[0]*2, self.start[1]*2+1
        if self.goal[0] == 0: # 上
            gy, gx = self.goal[0]*2, self.goal[1]*2+1
        elif self.goal[0] == self.height-1: # 下
            gy, gx = self.goal[0]*2+2, self.goal[1]*2+1
        elif self.goal[1] == 0: # 左
            gy, gx = self.goal[0]*2+1, self.goal[1]*2
        elif self.goal[1] == self.width-1: # 右
            gy, gx = self.goal[0]*2+1, self.goal[1]*2+2
        self.pole_area[sy][sx] = " "
        self.pole_area[gy][gx] = " "

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

        return self.pole_area

    # 接続情報生成に使う隣接リスト生成
    def create_adjacency_list(self) -> list:
        # 無向グラフの隣接リスト
        adjacency_list = [set() for _ in range(len(self.pole_c))]
        ex_width = self.width*2+1
        ex_height = self.height*2+1
        for idx, (py, px) in enumerate(self.pole_c):
            # 上下方向探索, 上右下左
            direction = [[1, 0], [0, 1], [-1, 0], [0, -1]]
            for i, j in direction:
                y, x = py+i, px+j
                # 範囲外は無視
                if not (0 <= y < ex_height and 0 <= x < ex_width): continue
                if self.pole_area[y][x] == "=":
                    pole_idx = self.pole_area[py+i*2][px+j*2]
                    adjacency_list[idx].add(pole_idx)
                    adjacency_list[pole_idx].add(idx)
                    
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
                if not (len(self.pole_c[i]) <= 2): continue # 既に方向決定済を飛ばす
                # 接続方向, iとpの差分で決める
                py, px = self.pole_c[p][0], self.pole_c[p][1]
                ny, nx = self.pole_c[i]
                y = (py-ny)//2
                x = (px-nx)//2
                self.pole_c[i].append([y, x])

                done_p.add(i)
                Q.append(i)
            
    def show_pole_way(self):
        way = ["↑", "↓", "→", "←"]
        direction = ""
        for pole in self.pole_c:
            if len(pole) <= 2: continue
            y, x = pole[0], pole[1]
            wy, wx = pole[2]

            if wy == -1: # 上
                direction = way[0]
            elif wy == 1: # 下 
                direction = way[1]
            elif wx == 1: # 右
                direction = way[2]
            elif wx == -1: # 左
                direction = way[3]

            self.pole_area[y+wy][x+wx] = direction
