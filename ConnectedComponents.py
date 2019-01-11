# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 15:12:50 2018

@author: divya
"""
import networkx as nx
import os


def get_file_names(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            filenames.append(os.path.join(root, name))

def read_files(names):
    for name in names:
        G=create_graphs(name)
        c = nx.connected_components(G)
        return c

def create_graphs(fname):
    G = nx.Graph()
    for line in open(fname, 'r'):
        e1, es = line.split(':')
        es = es.split()
        for e in es:
          if e == e1: continue
          G.add_edge(int(e1),int(e))
    return G

if __name__ == '__main__':
    f = open('output.txt', 'w')
    path= "E:/Social Network Analysis/project data/egonets/"
    filenames=[]
    get_file_names(path) #to read all file in the folder
    
    for name in filenames:
        G=create_graphs(name) #converting egonet files to graph
        c = nx.connected_components(G) #find connected component
        f.write(str(list(c))+'\n'+'\n') # print all the components in the form of a list of nodes

    