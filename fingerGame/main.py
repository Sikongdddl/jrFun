#Todo:
#目前minimaxAI无法必胜人类先手（存在轨迹LL-LL-LR-LL-RL-RL-Rl-Rl-RL-RR先手获胜）
#1.探索有无必胜策略
#2.加入robust：探索到死循环（即陷入斐波那契数列）时提前终止
#3.模拟采样探索有无后手必胜轨迹
#4.实现RL agent
#5.RL agent vs minimax
#6.RL agent vs man
#7.RL agent vs RL agent
#8.可视化 上线测试供游玩
import math

class HandGame:
    def __init__(self):
        self.player_hands = [[1, 1], [1, 1]]  # [P1 左, P1 右], [P2 左, P2 右]
        self.current_player = 0  # 0: 玩家1, 1: 玩家2
    
    def display(self):
        """显示当前游戏状态"""
        print(f"玩家1: 左({self.player_hands[0][0]}) 右({self.player_hands[0][1]})")
        print(f"玩家2: 左({self.player_hands[1][0]}) 右({self.player_hands[1][1]})")
    
    def is_game_over(self):
        """判断游戏是否结束"""
        return sum(self.player_hands[0]) == 0 or sum(self.player_hands[1]) == 0
    
    def get_legal_moves(self):
        """返回所有合法动作 (from_hand, to_hand)"""
        moves = []
        for from_hand in [0, 1]:  # 左手(0) 或 右手(1)
            if self.player_hands[self.current_player][from_hand] == 0:
                continue  # 不能用已经放下的手
            for to_hand in [0, 1]:
                if self.player_hands[1 - self.current_player][to_hand] > 0:
                    moves.append((from_hand, to_hand))
        return moves
    
    def take_action(self, from_hand, to_hand):
        """执行一个玩家的动作"""
        opponent = 1 - self.current_player
        
        # 获取当前玩家的手指数
        from_fingers = self.player_hands[self.current_player][from_hand]
        to_fingers = self.player_hands[opponent][to_hand]
        
        # 计算新手指数
        new_value = (to_fingers + from_fingers) % 10
        self.player_hands[self.current_player][from_hand] = new_value
        
        # 若手指数变成 0，则该手放下
        if new_value == 0:
            self.player_hands[self.current_player][from_hand] = 0
        
        # 切换玩家
        self.current_player = opponent
    
    def minimax(self, depth, maximizing_player):
        """Minimax 搜索，maximizing_player=True 表示当前层是最大化层"""
        if self.is_game_over() or depth == 0:
            return 1 if sum(self.player_hands[1 - self.current_player]) == 0 else -1
        
        best_value = -math.inf if maximizing_player else math.inf
        for move in self.get_legal_moves():
            temp_game = HandGame()
            temp_game.player_hands = [list(self.player_hands[0]), list(self.player_hands[1])]
            temp_game.current_player = self.current_player
            temp_game.take_action(*move)
            eval_score = temp_game.minimax(depth - 1, not maximizing_player)
            
            if maximizing_player:
                best_value = max(best_value, eval_score)
            else:
                best_value = min(best_value, eval_score)
        return best_value
    
    def find_best_move(self):
        """寻找当前玩家的最优策略"""
        best_move = None
        best_value = -math.inf
        for move in self.get_legal_moves():
            temp_game = HandGame()
            temp_game.player_hands = [list(self.player_hands[0]), list(self.player_hands[1])]
            temp_game.current_player = self.current_player
            temp_game.take_action(*move)
            move_value = temp_game.minimax(5, False)  # 设定搜索深度为5
            if move_value > best_value:
                best_value = move_value
                best_move = move
        return best_move
    
    def play(self):
        """主循环，玩家 vs AI"""
        print("游戏开始！\n请输入你的动作，例如 'LR' 代表用左手打对方右手")
        while not self.is_game_over():
            self.display()
            
            if self.current_player == 0:
                move = input("你的回合 (输入 LL, LR, RL, RR): ").strip().upper()
                if move not in ["LL", "LR", "RL", "RR"]:
                    print("无效输入，请输入 LL, LR, RL, RR")
                    continue
                from_hand = 0 if move[0] == 'L' else 1
                to_hand = 0 if move[1] == 'L' else 1
                
                if self.player_hands[self.current_player][from_hand] == 0:
                    print("不能用已经放下的手！请重新选择。")
                    continue
            else:
                best_move = self.find_best_move()
                if best_move:
                    from_hand, to_hand = best_move
                    print(f"AI 选择了 {['L', 'R'][from_hand]}{['L', 'R'][to_hand]}")
                else:
                    print("AI 无可用动作！")
                    break
            
            self.take_action(from_hand, to_hand)
        
        # 游戏结束
        # 由于每次调用take_action后玩家会反转 因此终局时的current_player是输家
        winner = self.current_player
        if winner == 0:
            print(f"游戏结束！AI获胜！")
        else:
            print(f"游戏结束！玩家获胜！")

if __name__ == "__main__":
    game = HandGame()
    game.play()
