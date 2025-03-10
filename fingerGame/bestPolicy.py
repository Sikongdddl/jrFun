# Task1：寻找必胜策略

from collections import deque

def generate_all_states():
    """生成所有标准化的游戏状态"""
    states = {}
    for p1_l in range(10):
        for p1_r in range(10):
            if p1_r < p1_l:
                continue  # 确保 p1_l ≤ p1_r
            for p2_l in range(10):
                for p2_r in range(10):
                    if p2_r < p2_l:
                        continue  # 确保 p2_l ≤ p2_r
                    state = (p1_l, p1_r, p2_l, p2_r)
                    states[state] = None  # 未知状态
    return states

#加入特殊状态 用于调试算法
def generate_test_states():
    states = {}
    state = (0,0,5,4)#显而易见的必胜状态 用于调试算法
    states[state] = None
    return states

def get_legal_moves(state):
    """获取当前状态的所有可能合法移动（P1 先手）"""
    p1, p2 = state[:2], state[2:]
    moves = []

    for i in range(2):  # 选择 P1 的左端点或右端点
        if p1[i] > 0:
            new_p1 = list(p1)
            new_p1[i] = (new_p1[i] + p2[0]) % 10  # **修改自身状态**
            moves.append((new_p1[0], new_p1[1], p2[0], p2[1]))  # 交换 P1 和 P2，轮到 P2 走
    return moves

def get_previous_states(state):
    """找到可以一步走到当前状态的所有前驱状态"""
    p1, p2 = state[:2], state[2:]
    previous_states = []

    for i in range(2):  # P1变成了当前的获胜状态
        #说明在上一步p1的行动中，p1的某个手指变成了当前状态
        for j in range(2):  # P1 的某个手指变成了当前状态
            for prev_val in range(10):  # 这个手指可能是某个值加上 p2[i] 后变成的
                if (prev_val + p2[i]) % 10 == p1[j]:
                    new_p1 = list(p1)
                    new_p1[j] = prev_val
                    previous_states.append((new_p1[0], new_p1[1], p2[0], p2[1]))
    previous_states = list(set(previous_states))
    return previous_states

def compute_winning_states(mode):
    """计算所有状态的胜负情况，确保P1总是先手"""
    if(mode == 'test'):
        states = generate_test_states()
    else:
        states = generate_all_states()
    queue = deque()
    losing_states = set()
    winning_states = set()
    move_count = {}

    # 1. 终止状态 (0,0) 是**获胜状态**
    for state in states:
        p1 = state[:2]
        if sum(p1) == 0:
            states[state] = 1
            queue.append((state, 1))
            winning_states.add(state)
        # else:
        #     move_count[state] = len(get_legal_moves(state))

    # 2. 反向标记
    while queue:
        state, result = queue.popleft()
        
        for prev_state in get_previous_states(state):
            if prev_state in states and states[prev_state] is None:
                states[prev_state] = -result
                if result == 1:
                    winning_states.add(prev_state)
                else:
                    losing_states.add(prev_state)
                queue.append((prev_state, -result))

    return states, winning_states

def find_all_winning_states(states):
    """找出所有 P1 先手的必胜状态"""
    return [
        state for state, result in states.items()
        if result == 1 and sum(state[:2]) > 0 and sum(state[2:]) > 0
    ]

if __name__ == "__main__":
    states, winning_states = compute_winning_states('normal')
    winning_states_filtered = find_all_winning_states(states)
    print(f"存在必胜策略的状态数量: {len(winning_states_filtered)}")
    print("示例前 10 个必胜状态:", winning_states_filtered)
