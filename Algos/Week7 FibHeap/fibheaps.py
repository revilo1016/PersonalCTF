import math
"""
implementation of a fib heap
"""

class FibonacciHeap:
    '''
    Establish our node class
    '''
    class Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.parent = None
            self.child = None
            self.left = None
            self.right = None
            self.degree = 0
            self.mark = False

    """
    function for iterating through linked list
    """
    def iterate(self, head):
        node = stop = head
        flag = False
        while True:
            if node == stop and flag is True:
                break
            elif node == stop:
                flag = True
            yield node
            node = node.right

    '''init pointers to head node and min node'''
    forest = None
    min = None

    """no of nodes in heap"""
    total = 0

    """acces our pointer to return min node"""
    def findMin(self):
        return self.min


    def RemoveMin(self):
        '''
        extracts the minimum node from the list
        :return: min node
        '''
        minNode = self.min
        if minNode is not None:
            if minNode.child is not None:
                '''If z has children, send to forest'''
                children = [x for x in self.iterate(minNode.child)]
                for i in range(0, len(children)):
                    self.mergeWithForest(children[i])
                    children[i].parent = None
            self.removeFromForest(minNode)
            '''set the min node to the right child of our prev min'''
            if minNode == minNode.right:
                self.min = self.forest = None
            else:
                self.min = minNode.right
                '''Consolidate the list after operation'''
                self.consolidate()
            self.total -= 1
            "we've removed a node, so remove one from the total"
        return minNode


    def insert(self, key, value=None):
        '''Inserting a new node into the forest, do not consolidate yet, that will be done in extract min'''
        n = self.Node(key, value)
        #create node
        n.left = n.right = n
        self.mergeWithForest(n)
        #add to forest
        if self.min is None or n.key < self.min.key:
            self.min = n
        #update the min node if needed
        self.total += 1
        #add one to total min node
        return n

    def decreaseKey(self, x, k):
        '''modify the key of a node'''
        if k > x.key:
            return None
        x.key = k
        y = x.parent
        if y is not None and x.key < y.key:
            self.cut(x, y)
            self.cascading_cut(y)
        if x.key < self.min.key:
            self.min = x
            #check for new min

    '''
    merging 2 fibbonacci heaps thru concatenating root lists
    '''
    def merge(self, heap2nd):
        """

        :param heap2nd: heap to add to current heap
        :return: newly merged heap
        """
        currHeap = FibonacciHeap()
        currHeap.forest, currHeap.min = self.forest, self.min
        #we need to update pointers with vals from second heap
        last = heap2nd.forest.left
        heap2nd.forest.left = currHeap.forest.left
        currHeap.forest.left.right = heap2nd.forest
        currHeap.forest.left = last
        currHeap.forest.left.right = currHeap.forest
        # update min node if needed
        if heap2nd.min.key < currHeap.min.key:
            currHeap.min = heap2nd.min
        # update total nodes
        currHeap.total = self.total + heap2nd.total
        return currHeap

    '''If a child is smaller than a parent node, the child needs to be sent to the forest'''
    def cut(self, x, y):
        """
        :param x: child
        :param y: par
        :return: nothing, but child is now in forest
        """
        self.DestroyTheChild(y, x)
        y.degree -= 1
        #remove a child, so now decrease degree
        self.mergeWithForest(x)
        x.parent = None
        #child is in forest so no parent
        x.mark = False

    # cascading cut of parent node to obtain good time bounds
    def cascading_cut(self, y):
        z = y.parent
        if z is not None:
            if y.mark is False:
                y.mark = True
            else:
                self.cut(y, z)
                self.cascading_cut(z)

    '''Our consolidate function, we'll be merging nodes of equal degree'''
    def consolidate(self):
        A = [None] * int(math.log(self.total) * 2)
        #list of nodes
        #may want to implement in an easier to read fashion
        nodes = [w for w in self.iterate(self.forest)]
        for w in range(0, len(nodes)):
            x = nodes[w]
            d = x.degree
            while A[d] != None:
                y = A[d]
                if x.key > y.key:
                    temp = x
                    x, y = y, temp
                self.heapLink(y, x)
                #if the degrees match, link the two trees
                A[d] = None
                d += 1
            A[d] = x
        '''
        after this we will need to search for a new min
        '''
        for i in range(0, len(A)):
            if A[i] is not None:
                if A[i].key < self.min.key:
                    self.min = A[i]

    '''This is where we will link the two nodes of equal degrees together '''
    def heapLink(self, y, x):
        self.removeFromForest(y)
        y.left = y.right = y
        self.MergeTheChild(x, y)
        x.degree += 1
        y.parent = x
        y.mark = False

    # merge a node with the doubly linked root list
    def mergeWithForest(self, node):
        if self.forest is None:
            self.forest = node
        else:
            node.right = self.forest.right
            node.left = self.forest
            self.forest.right.left = node
            self.forest.right = node

    # merge a node with the doubly linked child list of a root node
    def MergeTheChild(self, parent, node):
        if parent.child is None:
            parent.child = node
        else:
            node.right = parent.child.right
            node.left = parent.child
            parent.child.right.left = node
            parent.child.right = node

    # remove a node from the doubly linked root list
    def removeFromForest(self, node):
        if node == self.forest:
            self.forest = node.right
        node.left.right = node.right
        node.right.left = node.left

    # remove a node from the doubly linked child list
    def DestroyTheChild(self, parent, node):
        if parent.child == parent.child.right:
            parent.child = None
        elif parent.child == node:
            parent.child = node.right
            node.right.parent = parent
        node.left.right = node.right
        node.right.left = node.left