# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 23:20:58 2018

@author: divya
"""
"""
Steps:
    1. Read all the files in the egonet folder
    2. Converted egonet files to graphs (To avoid large computation time, files with number of nodes>65 are skipped)
    3. Found circles in graph using enumedrate_all_cliques()
    4. Imposed minimum threshold of 5 friends on clique to form a circle
    5. Identified common features that exist among nodes in same circle 

"""



import networkx as nx
import os

def get_file_names(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            filenames.append(os.path.join(root, name))
            
def create_graphs(fname):
    G = nx.Graph()
    for line in open(fname, 'r'):
        e1, es = line.split(':')
        es = es.split()
        for e in es:
          if e == e1: continue
          G.add_edge(int(e1),int(e))
    return G

def find_Cliques(G, cliqueSize):
    # find communities using enumedrate_all_cliques()
    listOfCircles = []
    kCliqueComunities = list(nx.enumedrate_all_cliques(G))
    for community in kCliqueComunities:
        # leave only relativly large communities
        if len(community) >= cliqueSize:
            print(community)
            f.write('\n'+str(community))
            find_features(community)
            listOfCircles.append(list(community))
    return listOfCircles

def find_features(nodes):
    features = open('features.txt', 'r') 
    FList=[]
    Common=[]
    for line in features:
        Temp_list=[]
        words=line.split(' ')
        for word in words: 
            Temp_list.append(word)
        if(int(Temp_list[0]) in nodes):
            if(len(FList)>0 and len(Common)==0):
                for i in Temp_list:
                    if i in FList and i not in Common:
                        #adding features to common list
                        Common.append(i)
            elif(len(Common)>0):
                for i in Common:
                    if i not in Temp_list:
                        #removing features from common list
                        Common.remove(i)
            else:
                for i in Temp_list:
                    FList.append(i)
    
    f.write(' feature: '+ str(Common))

if __name__ == '__main__':
    f = open('Common_features.txt', 'w')
    f1= open('output.txt', 'w')
    path= "E:/Social Network Analysis/project data/egonets/"
    filenames=[]
    get_file_names(path) #to read all file in the folder
    for name in filenames:
        G=create_graphs(name) #converting egonet files to graph
        Circles = []
        # do not calculate for large graphs (it takes too long)
        if len(G.nodes()) > 65:  #tooManyNodesThreshold=65                                 
            print ('skipping user ' + str(name) +'\n')
            continue
        else:
            print ('predicting for user ' + str(name) +'\n')
            Circles.append(find_Cliques(G, 5)) #tooLittleFriendsInCircleThreshold=5 
        predictionString = ''
        for circle in Circles:
            for node in circle:
                predictionString = predictionString + str(node) + ' '
            predictionString = predictionString[:-1] + ';'
            f1.write(predictionString+'\n')
        predictionString = predictionString[:-1]

    