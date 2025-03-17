# 探索先手必胜问题
# 1vs1局面：player_hands = 1, opponent_hands = 1
# 2vs1局面：必胜条件为进入1vs1局面的必胜起始状态:player_hands = [1,1], opponent_hands = [1,0]
import numpy as np
class HandGame11:
    def __init__(self,player_hands,opponent_hands,current_player):
        self.player_hands = player_hands
        self.opponent_hands = opponent_hands
        self.hands = [player_hands,opponent_hands]
        self.current_player = current_player #0 means player, 1 means opponent
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

class HandGame21:
    def __init__(self,player_hands,opponent_hands,current_player):
        self.player_left_hand = player_hands[0]
        self.player_right_hand = player_hands[1]
        self.opponent_hand = opponent_hands[0]
        self.current_player = current_player
        self.current_round = 0

    def is_game_over(self):
        return self.player_left_hand == 0 or self.player_right_hand == 0 or self.opponent_hand == 0

    def take_action(self):
        self.current_round += 1
        #player take action randomly from left hand or right hand
        if self.player_left_hand == 0:
            from_hand = 1
        elif self.player_right_hand == 0:
            from_hand = 0
        else:
            from_hand = np.random.choice([0,1])
        
        if from_hand == 0:
            if self.current_player == 0:
                self.player_left_hand += self.opponent_hand
                self.player_left_hand %= 10
            else:
                self.opponent_hand += self.player_left_hand
                self.opponent_hand %= 10
        else:
            if self.current_player == 0:
                self.player_right_hand += self.opponent_hand
                self.player_right_hand %= 10
            else:
                self.opponent_hand += self.player_right_hand
                self.opponent_hand %= 10
        self.current_player = 1 - self.current_player
                
    
    def display(self):
        print(f"玩家1: 左({self.player_left_hand}) 右({self.player_right_hand})")
        print(f"玩家2: {self.opponent_hand}")



def get1versus1Status():
    states = np.zeros((10,10))
    #1 means player wins, -1 means opponent wins, 0 means draw
    for i in range(10):
        for j in range(10):
            game = HandGame11(i,j,0)
            while not game.is_game_over():
                game.take_action()
                if game.current_round == 100:
                    break
            if game.hands[0] == 0:
                states[i,j] = 1
            elif game.hands[1] == 0:
                states[i,j] = -1
            else:
                states[i,j] = 0
    return states

def get2versus1Status():
    status_21 = np.zeros((10,10,10))
    #1 means player wins, -1 means opponent wins, 0 means draw
    status_11 = get1versus1Status()
    game = HandGame21([1,1],[1],0)
    while not game.is_game_over():
        game.take_action()
        if game.current_round == 1000:
            break
    # end by three modes: player win, opponent win, draw
    # player win: turn to 1vs1 status(must be player move first so add a robust check)
    # opponent win: very bad situations (2vs0), not implemented
    # draw: 2vs1 draw then quit, 1vs1 draw won't happen cause the stop conditions
    
    # robust check
    if game.current_player == 1:
        game.take_action()
    
    remained_hand = 0
    # find end status:
    if game.player_left_hand != 0 and game.player_right_hand != 0:
        #draw
        if game.opponent_hand != 0:
            #print("draw and fuck you")
            return 0
        #opponent win
        else:
            #print("opponent win you idiot!")
            return -1
    
    elif game.player_left_hand == 0:
        remained_hand = game.player_right_hand
    else:
        remained_hand = game.player_left_hand
    
    #print(game.player_left_hand,game.player_right_hand,game.opponent_hand)
    #print(status_11[remained_hand][game.opponent_hand])
    return status_11[remained_hand][game.opponent_hand]

if __name__ == "__main__":
    sum = 0
    for i in range (1000):
        cur_status = get2versus1Status()
        sum += cur_status
    print(sum)

'''
# 1vs1的全部起始局面和终局情况如下（player先手时）
# 值得注意的是：这个游戏并不是对称的 同样的起始局面下player先手与后手的结果并不相同
# 这可以从这个矩阵不是对称矩阵看出
# 上次没有发现的2684trajectory其实在mod5时也是2134 只有这一个起始序列会导致问题
# chopsticks游戏真是其乐无穷
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
'''
