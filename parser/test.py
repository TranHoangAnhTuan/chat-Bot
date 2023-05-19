import nltk

# Construct the tree

# Convert the tree to a ParentedTree object
# Define a recursive function to check if a subtree is a Det and NP combination
# tree.pretty_print()

def subtree_label(tree):
    labels = []
    if len(tree) == 1:
        return [tree.label()]
    for subtree in tree:
        try:
            labels.append(subtree.label())
        except:
            print("subtree ", type(tree))
            raise NotImplementedError
        
    return labels


def NP_chunk(tree):

    subtree = subtree_label(tree)
    if len(subtree) == 1:
        if subtree[0] == "N" or subtree[0] == "NP":
            return [tree]
        else:
            return []
    if subtree[0] == "Det" and subtree[1] == "NP":
        return [tree]
    
    list_NP = []
    for subtree in tree:
        list_NP += NP_chunk(subtree)
        
            
    return list_NP
    
