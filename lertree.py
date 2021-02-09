import time
class Node: 
    def __init__(self, tag):
        self.tag = tag
        self.left = None
        self.right = None
        self.colour = None 
        self.parent = [None, None]
        self.isPrincipal = False
        self.wx = 0
        self.wwx = 0
        self.bx = 0
        self.bbx = 0
        self.totalWhite = self.wx + self.wwx
        self.totalBlack = self.bx + self.bbx
        self.noOfChildren = 0


def solver(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        t3 = time.time()
        global nodes
        nodes = []
        data = list(map(str.strip, f.readlines()))
        # totalNodes = int(data[0])
        colours = data[1].split()
        for i in range(len(colours)):
            currNode = Node(i)
            currNode.colour = colours[i]
            nodes.append(currNode)
        root = nodes[0]
        for line in data[2:]:
            parent, child, c = line.split()
            parent = int(parent)
            child = int(child)
            nodes[parent].noOfChildren += 1
            if c == '0':
                nodes[parent].left = nodes[child]
                nodes[child].parent = [nodes[parent], 'left']
            else:
                nodes[parent].right = nodes[child]
                nodes[child].parent = [nodes[parent], 'right']
            if nodes[parent].noOfChildren == 2:
                nodes[parent].isPrincipal = "possible"
        t4 = time.time()
        # print("time taken to form the tree ", t4 -t3)
        t1 = time.time()
        nodeCategory = postOrderIterative(root)
        t2 = time.time()
        # print("time taken by the post order function ", t2 - t1)
        return str(nodeCategory[0]) + ' ' + str(nodeCategory[1]) + ' ' + str(nodeCategory[2])
        
def peek(stack): 
    if len(stack) > 0: 
        return stack[-1] 
    return None

# the idea for this bit of code was borrowed from https://www.geeksforgeeks.org/iterative-postorder-traversal-using-stack/
def postOrderIterative(root): 
    lNodes = 0
    eNodes = 0
    rNodes = 0
    # tree = [] 
    stack = [] 
    while(True): 
        while (root): 
            if root.right is not None: 
                stack.append(root.right) 
            stack.append(root) 
            root = root.left 
        root = stack.pop() 
        # check if it has any children to its right 
        if (root.right is not None and 
            peek(stack) == root.right): 
            stack.pop() 
            stack.append(root) 
            root = root.right 
        # check left subtree
        else:
            # increament total black and total white here
            root.totalWhite = root.wx + root.wwx
            root.totalBlack = root.bx + root.bbx
            # now check for ler
            if root.isPrincipal == "possible":
                nodeType = lerCheck(root) 
                if nodeType == 'L':
                    lNodes += 1
                elif nodeType == 'E':
                    eNodes += 1
                elif nodeType == 'R':
                    rNodes += 1
            # change the atributes of the parent  
            parent = root.parent
            if parent[1] == 'left': 
                if root.colour == '0': # colour is white
                    parent[0].wx += root.totalWhite + 1
                    parent[0].bx += root.totalBlack
                else: # root is black
                    parent[0].bx += root.totalBlack + 1 
                    parent[0].wx += root.totalWhite    
            elif parent[1] == 'right':
                if root.colour == '0':
                    parent[0].wwx += root.totalWhite + 1
                    parent[0].bbx += root.totalBlack 
                else:
                    parent[0].bbx += root.totalBlack + 1
                    parent[0].wwx += root.totalWhite
            # tree.append(root.tag)  
            root = None
        if (len(stack) <= 0): 
                break
    return [lNodes, eNodes, rNodes]

def lerCheck(node):
    if node.wx <= 0 or node.wwx <= 0 or node.bx <= 0 or node.bbx <= 0:
        return None
    elif node.wx/node.bx > node.wwx/node.bbx:
        return "L"
    elif  node.wx/node.bx == node.wwx/node.bbx:
        return "E"
    else:
        return "R"


# print(solver("alg\L-E-RTrees\lerTreeData\pub09.in"))

def driver():
    for i in range(1, 11):
        inFile = "alg\L-E-RTrees\lerTreeData\pub" + \
        f"{i:02d}" + '.in'
        outFile = "alg\L-E-RTrees\lerTreeData\pub" + \
        f"{i:02d}" + '.out'
        t1 = time.time()
        myAns = solver(inFile)
        t2 = time.time()
        with open(outFile, 'r', encoding='utf-8') as out:
            ans = out.readlines()
            ans = list(map(str.strip, ans))
            ans = ans[0]
        print(myAns, '|', ans, '|', myAns == ans, 'time taken = ', t2 - t1)
       

driver()