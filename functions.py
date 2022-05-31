"""
This file was created to read the external coefficients made by Robert Wills

https://www.youtube.com/watch?v=ACvXAjZE9jQ

"""


# heart coefficients precreated by Robert Wills
heartByRobertWills = [(0 - 0.0390431j), (0 - 0.2342587j), (0 - 0.1952156j), (0 + 0.9760778j), (0 - 0.0060066j ), (0 + 0.0390431j), (0 - 0.1952156j), (0 + 0.0780862j), (0 - 0.0390431j)]


def cordListGenerate(scale): # scale is required to change the coefficient scale
    returnlist = []     # temporary list
    for i in range(len(heartByRobertWills)//2 + 1):
        
        # rearrange the list given from coefficient order of c-4, c-3, c-2, c-1, c0, c1, c2, c3, c4 to c0, c1, c-1, c2, c-2, c3, c-3, c4, c-4
        if i != 0: 
            returnlist.append(heartByRobertWills[len(heartByRobertWills)//2 + i] * scale)
            returnlist.append(heartByRobertWills[len(heartByRobertWills)//2 - i] * scale)
        else: returnlist.append(heartByRobertWills[len(heartByRobertWills)//2] * scale)
    return returnlist

# sum all the elements in a list
def sumList(ll):
    total = 0
    for i in ll:
        total += i
    return total