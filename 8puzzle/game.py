from copy import deepcopy
from functools import partial

from search import BfsMixin, AStar

class Puzzle8(BfsMixin, AStar):
    
    move2coord = {"Up":(-1,0),
                  "Down":(1,0),
                  "Right":(0,1),
                  "Left":(0,-1)}
            
    def __init__(self, si, s_goal):
        self.si = (si,[])
        self.s_goal = s_goal

    def pos(self, mv):
        return self.move2coord[mv]
    
    def find_num(self, num, s):

        for ir, row in enumerate(s):
            for ic, elem in enumerate(row):
                if elem == num: return ir, ic

    def find_zero(self, s):
        return self.find_num(0,s)

    def is_bound(self, pos):
        x, y = pos
        if 0<=x<=2 and 0<=y<=2: return True
        return False

    def add_tuple(self, t1, t2):
        return tuple(i+j for i, j in zip(t1, t2))

    def swap(self, new, actual, s):
        nx, ny = new
        ax, ay = actual
        s[ax][ay], s[nx][ny] = s[nx][ny], s[ax][ay]
        return s

    def is_goal(self, si):
        s, t = si
        if s == self.s_goal: return True
        return False

    def __move(self, direc, st):
        s, t = st
        zero_pos = self.find_zero(s)
        new_zero_pos = self.add_tuple(zero_pos, self.pos(direc))

        new_s = "stop"

        if self.is_bound(new_zero_pos):
            new_s = deepcopy(s)
            new_s = self.swap(zero_pos, new_zero_pos, new_s)
            
        return (new_s, t + [direc])

    def moves(self, sts):
        
        return list(filter(lambda x: x[0] != "stop", 
                           [self.__move(direc, st) for st in sts 
                                                   for direc in self.move2coord.keys()]))
    
    def is_feasible(self,x):
        return True
    
    def bfs(self):
        return BfsMixin.bfs(self.si, self.is_goal, self.is_feasible, self.moves)
    
    def abs_diff(self, x, y):
        return (abs(x[0]-y[0]), abs(x[1]-y[1]))

    def dist(self, v, x, y):
        return sum(self.abs_diff(self.find_num(v,x), self.find_num(v,y)))

    def f1(self, st):
        s, t = st
        return len(t) + sum([self.dist(v, s, self.s_goal) for v in range(1,9)])
    
    def f2(self, st):
        s, t = st
        return len(t) + sum([s[i][j] != self.s_goal[i][j] 
                            for i in range(3) 
                            for j in range(3) ]) - 1
    
    def astar(self, heuristic):
        if "manhattan" == heuristic:
            return AStar.astar(self.si, self.f1, self.is_goal, self.moves)
            
        elif "soma" == heuristic:
            return AStar.astar(self.si, self.f2, self.is_goal, self.moves)