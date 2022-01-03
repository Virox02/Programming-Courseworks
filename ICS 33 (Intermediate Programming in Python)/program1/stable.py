# Submitter: kimmk10 (Kim, Min Kee)
# Partner  : vvijaywa (Vijaywargiya, Viraj)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

import prompt
import goody
from copy import deepcopy

# Use these global variables to index the list associated with each name in the dictionary.
# e.g., if men is a dictionary, men['m1'][match] is the woman who matches man 'm1', and 
# men['m1'][prefs] is the list of preference for man 'm1'.
# It would seems that this list might be better represented as a named tuple, but the
# preference list it contains is mutated, which is not allowed in a named tuple. 

match = 0   # Index 0 of list associate with name is match (str)
prefs = 1   # Index 1 of list associate with name is preferences (list of str)


def read_match_preferences(open_file : open) -> {str:[str,[str]]}:
    preferences_dict = {}
    for line in open_file:
        person, *preferences = line.rstrip('\n').split(';')
        preferences_dict[person] = [None, preferences]
    return preferences_dict


def dict_as_str(d : {str:[str,[str]]}, key : callable=None, reverse : bool=False) -> str:
    dict_str = ''
    for person in sorted(d.keys(), key=key, reverse=reverse):
        dict_str += '  ' + person + ' -> ' + str(d[person]) + '\n'
    return dict_str


def who_prefer(order : [str], p1 : str, p2 : str) -> str:
    return (p1 if (order.index(p1) < order.index(p2)) else p2)


def extract_matches(men : {str:[str,[str]]}) -> {(str,str)}:
    return {(man, men[man][match]) for man in men}


def make_match(men : {str:[str,[str]]}, women : {str:[str,[str]]}, trace : bool = False) -> {(str,str)}:
    trace_statement = '\nWomen Preferences (unchanging)\n' + str(dict_as_str(women))
    men_copy = deepcopy(men)
    unmatched_men = {man for man in men_copy}
    while len(unmatched_men) > 0:
        for man in men:
            if man in unmatched_men:
                while men_copy[man][match] == None:
                    trace_statement += '\nMen Preferences (current)\n' + str(dict_as_str(men_copy)) + '\nunmatched men = ' + str(unmatched_men) + '\n'
                    if (women[men_copy[man][prefs][0]][match] == None) or (who_prefer(women[men_copy[man][prefs][0]][prefs], man, women[men_copy[man][prefs][0]][match]) == man):
                        unmatched_men.remove(man)
                        men_copy[man][match] = men_copy[man][prefs][0]
                        if women[men_copy[man][prefs][0]][match] != None:
                            unmatched_men.add(women[men_copy[man][prefs][0]][match])
                            men_copy[women[men_copy[man][prefs][0]][match]][match] = None
                            trace_statement += '\n' + man + ' proposes to ' + men_copy[man][prefs][0] + ' (a matched woman); she prefers her new match, so she accepts the proposal\n'
                        else:
                            trace_statement += '\n' + man + ' proposes to ' + men_copy[man][prefs][0] + ' (an unmatched woman); so she accepts the proposal\n'
                        women[men_copy[man][prefs][0]][match] = man
                    else:
                        trace_statement += '\n' + man + ' proposes to ' + men_copy[man][prefs][0] + ' (a matched woman); she prefers her current match, so she rejects the proposal'
                    men_copy[man][prefs].pop(0)
    trace_statement += '\nTracing option finished: final matches = ' + str(extract_matches(men_copy))
    if trace:
        print(trace_statement)
    return extract_matches(men_copy)
            
  


  
    
if __name__ == '__main__':
    input_file_men = goody.safe_open('Input the file name detailing the preferences for men', 'r', 'Illegal file name')
    input_file_women = goody.safe_open('Input the file name detailing the preferences for women', 'r', 'Illegal file name')
    print()
    men_preferences = read_match_preferences(input_file_men)
    women_preferences = read_match_preferences(input_file_women)
    input_file_men.close()
    input_file_women.close()
    print('Men Preferences')
    print(dict_as_str(men_preferences))
    print('Women Preferences')
    print(dict_as_str(women_preferences))
    trace_option = prompt.for_bool('Input tracing algorithm option', True, 'Please enter a boolean value: True or False')
    print('\nThe final matches = ' + str(make_match(men_preferences, women_preferences, trace_option)))
    
    
    
              
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc2.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
