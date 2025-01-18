import re
from collections import defaultdict, deque

# NFA Class
class NFA:
    def __init__(self, states, alphabet, start_state, accept_states, transitions, epsilon_transitions):
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions
        self.epsilon_transitions = epsilon_transitions

    def __str__(self):
        result = ["NFA:"]
        result.append(f"States: {self.states}")
        result.append(f"Alphabet: {self.alphabet}")
        result.append(f"Start State: {self.start_state}")
        result.append(f"Accept States: {self.accept_states}")
        result.append("Transitions:")
        for state, paths in self.transitions.items():
            for symbol, next_states in paths.items():
                result.append(f"  {state} --{symbol}--> {next_states}")
        result.append("Epsilon Transitions:")
        for state, next_states in self.epsilon_transitions.items():
            result.append(f"  {state} --epsilon--> {next_states}")
        return "\n".join(result)

# DFA Class
class DFA:
    # dfa = DFA(set(set()), nfa.alphabet, set(0), set(), {})

    def __init__(self, states, alphabet, start_state, accept_states, transitions):
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions

    def __str__(self):
        result = ["DFA:"]
        result.append(f"States: {self.states}")
        result.append(f"Alphabet: {self.alphabet}")
        result.append(f"Start State: {self.start_state}")
        result.append(f"Accept States: {self.accept_states}")
        result.append("Transitions:")
        for state, paths in self.transitions.items():
            for symbol, next_state in paths.items():
                result.append(f"  {state} --{symbol}--> {next_state}")
        return "\n".join(result)

def preprocess_regex(regex):
    """
    Insert explicit concatenation (.) where needed in the regex.
    """
    result = []
    for i in range(len(regex)):
        result.append(regex[i])
        if i + 1 < len(regex):
            # Add concatenation if the next character is an operand or opening parenthesis
            if (regex[i].isalnum() or regex[i] == ')' or regex[i] == '*') and (regex[i + 1].isalnum() or regex[i + 1] == '('):
                result.append('.')
    return ''.join(result)

def regex_to_postfix(regex):
    """
    Convert infix regex to postfix using the Shunting Yard algorithm.
    """
    precedence = {'*': 3, '.': 2, '|': 1, '(': 0, ')': 0}
    output = []
    operators = []

    for char in regex:
        if char.isalnum():  # Operand
            output.append(char)
        elif char == '(':
            operators.append(char)
        elif char == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()  # Remove '('
        else:  # Operator (*, |, .)
            while (operators and precedence[operators[-1]] >= precedence[char]):
                output.append(operators.pop())
            operators.append(char)

    while operators:
        output.append(operators.pop())

    return ''.join(output)

# Function to parse regex and construct NFA
def regex_to_nfa(regex):
    regex = regex_to_postfix(preprocess_regex(regex))
    stack = []
    state_counter = 0

    def new_state():
        nonlocal state_counter
        state_counter += 1
        return state_counter - 1

    def create_basic_nfa(symbol):
        start = new_state()
        end = new_state()
        transitions = defaultdict(lambda: defaultdict(set))
        epsilon_transitions = defaultdict(set)
        transitions[start][symbol].add(end)
        return NFA({start, end}, {symbol}, start, {end}, transitions, epsilon_transitions)

    for char in regex:
        if char.isalnum():  # Basic character
            stack.append(create_basic_nfa(char))
        elif char == '*':  # Kleene star
            nfa = stack.pop()
            start = new_state()
            end = new_state()

            transitions = defaultdict(lambda: defaultdict(set))
            epsilon_transitions = defaultdict(set, nfa.epsilon_transitions)

            epsilon_transitions[start].update({nfa.start_state, end})
            epsilon_transitions[list(nfa.accept_states)[0]].update({nfa.start_state, end})

            transitions.update(nfa.transitions)

            stack.append(NFA(nfa.states | {start, end}, nfa.alphabet, start, {end}, transitions, epsilon_transitions))
        elif char == '.':  # Concatenation
            nfa2 = stack.pop()
            nfa1 = stack.pop()

            transitions = defaultdict(lambda: defaultdict(set), nfa1.transitions)
            epsilon_transitions = defaultdict(set, nfa1.epsilon_transitions)

            epsilon_transitions[list(nfa1.accept_states)[0]].add(nfa2.start_state)
            transitions.update(nfa2.transitions)
            epsilon_transitions.update(nfa2.epsilon_transitions)

            stack.append(NFA(nfa1.states | nfa2.states, nfa1.alphabet | nfa2.alphabet, nfa1.start_state, nfa2.accept_states, transitions, epsilon_transitions))
        elif char == '|':  # Union (OR)
            nfa2 = stack.pop()
            nfa1 = stack.pop()

            start = new_state()
            end = new_state()

            transitions = defaultdict(lambda: defaultdict(set))
            epsilon_transitions = defaultdict(set, nfa1.epsilon_transitions)
            epsilon_transitions.update(nfa2.epsilon_transitions)

            epsilon_transitions[start].update({nfa1.start_state, nfa2.start_state})
            epsilon_transitions[list(nfa1.accept_states)[0]].add(end)
            epsilon_transitions[list(nfa2.accept_states)[0]].add(end)

            transitions.update(nfa1.transitions)
            transitions.update(nfa2.transitions)

            stack.append(NFA(nfa1.states | nfa2.states | {start, end}, nfa1.alphabet | nfa2.alphabet, start, {end}, transitions, epsilon_transitions))

    return stack.pop()

# Function to compute epsilon closure
def epsilon_closure(states, epsilon_transitions):
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        for next_state in epsilon_transitions[state]:
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)

    return frozenset(closure)

# Function to check if a set of NFA states contains any accept state
def contains_accept_state(state_set, accept_states):
    """Check if the state set contains any accept state."""
    return not state_set.isdisjoint(accept_states)

# Function to convert NFA to DFA
def convert_nfa_to_dfa(nfa):
    dfa = DFA(set(), nfa.alphabet, frozenset(), set(), defaultdict(lambda: defaultdict(frozenset)))

    # Initial DFA state (set containing NFA start state)
    start_state = epsilon_closure({nfa.start_state}, nfa.epsilon_transitions)
    dfa.start_state = start_state

    unmarked_states = deque([start_state]) # Queue for BFS
    visited_states = {start_state: True}  # Track visited DFA states
    dfa.states.add(start_state) # Add start state to the set of DFA states

    if contains_accept_state(start_state, nfa.accept_states):
        dfa.accept_states.add(start_state) # Mark start state as an accept state

    # BFS to construct the DFA
    while unmarked_states:
        current_state = unmarked_states.popleft()
        
        for symbol in nfa.alphabet:
            new_set = set()
            for state in current_state:
                new_set.update(nfa.transitions[state][symbol])

            # Compute epsilon closure of the next state
            new_set = epsilon_closure(new_set, nfa.epsilon_transitions)

            if new_set:
                dfa.transitions[current_state][symbol] = new_set

                # check if the next set has not been visited
                if new_set not in visited_states:
                    visited_states[new_set] = True
                    dfa.states.add(new_set)
                    unmarked_states.append(new_set)

                    if contains_accept_state(new_set, nfa.accept_states):
                        dfa.accept_states.add(new_set)
            
    return dfa
                        

# Main Function for Testing
def main():
    regex = "(a|b)*abb"
    nfa = regex_to_nfa(regex)
    print(nfa)

    dfa = convert_nfa_to_dfa(nfa)
    print(dfa)

if __name__ == "__main__":
    main()
