from bisect import bisect
from copy import deepcopy
from collections import deque

class BfsMixin:
    
    @classmethod
    def bfs(cls, si, is_goal, is_feasible, moves):
        
        explore_sts = deepcopy([si])

        goal = list(filter(is_goal, explore_sts))
        n = 0
        
        while len(goal) == 0:
            explore_sts = list(filter(is_feasible, moves(explore_sts)))
            goal = list(filter(is_goal, explore_sts))
            n += len(explore_sts)
        return goal[0], n
    
class AStar:

    @classmethod   
    def astar(cls, si, f, is_goal, moves):

        sts = deepcopy([si])

        goal = list(filter(is_goal, sts))  
        n = 0
        explore_sts = []
        explore_fs = []
        while len(goal) == 0:

            for f_val, st in zip(map(f, sts), sts):
                idx = bisect(explore_fs, f_val)
                explore_sts.insert(idx, st)  # insert in the corret position
                explore_fs.insert(idx, f_val)  # insert in the corret position

            s = explore_sts.pop(0)
            _ = explore_fs.pop(0)
            sts = moves([s])

            goal = list(filter(is_goal, sts))    
            n += len(sts)   

        return goal[0], n