# Submitter: kimmk10 (Kim, Min Kee)
# Partner  : vvijaywa (Vijaywargiya, Viraj)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

import goody
import prompt
from collections import defaultdict


def read_graph(file : open) -> {str:{str}}:
    graph_dict = defaultdict(set)
    for line in file:
        source_node, reached_node = line.rstrip('\n').split(';')
        graph_dict[source_node].add(reached_node)
    return dict(graph_dict)


def graph_as_str(graph : {str:{str}}) -> str:
    graph_str = ''
    for source_node, reached_nodes in sorted(graph.items()):
        graph_str += '  ' + str(source_node) + ' -> ' + str(sorted(reached_nodes)) + '\n'
    return graph_str

        
def reachable(graph : {str:{str}}, start : str, trace : bool = False) -> {str}:
    trace_statement = ''
    reached_set = set()
    exploring_list = [start]
    while exploring_list != []:
        explore_node = exploring_list[0]
        trace_statement += 'reached set    = ' + str(reached_set) + '\n' + 'exploring list = ' + str(exploring_list) + '\n'+ 'transferring node ' + explore_node + ' from the exploring list to the reached set\n'
        exploring_list.pop(0)
        reached_set.add(explore_node)
        if explore_node in graph.keys():
            for reached_node in graph[explore_node]:
                if reached_node not in reached_set:
                    exploring_list.append(reached_node)
        trace_statement += 'after adding all nodes reachable directly from ' + explore_node + ' but not already in reached, exploring = ' + str(exploring_list) + '\n\n'
    if trace:
        print(trace_statement)
    return reached_set

if __name__ == '__main__':
    input_file = goody.safe_open('Input the file name detailing the graph', 'r', 'Illegal file name')
    print()
    graph = read_graph(input_file)
    input_file.close()
    print('Graph: str (source node) -> [str] (sorted destination nodes)')
    print(graph_as_str(graph))
    starting_node = prompt.for_string('Input one starting node (or input done)', None, (lambda x: x in sorted(list(graph.keys()))+['done']), 'Illegal: not a source node')
    if starting_node != 'done':
        trace_option = prompt.for_bool('Input tracing algorithm option', True, 'Please enter a boolean value: True or False')
        print('From the starting node ' + starting_node + ', its reachable nodes are: ' + str(reachable(graph, starting_node, trace_option)))
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc1.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()