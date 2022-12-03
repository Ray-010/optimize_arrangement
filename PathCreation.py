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

        self.cnt = 0
    
    def create_map_and_adjacency_list(self):
        self.G = [[i for i in range(j*self.width, self.width+j*self.width)] for j in range(self.height)]
        self.adjacency_list = [[] for _ in range(self.height*self.width)]
        for i in range(self.height):
            for j in range(self.width):
                idx = self.G[i][j]
                for i2, j2 in [[i+1, j],[i-1, j],[i, j+1],[i, j-1]]:
                    if not(0<=i2<self.height and 0<=j2<self.width): continue
                    self.adjacency_list[idx].append(self.G[i2][j2])
    
    def create_dp(self):
        dp = [[[] for _ in range(self.element_num)] for _ in range(self.operation_num)]
        return dp
            
    def dp_forward(self, dp):
        dp[0][self.start_num] = [-1] # 番兵
        for i in self.adjacency_list[self.start_num]:
            dp[1][i].append(self.start_num)
        
        for i in range(self.operation_num):
            for j in range(self.element_num):
                if j == self.start_num: continue
                if not dp[i-1][j]: continue # 空
                for el in self.adjacency_list[j]:
                    if j in dp[i][el]: continue
                    dp[i][el].append(j)
        return dp
    
    def dp_backward(self, dp1):
        dp2 = self.create_dp()
        self.operation = -1
        for i in range(self.operation_num-1, -1, -1):
            if dp1[i][self.goal_num]:
                self.operation = i
                break
        if self.operation == -1: return None

        dp2[self.operation][self.goal_num] = [-1] # 番兵
        for i in self.adjacency_list[self.goal_num]:
            dp2[self.operation-1][i].append(self.goal_num)

        for i in range(self.operation, 0, -1):
            for j in range(self.element_num):
                if not dp2[i][j]: continue # 空
                if j == self.goal_num: continue
                
                for el in dp1[i][j]:
                    # TODO: 到達不可をここで判定
                    if j in dp2[i][el]: continue
                    dp2[i-1][el].append(j)
        return dp2

    
    def find_route(self, dp):
        memo = [[] for _ in range(self.operation_num)]
        def dfs(route, y, x):
            # if set(route) in memo[y]:
            #     self.cnt += 1
            #     return route[:-1]
                
            if -1 in dp[y][x]:
                route.append(-1)
                return route

            for i in dp[y][x]:
                if route[-1] == -1: return route
                if i in route: continue
                route = dfs(route+[i], y+1, i)

            if route[-1] != -1:
                # if set(route[:-1]) not in memo[y]: memo[y].append(set(route[:-1]))
                return route[:-1]
            
            return route

        route = dfs([self.start_num], 0, self.start_num)
        # for row in memo:
        #     print(row)
        print(self.cnt)
        return route[:-1]
    
    def reformat_map(self, route):
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