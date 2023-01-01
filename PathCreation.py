import sys
from collections import deque
sys.setrecursionlimit(10000000)


class PathCreation:
    def __init__(self, width, height, start, goal) -> None:
        self.width = width
        self.height = height
        
        self.element_num = self.height*self.width
        self.operation_num = self.element_num

        self.start = start
        self.goal = goal
        self.create_map_and_adjacency_list()
        self.start_num = self.G[start[0]][start[1]]
        self.goal_num = self.G[goal[0]][goal[1]]
        self.create_bfs_map()

        self.cnt = 0
    
    def create_map_and_adjacency_list(self): # 隣接リストの作成
        self.G = [[i for i in range(j*self.width, self.width+j*self.width)] for j in range(self.height)]
        self.adjacency_list = [[] for _ in range(self.height*self.width)]
        for i in range(self.height):
            for j in range(self.width):
                idx = self.G[i][j]
                for i2, j2 in [[i+1, j],[i-1, j],[i, j+1],[i, j-1]]:
                    if not(0<=i2<self.height and 0<=j2<self.width): continue
                    self.adjacency_list[idx].append(self.G[i2][j2])
    
    def create_bfs_map(self): # BFS到達判定用，マップGの1次元配列
        self.bfs_map = [-1]*(self.element_num)
        self.bfs_map[self.goal_num] = 0
        Q = deque()
        Q.append(self.goal_num)
        while len(Q):
            now = Q.popleft()
            for next in self.adjacency_list[now]:
                if next == self.start_num: continue
                if self.bfs_map[next] == -1:
                    self.bfs_map[next] = self.bfs_map[now]+1
                    Q.append(next)
        
    def check_passable(self, route, y, x) -> bool:
        passable = False
        passable_cnt = 0
        passed_num = set(route[:-1])
        bfs_map = [-1]*(self.element_num)
        bfs_map[self.goal_num] = 0
        Q = deque()
        Q.append(self.goal_num)
        while len(Q):
            now = Q.popleft()
            for next in self.adjacency_list[now]:
                if next in passed_num: continue
                if bfs_map[next] == -1:
                    passable_cnt += 1
                    bfs_map[next] = bfs_map[now]+1
                    Q.append(next)
        
        if bfs_map[x] != -1 and (passable_cnt>=self.actual_operation-y): passable = True
        return passable
    
    def create_dp(self): # dpの2次元配列作成(厳密には3次元配列)
        dp = [[[] for _ in range(self.element_num)] for _ in range(self.operation_num)]
        return dp
        
    def dp_forward(self, dp): # 始点からのdp
        dp[0][self.start_num] = [-1] # 番兵
        for i in self.adjacency_list[self.start_num]:
            dp[1][i].append(self.start_num)
        for i in range(1, self.operation_num-1):
            for j in range(self.element_num):
                if j == self.start_num: continue
                if not dp[i][j]: continue # 空
                for el in self.adjacency_list[j]:
                    if j in dp[i+1][el]: continue
                    if el == self.start_num: continue
                    dp[i+1][el].append(j)
        return dp
    
    def dp_backward(self, dp1, ratio): # 終点からのdp
        dp2 = self.create_dp()
        self.actual_operation = -1
        border = self.element_num*ratio
        cnt = 0
        for i in range(self.operation_num-1, -1, -1):
            if dp1[i][self.goal_num]:
                actual_operation = i
                if cnt >= border: break
            cnt += 1
        if actual_operation == -1: return None

        dp2[actual_operation][self.goal_num] = [-1] # 番兵
        for i in self.adjacency_list[self.goal_num]:
            dp2[actual_operation-1][i].append(self.goal_num)

        for i in range(actual_operation-1, 0, -1):
            for j in range(self.element_num):
                if not dp2[i][j]: continue # 空
                if j == self.goal_num: continue
                for el in dp1[i][j]:
                    # TODO: 到達不可をここで判定
                    if j in dp2[i][el]: continue
                    if el == self.goal_num: continue
                    dp2[i-1][el].append(j)
        return dp2
    
    def find_route_by_bfs_dfs(self, dp): # bfs到達可能判定と再帰関数による経路復元
        def dfs(route, y, x):
            if route[-1] == self.goal_num: return route
            if not self.check_passable(route, y, x):
                route.pop()
                return route
            passed_num = set(route)
            for next in dp[y][x]:
                if next not in set(self.adjacency_list[x]): continue
                if next in passed_num: continue
                route.append(next)
                route = dfs(route, y+1, next)
            
            if route[-1] == self.goal_num: return route
            else:
                route.pop()
                return route
        
        route = dfs([self.start_num], 0, self.start_num)
        return route
    
    def reformat_map(self, route): # 経路マップ生成
        numidx = {}
        for i, num in enumerate(route):
            numidx[num] = i
        for i in range(self.height):
            for j in range(self.width):
                if self.G[i][j] not in numidx:
                    self.G[i][j] = -1
                else:
                    self.G[i][j] = numidx[self.G[i][j]]
        return self.G