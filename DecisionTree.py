

import csv
import copy
import random
import math
import collections 
import sys

class treeNode:
    def __init__(self):
        self.left = None
        self.right = None
        self.label = None
        self.D_set = None
        self.val = -1
        self.isLeaf = -1

class DecisionTree:
    def __init__(self, data, Mlist):
        self.data = data
        self.Mlist = Mlist

    def entropy(self, D_set):
        B_list = self.B_list(D_set)
        result = collections.Counter(B_list)
        l = len(B_list)
        entropyval = 0.0
        for k in result:
            probval = float(result[k]) / l
            entropyval -=  probval * math.log(probval, 2)
        return entropyval

    def splitAttribute(self, Dataset, value):
        d1_set=[]
        d2_set=[]
        for row in Dataset:
            if row[self.Mlist.index(value)] == 0:
                d1_set.append(row)
            else:
                d2_set.append(row)
        return (d1_set, d2_set)

    def InformationGain(self, set, datalist):
        G = 0.0
        F = ''
        old = self.entropy(set)
        new = 0.0
        s = len(set)
        for val in datalist:
            (N_set, P_set) = self.splitAttribute(set, val)
            prob = float(len(P_set))/s
            t = 1.0 - prob
            new = prob * self.entropy(P_set) + t * self.entropy(N_set)
            gain = old - new
            if gain > G:
                G = gain
                F = val
        return G,F

    def Variance(self, Data_set):
        B_list = self.B_list(Data_set)
        v = len(B_list)
        result = collections.Counter(B_list)
        s = len(result)
        if s <= 1:
            return 0
        else:
            vinumber = 1.0
            for i in result:
                probval = float(result[i])/v
                vinumber *=  probval
            return vinumber

    def VarianceImp(self, set1, D_list):
        BG = 0.0
        finalval=''
        new = 0.0
        s = len(set1)
        old = self.Variance(set1)
        for v in D_list:
            (N_set, P_set) = self.splitAttribute(set1, v)
            prob = (float(len(P_set)))/s
            r = 1.0 - prob
            new = prob * self.Variance(P_set) + r * self.Variance(N_set)
            gainval = old - new
            if gainval > BG:
                BG = gainval
                finalval = v
        return BG, finalval

    def measure(self,B_list,root,D_set, Dlist):
        s = len(Dlist)
        entropy = self.entropy(D_set)
        t = B_list.count(B_list[0])
        if (t == len(B_list)):
            root.val = B_list[0]
            root.isLeaf = 1
            root.left = None
            root.right = None
            return root        
        root.val = self.maxlabel(D_set)
        if s == 0 or entropy == 0:
            root.isLeaf = 1
            root.left = None
            root.right = None
            return root
        return root

    def maxlabel(self, D_set):
        B_list = self.B_list(D_set)
        B_count = {}
        for tag in B_list:
            if tag not in B_count.keys():B_count[tag] = 0
            B_count[tag] += 1
        C = -1
        num = -1
        for key in B_count.keys():
            if B_count[key] > C:
                C = B_count[key]
                num = key
        return num

    def traverse(self, row, root):
        if root.right == None and root.left == None:
            return root.val
        if row[self.Mlist.index(root.label)] == 0:
            return self.traverse(row, root.left)
        else:
            return self.traverse(row, root.right)
        
    def accuracylevel(self, data, root):
        s = len(data)
        if root == None or s == 0:
            return 0
        Count = 0
        aval = self.B_list(data);
        b = len(aval)
        n = 0
        for row in data:
            if int(self.traverse(row, root)) == int(aval[n]):
                Count= Count+1
            n=n+1
        acc = float(Count)/b
        return acc

    def EntropyTree(self, D_set, D_list1):
        t = len(D_set)
        if(t == 0):
            return 0
        root= treeNode()
        B_list = self.B_list(D_set)
        root=self.measure(B_list,root,D_set, D_list1)
        gain,att = self.InformationGain(D_set, D_list1)
        if gain > 0:
            root.label = att
            D_list1.remove(att)
            C1_set = copy.copy(D_list1)
            C2_set = copy.copy(D_list1)
            D_set0, D_set1 = self.splitAttribute(D_set, att)
            root.left = self.EntropyTree(D_set0, C1_set)
            root.right = self.EntropyTree(D_set1, C2_set)
        return root
     
    def VarianceTree(self, D_set, D_list2):
        s = len(D_set)
        if(s == 0):
            return 0
        root=treeNode()
        B_list = self.B_list(D_set)
        root=self.measure(B_list,root,D_set, D_list2)
        variancegain,att = self.VarianceImp(D_set, D_list2)
        if variancegain > 0:
            root.label = att
            D_list2.remove(att)
            C1_set = copy.copy(D_list2)
            C2_set = copy.copy(D_list2)
            D_set0, D_set1 = self.splitAttribute(D_set, att)
            root.left = self.VarianceTree(D_set0, C1_set)
            root.right = self.VarianceTree(D_set1, C2_set)
        return root
    
    def nodeOrder(self,root):
        nodeOrder = []
        p = root.isLeaf
        if root == None or p == 1:
            return root
        queue = collections.deque([root])
        while len(queue) > 0:
            rootnode = queue.popleft()
            nodeOrder.append(rootnode)
            if rootnode.left!= None and rootnode.left.isLeaf == -1:
                queue.append(rootnode.left)
            if rootnode.right!= None and rootnode.right.isLeaf == -1:
                queue.append(rootnode.right)
        return nodeOrder
    
    def treePrune(self, data, root, m, n):
        root_1 = copy.deepcopy(root)
        for i in range(1, m):
            root_2 = copy.deepcopy(root)
            r = random.randint(1, n)
            for j in range(1, r):
                nodearranged = self.nodeOrder(root_2)
                if (len(nodearranged) - 1) <= 0:
                    return root_1
                p = random.randint(1, len(nodearranged) - 1)
                nodenew = nodearranged[p]
                nodenew.isLeaf = 1
                nodenew.left = None
                nodenew.right = None
            base = self.accuracylevel(data, root_1)
            new = self.accuracylevel(data, root_2)
            if (new > base):
                root_1 = root_2
        return root_1

    def displaytree(self, root,c):
        d = ''
        if root == None:
            return ''
        if root.left == None and root.right == None:
            d += str(root.val) + '\n'
            return d
        barline = ''
        for i in range(0, c):
            barline += '|'
        d += barline
        if root.left!= None and root.left.left == None and root.left.right == None:
            d +=  str(root.label) + " = 0 : "
        else:
            d +=  str(root.label) + " = 0 :\n"
        d += self.displaytree(root.left, c + 1)
        d += barline
        if root.left != None and root.right.left == None and root.right.right == None:
            d += str(root.label) + " = 1 :"
        else:
            d += str(root.label) + " = 1 :\n"
        d += self.displaytree(root.right, c + 1)
        return d

    def B_list(self, Dataset):
        B_list = [row[-1] for row in Dataset]
        return B_list


if __name__ == "__main__":

    # get L,K values
    L = int(sys.argv[1])
    K = int(sys.argv[2])
    training_path = sys.argv[3]
    test_path = sys.argv[4]
    validation_path = sys.argv[5]
    Print = sys.argv[6]
    l = 0

    with open(training_path,'r') as file1:
     data = list(csv.reader(file1))
    B_List = data[0][:-1]
    data = data[1:]
    list1 = []
    list2 =[]
    for row in data:
        list2.append([int(i) for i in row])
        list1.append([int(i) for i in row])
    DTree = DecisionTree(set, B_List)
    D_set1 = copy.deepcopy(B_List)
    D_set2 = copy.deepcopy(B_List)
    E_tree = DTree.EntropyTree(list2, D_set1)
    V_tree= DTree.VarianceTree(list1,D_set2)

    with open(test_path, 'r') as file2:
        test_data = list(csv.reader(file2))
    test_data = test_data[1:]
    testDataset = []
    for row in test_data:
        testDataset.append([int(i) for i in row])

    with open(validation_path,'r') as file3:
        data= list(csv.reader(file3))
    B_List = data[0][:-1]
    datalist = data[1:]
    v_set = []
    for row in datalist:
        v_set.append([int(t) for t in row])


    EntropyB_Tree = DTree.treePrune(v_set, E_tree, L, K)
    VarB_Tree = DTree.treePrune(v_set, V_tree, L, K)
    print('accuracy before pruning entropy:',DTree.accuracylevel(testDataset, E_tree))
    print('accuracy before pruning Var_Imp:',DTree.accuracylevel(testDataset, V_tree))
    print('accuracy value post_pruning for entropy:',DTree.accuracylevel(testDataset,EntropyB_Tree))
    print('accuracy value post_pruning for Var_Imp:',DTree.accuracylevel(testDataset,VarB_Tree))
    if(Print == 'yes'):
        print('Prepruning tree based on info-gain:\n',DTree.displaytree(E_tree, l))
        print('Prepruning Tree based on Varianceimp:\n',DTree.displaytree(V_tree, l))
        print('Postpruning Tree based on info-gain:\n',DTree.displaytree(EntropyB_Tree, l))
        print('Postpruning Tree based on Varianceimp:\n',DTree.displaytree(VarB_Tree, l))
     
  