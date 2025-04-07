# 探索先手必胜问题
# 1vs1局面：player_hands = 1, opponent_hands = 1
# 2vs1局面：必胜条件为进入1vs1局面的必胜起始状态:player_hands = [1,1], opponent_hands = [1,0]
# 在蒙特卡洛采样模拟下得到了每个起始状态的value function 没有发现稳定为1的状态 所有稳定为-1的状态也都是平凡解 由此可以得出结论：
# 2vs1局面不存在必胜起始条件 因此2vs2也不存在必胜起始条件 而value function有助于2vs2局面下的决策（如果能进入一个好的2vs1局面就进入，否则不进入）
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
    states = np.zeros((9,9))
    #1 means player wins, -1 means opponent wins, 0 means draw
    for i in range(1,10):
        for j in range(1,10):
            game = HandGame11(i,j,0)
            while not game.is_game_over():
                game.take_action()
                if game.current_round == 100:
                    break
            if game.hands[0] == 0:
                states[i-1,j-1] = 1
            elif game.hands[1] == 0:
                states[i-1,j-1] = -1
            else:
                states[i-1,j-1] = 0
    return states

def get2versus1StatusEntry(status_11,status_21,i,j,k):
    #1 means player wins, -1 means opponent wins, 0 means draw 
    game = HandGame21([i,j],[k],0)
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
    #at this step, opponent win
    if(game.opponent_hand == 0):
        ret = -1
        status_21[i-1][j-1][k-1] += ret
        return status_21
    
    remained_hand = 0
    # find end status:
    if game.player_left_hand != 0 and game.player_right_hand != 0:
        #draw
        if game.opponent_hand != 0:
            #print("draw and fuck you")
            ret = 0
        #opponent win
        else:
            #print("opponent win you idiot!")
            ret = -1
        status_21[i-1][j-1][k-1] += ret
        return status_21

    elif game.player_left_hand == 0:
        remained_hand = game.player_right_hand
    else:
        remained_hand = game.player_left_hand
    
    #print(game.player_left_hand,game.player_right_hand,game.opponent_hand)
    #print(status_11[remained_hand][game.opponent_hand])
    
    ret = status_11[remained_hand-1][game.opponent_hand-1]
    status_21[i-1][j-1][k-1] += ret
    return status_21

def get2versus1Status():
    sum = 0
    num_epoch = 10000
    status_11 = get1versus1Status()
    status_21 = np.zeros((9,9,9))
    for i in range(1,10):
        print("i=",i)
        for j in range(1,10):
            for k in range(1,10):
                for epoch in range(num_epoch):
                    status_21 = get2versus1StatusEntry(status_11,status_21,i,j,k)
    
    status_21 = status_21 / num_epoch
    for i in range(status_21.shape[2]):
        slice_data = status_21[:,:,i]
        np.savetxt(f"./log/opponent_{i+1}.txt",slice_data,fmt='%.6f',delimiter="\t")

if __name__ == "__main__":
    print("hello,world!")