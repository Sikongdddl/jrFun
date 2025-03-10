# 探索先手必胜问题
# 1vs1局面：player_hands = 1, opponent_hands = 1
import numpy as np
class HandGame:
    def __init__(self,player_hands,opponent_hands):
        self.player_hands = player_hands
        self.opponent_hands = opponent_hands
        self.hands = [player_hands,opponent_hands]
        self.current_player = 1 #0 means player, 1 means opponent
        self.current_round = 0 #round50 means draw

    def is_game_over(self):
        """判断游戏是否结束"""
        return self.hands[0] == 0 or self.hands[1] == 0
    
    def take_action(self):
        self.current_round += 1
        if self.current_player == 0:
            self.hands[0] = (self.hands[0] + self.hands[1]) % 10
        else:
            self.hands[1] = (self.hands[0] + self.hands[1]) % 10
        self.current_player = 1 - self.current_player 

    def display(self):
        print(f"玩家1: {self.hands[0]}")
        print(f"玩家2: {self.hands[1]}")

states = np.zeros((10,10))
#1 means player wins, -1 means opponent wins, 0 means draw
for i in range(10):
    for j in range(10):
        game = HandGame(i,j)
        while not game.is_game_over():
            game.take_action()
            if i == 2 and j == 6:
                game.display()
            if game.current_round == 100:
                break
        if game.hands[0] == 0:
            states[i,j] = 1
        elif game.hands[1] == 0:
            states[i,j] = -1
        else:
            states[i,j] = 0
print(states)
# 1vs1的全部启示局面和终局情况如下（player先手时）
# 值得注意的是：这个游戏并不是对称的 同样的起始局面下player先手与后手的结果并不相同
# 这可以从这个矩阵不是对称矩阵看出
#  [ 1.  1.  1.  1.  1.  1.  1.  1.  1.  1.]
#  [-1.  1. -1.  0. -1. -1.  1.  1.  0.  1.]
#  [-1.  0.  1.  1. -1.  1.  0. -1.  1. -1.]
#  [-1.  1. -1.  1.  0. -1. -1.  1.  1.  0.]
#  [-1.  1.  0. -1.  1.  1.  1.  0. -1. -1.]
#  [-1. -1.  1. -1.  1.  1.  1. -1.  1. -1.]
#  [-1. -1. -1.  0.  1.  1.  1. -1.  0.  1.]
#  [-1.  0.  1.  1. -1. -1.  0.  1. -1.  1.]
#  [-1. -1.  1. -1.  0.  1. -1.  1.  1.  0.]
#  [-1.  1.  0.  1.  1. -1. -1.  0. -1.  1.]

# 当player后手时，矩阵如下
#  [ 1.  1.  1.  1.  1.  1.  1.  1.  1.  1.]
#  [-1. -1.  0. -1. -1.  1.  1.  0.  1. -1.]
#  [-1.  1. -1.  1.  0. -1.  1. -1. -1.  0.]
#  [-1.  0. -1. -1.  1.  1.  0. -1.  1. -1.]
#  [-1.  1.  1.  0. -1. -1. -1.  1.  0. -1.]
#  [-1.  1. -1.  1. -1. -1. -1.  1. -1.  1.]
#  [-1. -1.  0.  1. -1. -1. -1.  0.  1.  1.]
#  [-1. -1.  1. -1.  0.  1.  1. -1. -1.  0.]
#  [-1.  0. -1. -1.  1. -1.  0.  1. -1.  1.]
#  [-1. -1.  1.  0.  1.  1. -1. -1.  0. -1.]

