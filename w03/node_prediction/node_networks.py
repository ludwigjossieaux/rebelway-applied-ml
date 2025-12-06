import hou

class NodeUtils:
    def __init__(self):
        pass
    
    def printTest(self):
        print("Test from NodeUtils")
        
    def getNetworkAsLinkedList(self, root_node):
        current = root_node
        
        res = [root_node.type().name()]
        
        while current.outputs():
            current = current.outputs()[0]
            res.append(current.type().name())
            print(current.name())
        
        return res