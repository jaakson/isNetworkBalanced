import networkx as net

# Middle East graph data
mid_east = net.Graph()

player_list = ["USA","Turkey","Russia","Assad","Iran","SaudiGulf","AlQaeda",
               "Israel","MB","Sisi","LebShias","LebSunnis","SyriaRebels",
               "Qatar","Hamas"]

for player in player_list:
    mid_east.add_node(player)

buddy_list = [("SaudiGulf","SyriaRebels"),("Qatar","MB"),("Iran","Hamas"),
              ("USA","SyriaRebels"),("USA","Israel"),("USA","SaudiGulf"),
              ("Turkey","MB"),("Turkey","SyriaRebels"),("Qatar","Hamas"),
              ("Russia","Assad"),("Iran","LebShias"),("Iran","Assad"),
              ("Israel","SyriaRebels"),("LebSunnis","SyriaRebels"),
              ("SaudiGulf","LebSunnis"),("AlQaeda","SyriaRebels"),
              ("Qatar","SyriaRebels"),("Hamas","SyriaRebels"),
              ("SaudiGulf","Sisi"),("LebShias","Assad")]

enemy_list = [("LebShias","SyriaRebels"),("Sisi","MB"),("USA","AlQaeda"),
              ("AlQaeda","Assad"),("Russia","SyriaRebels"),("Assad","MB"),
              ("LebSunnis","Assad"),("Qatar","Assad"),("Qatar","Sisi"),
              ("USA","Hamas"),("Hamas","Sisi"),("AlQaeda","SaudiGulf"),
              ("Turkey","Assad"),("Turkey","Sisi"),("SaudiGulf","MB"),
              ("USA","Assad"),("USA","Iran"),("Iran","SyriaRebels"),
              ("Israel","Hamas"),("Israel","Assad")]

mid_east.add_edges_from(buddy_list, polarity = 'positive')
mid_east.add_edges_from(enemy_list, polarity = 'negative')
mid_east = mid_east.to_directed() # needed for simple_cycles method

def main():
    """Analyses the mid_east graph. Gives the number of cycles in the
    graph; checks whether it is structurally balanced; if it is not
    balanced, provides counterexamples and shows which nodes are most
    disruptive to the balance."""

    print("One (sort of terrifying) Graph and Its Analysis")
    print("Data taken from The Washington Post:",
          "http://tinyurl.com/terrifyingChart\n"
          "The graph represents the relationships between these parties:")
    for player in player_list:
        print(player)
        
    print("\nChecking whether the graph is balanced...\n")
    (bad_cycles,good_cycles) = isItBalanced(mid_east)
    if bad_cycles != []:
        culprit_check = input("Would you like to see which parties are "
                              "most volatile? (y/n) ")
        if culprit_check == "y":
            culprits(bad_cycles, good_cycles,player_list)


def isItBalanced(graph):
    """Checks whether the (potentially noncomplete) signed graph is
    structurally balanced; that is, if it contains no cycle with an odd
    number of negative edges."""

    (counterexamples,okcycles) = allCycles(graph)
    num_bad = len(counterexamples)
    num_ok  = len(okcycles)
    total_cycles = num_bad + num_ok
    print("There are",str(total_cycles),"cycles in this graph.\n")

    if counterexamples == []:
        print("This graph is structurally balanced.")
    else:
        print("This graph is not structurally balanced; there are",num_bad,
              "counterexamples.")
        give_example = input("Would you like to see a counterexample? (y/n) ")
        example = 0
        while give_example == "y":
            current_cycle = counterexamples[example]
            neg_edges = numberOfNegativeEdges(graph,current_cycle)
            print("The following cycle has",neg_edges,"negative edges: ")
            print(current_cycle)
            example = example + 1
            give_example = input("Want to see another counterexample? (y/n) ")
    return (counterexamples,okcycles)


def culprits(bad_cycles,good_cycles,node_list):
    """Establishes which of the nodes are most "volatile" within the graph.
    A node's score is proportional to its volatility; it is the number of
    unbalanced cycles in which it appears, minus the number of balanced
    cycles in which it appears."""

    freqs_bad = [0]*len(node_list)
    for cycle in bad_cycles:
        for node in cycle:
            for i in range(len(node_list)):
                if node == node_list[i]:
                    freqs_bad[i] = freqs_bad[i] + 1
    for cycle in good_cycles:
        for node in cycle:
            for i in range(len(node_list)):
                if node == node_list[i]:
                    freqs_bad[i] = freqs_bad[i] - 1

    print("The more volatile the party, the higher its score.")
    max_score = -5000
    max_index = 0
    for node_index in range(len(node_list)):
        player = node_list[node_index]
        print(player,"has a score of",str(freqs_bad[node_index])+".")
    for index in range(len(node_list)):
        if max_score < freqs_bad[index]:
            max_index = index
            max_score = freqs_bad[index]
    print("The most volatile party is",node_list[max_index],
          "with a score of",str(max_score)+".")


def allCycles(graph):
    """Returns two lists of cycles: the 'bad' cycles (containing an odd
    number of negative edges) and the 'good' cycles (which do not disrupt
    the graph's structural balance.)"""

    bad_cycles = []
    good_cycles = []
    list_of_cycles = list(net.simple_cycles(graph))

    for cycle in list_of_cycles:
        neg_edges = numberOfNegativeEdges(graph,cycle)
        if neg_edges%2 != 0:
            bad_cycles.append(cycle)
        else:
            good_cycles.append(cycle)
    return (bad_cycles,good_cycles)


def numberOfNegativeEdges(graph,cycle):
    """Returns the number of negative edges in the cycle."""
    negative_edges = 0
    edge_list = getEdgesFromCycle(cycle)
    for edge in edge_list:
        (node1,node2) = edge
        edge_polarity = graph[node1][node2]['polarity']
        if edge_polarity == "negative":
            negative_edges = negative_edges + 1
    return negative_edges


def getEdgesFromCycle(cycle):
    """Takes in a cycle and returns a list of pairs of nodes,
    corresponding to the edges in the cycle."""
    list_of_edges = []
    index = -1 # index of first node in edge pair
    for this_node in cycle:
        last_node = cycle[index]
        list_of_edges.append((last_node,this_node))
        index = index + 1
    return list_of_edges

main()
