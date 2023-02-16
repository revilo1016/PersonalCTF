class Node:
    """
    Our standard node for our suffix Tree
    """

    def __init__(self, leaf, parent):
        self.start = None
        """Start Index"""
        self.end = None
        """End Index"""
        self.suffixLink = None
        """suffix Link pointer for suffix link optimization"""
        self.parent = parent
        """
        Distance of parent from root, aka how many chars are covered before reaching this node
        This is used to easily calculate the SA at the end
        """
        self.children = {}
        """Children of the node"""
        self.leaf = leaf
        """Is the node a leaf"""

    def __eq__(self, node):
        """
        Redefining equals for our node class, compares the start and end to see if
        the two nodes are equal to one another
        :param node: the node to check
        :return: True or False
        """
        start = self.start
        end = self.end
        nodeStart = node.start
        nodeEnd = node.end
        return nodeStart == start and nodeEnd == end

    def __ne__(self, node):
        """
        Same as above but defining not equals
        :param node: the node to check
        :return: True or False
        """
        start = self.start
        end = self.end
        nodeStart = node.start
        nodeEnd = node.end
        return nodeStart != start or nodeEnd != end

    def __getattribute__(self, name):
        """
        This allows us to set our global pointer for our leaf, saving space
        if it is a leaf it returns the leafEnd, if not it acts regularly
        :param name: node
        :return: The end index
        """
        if name == 'end':
            if self.leaf == True:
                return leafEnd
        return super(Node, self).__getattribute__(name)


class SuffixTree:
    """
    Implementation of our suffix tree class
    """

    def __init__(self, data):
        """
        Our Tree class, purpose of each variable is explained below
        :param data: the String
        """
        self.String = data + '$'
        """Need to append a $ to the end for smallest lexicographic Char"""
        self.lastNewNode = None
        """
        This is where we store the last node that was created for the purposes of 
        Suffix Linking
        """
        self.remainingsuff = 0
        """
        Remaining suffixes to be added
        """
        self.EndSplit = None
        """
        The end of the split node used in extension rule 2
        """
        self.size = len(self.String)
        """
        input string length
        """
        self.root = None
        """
        Storing the root node of the tree
        """
        self.suffArr = []
        """
        The suffix Array to be returned
        """
        self.AN = None
        """
        Our current active node
        """
        self.AE = -1
        """
        Our active edge, with the edge represented by the index not the char 
        """
        self.AL = 0
        """
        Length of the active edge
        """

    def edgeLen(self, node):
        """
        Helper function for returning edge length
        :param node: node to check edge len
        :return: length of edge
        """
        return node.end - node.start + 1

    def skipTrick(self, current_node):
        """
        This is the implementation of the skip trick, effectively checking if the current length of the active node
        is less than the length of the edge of the traversed node, if it is, we can skip over this until we can no
        longer skip, rather than doing each individual comparison

        :param current_node: node to check
        """
        length = self.edgeLen(current_node)
        didThisWork = False
        # helper function above
        if self.AL >= length:
            self.AE += length
            self.AL -= length
            self.AN = current_node
            didThisWork = True
            return didThisWork
        didThisWork = False
        return didThisWork

    def nodeFactory(self, start, end=None, leaf=False, par=-1):
        """
        The function used to create a new node
        :param start: start of the edge
        :param end: end of the edge
        :param leaf: is it a leaf
        :param par: length of parent edge, set to -1 for the root node
        :return: the new node with correct vals
        """
        node = Node(leaf, par)
        # create node with leaf and parent
        node.suffixLink = self.root
        # set the nodes link to the root until we update our next node
        node.start = start
        node.end = end
        # set start and end
        return node

    def growSuffTree(self, pos):
        global leafEnd
        """Global variable pointing to the leafEnd
        This is used for extension rule 1 as it lets us set the end for all leafs to the same val, since they will all 
        end at the same pos, saving space
        """
        leafEnd = pos
        """update leaf end as we run through"""

        # new suff to add to tree
        self.remainingsuff += 1
        # since we've started a new phase, we need to update so there is no lastNewNode to be added
        self.lastNewNode = None
        # add suffixes to tree
        while self.remainingsuff > 0:
            if self.AL == 0:
                self.AE = pos
            # there is no edge from active node
            if self.AN.children.get(self.String[self.AE]) is None:
                # ext rule 2
                self.AN.children[self.String[self.AE]] = self.nodeFactory(pos, leaf=True, par=self.edgeLen(self.AN) + self.AN.parent)
                """
                Create a new child, at string[edge] where edge is index, and set it to true. Set the parent val
                to the length of the parents parent value, and the edge length of the parent (how many before + how many
                in parent edge)
                """
                if self.lastNewNode is not None:
                    """set our suffix link to the active node"""
                    self.lastNewNode.suffixLink = self.AN
                    """set our 'waiting on link' variable to none"""
                    self.lastNewNode = None
            else:
                # find the next node along the edge
                NextNode = self.AN.children.get(self.String[self.AE])
                if self.skipTrick(NextNode):
                    #if it returns true it carries on
                    continue
                # ext rule 3
                if self.String[NextNode.start + self.AL] == self.String[pos]:
                    # update suffix link as per before, ensuring the active node isnt root
                    if (self.lastNewNode is not None) and (self.AN != self.root):
                        self.lastNewNode.suffixLink = self.AN
                        self.lastNewNode = None
                    self.AL = self.AL + 1
                    # theres now no need to carry on with this phase, so we can skip to next phase
                    break
                # this is extension rule 2 case b, where we now need to create a new node and split the current edge into
                # different branches
                self.EndSplit = NextNode.start + self.AL - 1
                # set the split to be before the start of the next node
                # create the new node using our node factory
                split = self.nodeFactory(NextNode.start, self.EndSplit, par=self.edgeLen(self.AN) + self.AN.parent)
                # active node is still the parent of this split node so we use it to find our parent value
                self.AN.children[self.String[self.AE]] = split
                # set the child of the active node to be equal to our new split node
                split.children[self.String[pos]] = self.nodeFactory(pos, leaf=True,
                                                                    par=self.edgeLen(split) + split.parent)
                # create a new node for the position as a child of split using split for parent
                NextNode.start += self.AL
                NextNode.parent = self.edgeLen(split) + split.parent
                split.children[self.String[NextNode.start]] = NextNode
                """we now use this to resolve our 'waiting for node' suffix link to split"""
                if self.lastNewNode is None:
                    pass
                else:
                    self.lastNewNode.suffixLink = split
                self.lastNewNode = split
                # now our new split node is waiting on a suffix link
            self.remainingsuff -= 1
            # we have now added a suffix to the tree, so decrement
            if (self.AN == self.root) and (self.AL > 0):
                self.AL -= 1
                self.AE = pos - self.remainingsuff + 1
            elif self.root != self.AN:
                self.AN = self.AN.suffixLink

    def makeSuffTree(self):

        """
        our initial suffix Tree Generator, makes the root bode then iterates through, adding each suffix
        :return: Returns true if nothing broke
        """
        self.root = self.nodeFactory(-1, -1)
        self.AN = self.root  # First activeNode will be root
        for i in range(self.size):
            self.growSuffTree(i)
        return True
tree = SuffixTree("testing")
tree.makeSuffTree()
print("this is a stop point")