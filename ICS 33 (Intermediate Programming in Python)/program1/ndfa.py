# Submitter: kimmk10 (Kim, Min Kee)
# Partner  : vvijaywa (Vijaywargiya, Viraj)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

import goody
from collections import defaultdict


def read_ndfa(file : open) -> {str:{str:{str}}}:
    ndfa_dict = {}
    for line in file:
        state, *transitions = line.rstrip('\n').split(';')
        ndfa_dict[state] = defaultdict(set)
        for user_input in transitions[::2]:
            ndfa_dict[state][user_input].add(transitions[transitions.index(user_input)+1])
            transitions[transitions.index(user_input)] = ''
        ndfa_dict[state] = dict(ndfa_dict[state])
    return ndfa_dict


def ndfa_as_str(ndfa : {str:{str:{str}}}) -> str:
    ndfa_str = ''
    for state, transitions in sorted(ndfa.items()):
        ndfa_str += '  ' + state + ' transitions: ' + str([(user_input, sorted(result_state)) for user_input, result_state in sorted(transitions.items())]) + '\n'
    return ndfa_str

       
def process(ndfa : {str:{str:{str}}}, state : str, inputs : [str]) -> [None]:
    current_state = {state}
    new_states = set()
    ndfa_states = [state]
    for user_input in inputs:
        if len(current_state) >= 1:
            for state1 in current_state:
                if user_input in ndfa[state1].keys():
                    new_states.update(ndfa[state1][user_input])
            ndfa_states.append((user_input, new_states))
            current_state = new_states
            new_states = set()
    return ndfa_states


def interpret(result : [None]) -> str:
    interpret_str = ''
    start, *states = result
    interpret_str += 'Start state = ' + start
    for user_input, new_states in states:
        interpret_str += '\n  Input = ' + user_input + '; new possible states = ' + str(sorted(list(new_states)))
    interpret_str += '\nStop state(s) = ' + str(sorted(list(new_states))) + '\n'
    return interpret_str





if __name__ == '__main__':
    ndfa_file = goody.safe_open('Input the file name detailing the Non-Deterministic Finite Automaton', 'r', 'Illegal file name')
    ndfa = read_ndfa(ndfa_file)
    ndfa_file.close()
    print('\nThe details of the Non-Deterministic Finite Automaton')
    print(ndfa_as_str(ndfa))
    input_file = goody.safe_open('Input the file name detailing groups of start-states and their inputs', 'r', 'Illegal file name')
    print()
    for line in input_file:
        state, *transitions = line.rstrip('\n').split(';')
        print('NDFA: the trace from its start_state')
        print(interpret(process(ndfa, state, transitions)))
    input_file.close()
    
              
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc4.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
