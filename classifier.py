import pandas as pd
import math
import requests
import sys

# def read_attributes_lines():
#     # TODO: CHANGE THIS TO LOCAL FILE READ
#     train_attribute_url = "https://raw.githubusercontent.com/yaoyusi1109/alpha_pruning/main/restaurant-attributes.txt"
#     return requests.get(train_attribute_url).content.decode("utf-8").split('\n')

ATTRIBUTE_FILE = sys.argv[1]
TRAIN_FILE = sys.argv[2]

def read_attributes_lines():
    # TODO: CHANGE THIS TO LOCAL FILE READ
    file = open(ATTRIBUTE_FILE, 'r', encoding='UTF-8')
    return [x.rstrip('\n') for x in file.readlines()]

ATTR_LINES = read_attributes_lines()
CLASSNAME = ATTR_LINES[0].split(',')[0]
YESNAME = ATTR_LINES[0].split(',')[1]
NONAME = ATTR_LINES[0].split(',')[2]

class Node:
    def __init__(self, isLeaf):
        self.attr_key = ""
        self.children = {}
        self.isLeaf = isLeaf
        self.leafVal = None
    
    def setYes(self):
        if not self.isLeaf:
            raise Exception(attr_key + " is not leaf")
        self.leafVal = YESNAME
    
    def setNo(self):
        if not self.isLeaf:
            raise Exception(attr_key + " is not leaf")
        self.leafVal = NONAME
    
    def set_attr_key(self, attr_key):
        if self.isLeaf:
            raise Exception("I'm a leaf!")
        self.attr_key = attr_key
            
    def append_child(self, branch_val, child):
        if self.isLeaf:
            raise Exception("I'm a leaf!")
        self.children[branch_val] = child
    
    def get_child(self, branch_val):
        if self.isLeaf:
            raise Exception("I'm a leaf!")
        return self.children[branch_val]
    
def read_train_dataframe():
    return pd.read_csv(TRAIN_FILE)

# def read_train_dataframe():
#     # TODO: CHANGE THIS TO LOCAL FILE READ
#     train_csv_url = "https://raw.githubusercontent.com/yaoyusi1109/alpha_pruning/main/restaurant.csv"
#     return pd.read_csv(train_csv_url)

def get_attributes_dictionary():
    attributes = {}
    for attr_line in ATTR_LINES[1:]:
        attr_element = attr_line.split(',')
        key = attr_element[0]
        if key == "":
            continue
        attributes[key] = attr_element[1:]
    return attributes

def entropy(q):
    if q == 1 or q == 0:
        return 0
    retval = -(q * math.log2(q) + (1-q) * math.log2(1-q))
    return retval

def calculate_gain(
    root_dataframe,
    ATTR_DICT,
    attr_key
):
    overall_yes_count = root_dataframe.loc[root_dataframe[CLASSNAME] == YESNAME].shape[0]
    overall_count = root_dataframe.shape[0]
    if overall_yes_count == overall_count:
        raise Exception("overall_yes_count equals to overall_count")
    term1 = entropy(overall_yes_count / overall_count)

    term2 = 0
    
    for branch_attr_val in ATTR_DICT[attr_key]:
        branched_df = root_dataframe.loc[root_dataframe[attr_key] == branch_attr_val]
        branched_df_val_count = branched_df.shape[0]
        if branched_df_val_count == 0:
            continue
        factor = branched_df_val_count / overall_count
        
        entro_param = branched_df.loc[branched_df[CLASSNAME] == YESNAME].shape[0] / branched_df_val_count
        
        term2 += (factor * entropy(entro_param))
    
    return term1 - term2

def build_root(
    root_dataframe, 
    ATTR_DICT, 
    attr_candidates_set):
    if root_dataframe.shape[0] == 0:
        raise Exception("root_dataframe cannot be empty")
    
    yes_count = root_dataframe.loc[root_dataframe[CLASSNAME] == YESNAME].shape[0]
    no_count = root_dataframe.loc[root_dataframe[CLASSNAME] == NONAME].shape[0]
    overall_count = root_dataframe.shape[0]
    
    if len(attr_candidates_set) == 0:
        root = Node(True)
        if yes_count >= no_count:
            root.setYes()
        elif yes_count < no_count:
            root.setNo()
        return root
    
    if yes_count == overall_count:
        root = Node(True)
        root.setYes()
        return root
        
    if no_count == overall_count:
        root = Node(True)
        root.setNo()
        return root

    attr_gain_pairs_lst = []
    for attr_key in attr_candidates_set:
        gain = calculate_gain(
            root_dataframe,
            ATTR_DICT,
            attr_key
        )
        attr_gain_pairs_lst.append((attr_key, gain))
    
    tup = max(attr_gain_pairs_lst, key= lambda x : x[1])
    max_attr_key = tup[0]
    root = Node(False)
    root.set_attr_key(max_attr_key)
    
    max_attr_vals = ATTR_DICT[max_attr_key]
    for branch_attr_val in max_attr_vals:
        child_dataframe = root_dataframe.loc[root_dataframe[max_attr_key] == branch_attr_val]
        if child_dataframe.shape[0] == 0:
            continue
        child_attr_candidates_set = attr_candidates_set.copy()
        child_attr_candidates_set.remove(max_attr_key)
        
        child = build_root(child_dataframe, ATTR_DICT, child_attr_candidates_set)
        root.append_child(branch_attr_val, child)
        
    return root

def visualize(root, prefix):
    if root.isLeaf:
        print(prefix + "Leaf with value: " + root.leafVal)
        return
    print(prefix + "Testing " + root.attr_key)
    for branch_val, child in root.children.items():
        child_prefix = prefix + "  "
        print(child_prefix + "Branch " + branch_val)
        visualize(child, child_prefix)

def node_count(root):
    if root.isLeaf:
        return 1
    retval = 0
    for _, child in root.children.items():
        retval += node_count(child)
    return retval + 1

def decision_count(root):
    if root.isLeaf:
        return 1
    retval = 0
    for _, child in root.children.items():
        retval += decision_count(child)
    return retval

def max_depth(root):
    if root.isLeaf:
        return 1
    dep = float('-inf')
    for _, child in root.children.items():
        dep = max(dep, max_depth(child))
    return dep + 1

def min_depth(root):
    if root.isLeaf:
        return 1
    dep = float('inf')
    for _, child in root.children.items():
        dep = min(dep, min_depth(child))
    return dep + 1

def sum_depth(root):
    if root.isLeaf:
        return 1
    dep = 0
    for _, child in root.children.items():
        dep += (sum_depth(child) + 1)
    return dep

ATTR_DICT = get_attributes_dictionary()
attr_candidate_set = set(ATTR_DICT.keys())

train_data = read_train_dataframe()


root = build_root(train_data, ATTR_DICT, attr_candidate_set)

visualize(root, "")
print("Total Nodes:", node_count(root))
print("Decision Nodes:", decision_count(root))
print("Maximum Depth:", max_depth(root))
print("Minimum Depth:", min_depth(root))
print("Average Depth of Root-to-Leaf:", sum_depth(root) / decision_count(root))
