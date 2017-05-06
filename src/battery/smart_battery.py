import random
import time
import math
import copy
from battery.battery import Battery
from evaluator import Evaluator

class SmartBattery(Battery):

    def __init__(self, evaluator):
        self.evaluator = evaluator
        self.sim_time = 10
        self.max_sim = 10000
        self.max_cost = 0

    def get_action(self, current_state):
        legal_moves = self.evaluator.get_legal_moves(current_state)
        if len(legal_moves) == 1:
            return legal_moves[0]
        else:
            return self.monte_carlo_search(current_state)

    def monte_carlo_search(self, current_state):
        results = {}
        amnt_children = len(self.evaluator.get_legal_moves(current_state))
        root = Node(current_state, None, amnt_children)

        sim_count = 0
        now = time.time()
        while (time.time() - now < self.sim_time and
               root.moves_unfinished > 0 and
               sim_count <= self.max_sim):
            picked_node = self.tree_policy(root)
            result = self.simulate(picked_node.game_state)
            result = 1 - (result / (result + 1))
            self.back_prop(picked_node, result)
            sim_count += 1
        print("The simulation count is {}".format(sim_count))

        for child in root.children:
            wins, plays = child.get_wins_plays()
            position = child.move
            results[position] = (wins, plays)

        # for position in sorted(results, key=lambda x: results[x][1]):
        #     print('{}: ({}/{})'.format(position, results[position][0], results[position][1]))
        # print('{} simulations performed.'.format(sim_count))
        return self.best_action(root)

    @staticmethod
    def best_action(node):
        most_plays = -float('inf')
        best_wins = -float('inf')
        best_actions = []
        for child in node.children:
            wins, plays = child.get_wins_plays()
            if plays > most_plays:
                most_plays = plays
                best_actions = [child.move]
                best_wins = wins
            elif plays == most_plays:
                if wins > best_wins:
                    best_wins = wins
                    best_actions = [child.move]
                elif wins == best_wins:
                    best_actions.append(child.move)
        return random.choice(best_actions)

    @staticmethod
    def back_prop(node, delta):
        while node.parent is not None:
            node.plays += 1
            node.wins += delta
            node = node.parent
        node.plays += 1
        node.wins += delta

    def tree_policy(self, root):
        cur_node = root
        while True and root.moves_unfinished > 0:
            legal_moves = self.evaluator.get_legal_moves(cur_node.game_state)
            if len(cur_node.children) < len(legal_moves):
                unexpanded = [
                    move for move in legal_moves
                    if move not in cur_node.moves_expanded
                ]
                assert len(unexpanded) > 0
                move = random.choice(unexpanded)
                state = self.evaluator.get_updated_state(cur_node.game_state, move)
                child = Node(state, move, len(legal_moves))
                cur_node.add_child(child)
                return child
            else:
                cur_node = self.best_child(cur_node)
        return cur_node

    def best_child(self, node):
        C = 1  # 'exploration' value
        values = {}
        for child in node.children:
            wins, plays = child.get_wins_plays()
            _, parent_plays = node.get_wins_plays()
            assert parent_plays > 0
            values[child] = (wins / plays) \
                + C * math.sqrt(2 * math.log(parent_plays) / plays)
        best_choice = max(values, key=values.get)
        return best_choice

    def simulate(self, game_state):
        state = copy.deepcopy(game_state)
        while state.rounds_remaining > 0:
            moves = self.evaluator.get_legal_moves(state)
            picked = random.choice(moves)
            state = self.evaluator.get_updated_state(state, picked)
        return state.cost

class Node:

    def __init__(self, game_state, move, amount_children):
        self.game_state = game_state
        self.plays = 0
        self.wins = 0
        self.children = []
        self.parent = None
        self.moves_expanded = set()  # which moves have we tried at least once
        self.moves_unfinished = amount_children  # amount of moves not fully expan
        self.move = move

    def propagate_completion(self):
        if self.parent is None:
            return
        if self.moves_unfinished > 0:
            self.moves_unfinished -= 1
        self.parent.propagate_completion()

    def add_child(self, node):
        self.children.append(node)
        self.moves_expanded.add(node.move)
        node.parent = self

    def has_children(self):
        return len(self.children) > 0

    def get_wins_plays(self):
        return self.wins, self.plays

    def __hash__(self):
        return hash(self.game_state)

    def __repr__(self):
        return 'move: {} wins: {} plays: {}'.format(self.move, self.wins, self.plays)

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.game_state == other.game_state
