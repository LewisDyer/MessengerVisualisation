import tkinter
from tkinter import filedialog, Tk
import os
import re
import json
from typing import Tuple
from collections import defaultdict
import networkx as nx
import itertools
from pyvis.network import Network
import yaml

def load_messages(filename: str) -> dict:
    with open(filename) as json_file:
        recent_messages = json.load(json_file)
    return recent_messages

def load_folder() -> list:
    cwd = os.getcwd()

    chat_loc = "messages/inbox" # This is where the chat folders will be located

    # We want to use the file dialog to select a folder, but not deal with tkinter windows!
    root = Tk()
    root.withdraw()

    messenger_folder = filedialog.askdirectory(initialdir = os.path.join(cwd, chat_loc), title="Select a chat folder")


    messenger_files = []

    for file in os.listdir(messenger_folder):
        if re.match("^message_(\d)+.json$", file):
            file_loc = os.path.join(messenger_folder, file)
            messenger_files.append(load_messages(file_loc))

    return(messenger_files)

def merge_files(file_list: list) -> Tuple[list, list]:
    messages, people = [], []
    for chat in file_list:

        for message in chat['messages']:

            messages.append(message)

        for person in chat['participants']: 
            if person != 'Facebook User': # don't include placeholder for deleted users
                people.append(person['name'])

    people = sorted(set(people)) # remove duplicates

    return (messages, people)

def build_react_info(messages: list, people: list, config: dict) -> dict:
    react_matrix: dict = {}

    with open('react-info.json', 'r') as react_file:
        react_info = json.load(react_file)

    react_map = react_info['names']
    category = config['graph']['react_category']
    filter_reacts = react_info['categories'][category]

    for person in people:
        react_matrix[person] = defaultdict(int)

    for message in messages:
        author = message['sender_name']
        if author in people: # exclude people who've left the chat
            if 'reactions' in message:
                for reaction in message['reactions']:
                    if reaction['actor'] in people:
                        if react_map[reaction['reaction']] in filter_reacts:
                            react_matrix[author][reaction['actor']] += 1
    
    return(react_matrix)

def get_pair_reacts(person1: str, person2: str, reacts: dict, directed: bool) -> int:

    if directed:
        return (reacts[person1][person2])
    else:
        return(reacts[person1][person2] + reacts[person2][person1])

def make_edge(person1: str, person2: str, reacts: dict, directed: bool, threshold: int, graph):
    pair_reactions = get_pair_reacts(person1, person2, reacts, directed)
    if pair_reactions > threshold:
        graph.add_edge(person1, person2)

def create_graph(messages: list, people: list, reacts: dict, config: dict):

    directed = config['graph']['directed']

    if directed:
        reacts_g = nx.DiGraph()
    else:
        reacts_g = nx.Graph()
    reacts_g.add_nodes_from(people)


    threshold = config['graph']['pair_threshold']

    for pair in itertools.combinations(people, 2):
        make_edge(pair[0], pair[1], reacts, directed, threshold, reacts_g)
        if directed:
            make_edge(pair[1], pair[0], reacts, directed, threshold, reacts_g)
        
    vis = Network(bgcolor='#222222', font_color="white", height="100%", width="100%", directed=directed)

    vis.from_nx(reacts_g)

    neighs = vis.get_adj_list()
    print(neighs)
    for edge in vis.edges:
        edge["value"] = get_pair_reacts(edge["from"], edge["to"], reacts, directed)
        print(edge)

    for node in vis.nodes:
        neighbors = vis.neighbors(node['id'])
        n_metadata = []
        for neighbor in neighbors:
            pair = (node['id'], neighbor)
            matching_edge = [edge for edge in vis.edges if (edge["from"] in pair and edge["to"] in pair)][0]
            n_metadata.append(f'{neighbor} ({matching_edge["value"]})')
        node['title'] = " Reacts:<br>" + "<br>".join(list(n_metadata))

    return(vis)

def show_graph(vis):
    
    vis.repulsion()
    vis.show('graph.html')

if __name__ == '__main__':

    with open("config.yaml", "r") as yml:
        config = yaml.load(yml)

    chat_files = load_folder()
    messages, people = merge_files(chat_files)
    react_matrix = build_react_info(messages, people, config)
    react_graph = create_graph(messages, people, react_matrix, config)

    show_graph(react_graph)


    

