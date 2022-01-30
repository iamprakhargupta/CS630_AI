"""
CSCI-630: Foundation of AI
HW1 Code - hw1.py
Author: Prakhar Gupta
Username: pg9349

An implementation of word ladder

Code uses graph.py and vertex.py

"""


from graph import Graph

import sys
from time import time

def read_file(f):
    """
    Reads the dict file
    :param f File name

    :return: A list of words in the file
    """
    lines=[]
    with open(f) as f:
        line=f.readlines()


    for i in line:
        lines.append(i.strip())

    return lines


def similarityscore(a,b):
    """
    Computes a similarity score between two words

    :param a Words one
    :param b Words two

    :return: A a score which is the number of letter it found different at
    each position of the two words
    score is zero if a==b
    """
    c=0
    for i in range(0,len(a)):
        if(a[i]!=b[i]):
            c+=1
    return c




def make_graph_dict(data):
    """
    Computes a adjacency dict which is used to make graph

    :param data list of words


    :return: d adjacency dict
    """
    d={}
    for i in data:
        letter_node=list(i)
        d[i] = []
        for j in data:

            if len(j)==len(i):
                letter_v=list(j)
                difference=similarityscore(letter_node,letter_v)
                if(difference==1):
                    d[i].append(j)


    return d


def make_graph(graph_list):
    """
    Creates a graph using the adjacency list

    :param graph_list Dict of nodes and vertices


    :return: word_graph Graph object
    """
    word_graph= Graph()
    for nodes, neighbors in graph_list.items():
        for neighbor in neighbors:
            if neighbor is not None:
                # this automatically creates a new vertex if not already present
                word_graph.addEdge(nodes, neighbor)

    return word_graph



def BFS(start, end):
    """
    This code is modified from CS 603

    Find the shortest path, if one exists, between a start and end vertex
    :param start (Vertex): the start vertex
    :param end (Vertex): the destination vertex

    :return: A list of Vertex objects from start to end, if a path exists,
             otherwise None
    """

    queue = []
    queue.append(start)  # prime the queue with the start vertex

    predecessors = {}
    predecessors[start] = None  # add the start vertex with no predecessor

    # Loop until either the queue is empty, or the end vertex is encountered
    while len(queue) > 0:
        current = queue.pop(0)
        if current == end:
            break
        for neighbor in current.getConnections():
            if neighbor not in predecessors:  # if neighbor unvisited
                predecessors[neighbor] = current  # map neighbor to current
                queue.append(neighbor)  # enqueue the neighbor

    # If the end vertex is in predecessors a path was found
    if end in predecessors:
        path = []
        current = end
        while current != start:  # loop backwards from end to start
            path.insert(0, current)  # prepend current to the path list
            current = predecessors[current]  # move to the predecessor
        path.insert(0, start)
        return path
    else:
        return None





def main(f,b,c):
    """
    THis is main
    :param f: File path
    :param b: word start
    :param c: word stop
    :return: None
    """

    data=read_file(f)
    start_time = time()

    print("Creating Graph mapping......")
    d=make_graph_dict(data)
    #print(d)
    print("Creating Graph........... ")
    word_graph=make_graph(d)
    #print(b,c)
    #print(word_graph)
    print("Word ladder........... ")
    if b in d.keys() and c in d.keys():
        temp = BFS(word_graph.getVertex(b),
                                  word_graph.getVertex(c))

        if temp is None or len(temp)==0:
            print("no solution")
        else:
            for i in temp:
                if i is not None:
                    print(i.id)

        runtime = f"{(time() - start_time):0.4f} seconds"
        print("It took "+runtime)

    else:
        print("Word not in dict")

if __name__ == '__main__':
    #print(sys.argv)
    if len(sys.argv)==4:
        a=sys.argv[1]
        b = sys.argv[2]
        c = sys.argv[3]
        main(a,b,c)
    else:
        print("Check args list")

