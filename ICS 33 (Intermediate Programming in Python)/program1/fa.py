# Submitter: kimmk10 (Kim, Min Kee)
# Partner  : vvijaywa (Vijaywargiya, Viraj)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

import goody


def read_fa(file : open) -> {str:{str:str}}:
    fa_dict = {}
    for line in file:
        state, *transitions = line.rstrip('\n').split(';')
        fa_dict[state] = {}
        for user_input in transitions[::2]:
            fa_dict[state][user_input] = transitions[transitions.index(user_input)+1]
    return fa_dict
        


def fa_as_str(fa : {str:{str:str}}) -> str:
    fa_str = ''
    for state, transitions in sorted(fa.items()):
        fa_str += '  ' + state + ' transitions: ' + str([(user_input, result_state) for user_input, result_state in sorted(transitions.items())]) + '\n'
    return fa_str

    
    
def process(fa : {str:{str:str}}, state : str, inputs : [str]) -> [None]:
    current_state = state
    fa_states = [state]
    for user_input in inputs:
        if user_input in fa[current_state].keys():
            current_state = fa[current_state][user_input]
            fa_states.append((user_input, current_state))
        else:
            fa_states.append((user_input, None))
            break
    return fa_states


def interpret(fa_result : [None]) -> str:
    interpret_str = ''
    start, *states = fa_result
    interpret_str += 'Start state = ' + start
    for user_input, new_state in states:
        if new_state != None:
            interpret_str += '\n  Input = ' + user_input + '; new state = ' + new_state
        else:
            interpret_str += '\n  Input = ' + user_input + '; illegal input: simulation terminated'
    interpret_str += '\nStop state = ' + str(new_state) + '\n'
    return interpret_str




if __name__ == '__main__':
    fa_file = goody.safe_open('Input the file name detailing the Finite Automaton', 'r', 'Illegal file name')
    fa = read_fa(fa_file)
    fa_file.close()
    print('\nThe details of the Finite Automaton')
    print(fa_as_str(fa))
    input_file = goody.safe_open('Input the file name detailing groups of start-states and their inputs', 'r', 'Illegal file name')
    print()
    for line in input_file:
        state, *transitions = line.rstrip('\n').split(';')
        print('FA: the trace from its start_state')
        print(interpret(process(fa, state, transitions)))
    input_file.close()
    
              
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc3.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
