import math
import sys
from timeit import default_timer as timer
from tabulate import tabulate

sys.setrecursionlimit(160000)


class Node(object):  # Obiekt - korzeń
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class BST(object):  # Obiekt - drzewo BST
    # Metoda - wstawianie pojedynczego elementu do drzewa i obliczanie wysokości każdego korzenia
    def insert(self, root, key):
        if root is None:
            return Node(key)
        if root.key == key:
            return root
        if root.key < key:
            root.right = self.insert(root.right, key)
        else:
            root.left = self.insert(root.left, key)
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))
        return root

    # Metoda - wstawianie listy do drzewa i obliczanie wysokości każdego korzenia
    def insertArr(self, root, arr):
        for i in arr:
            root = self.insert(root, i)
        return root

    # Metoda - usuwanie elementu z obliczaniem nowej wysokości
    def deleteNode(self, root, key):
        if root is None:
            return root
        if key < root.key:
            root.left = self.deleteNode(root.left, key)
        elif key > root.key:
            root.right = self.deleteNode(root.right, key)
        else:
            if root.left is None:
                tmp = root.right
                root = None
                return tmp
            if root.right is None:
                tmp = root.left
                root = None
                return tmp
            tmp = self.minValue(root.right)
            root.key = tmp.key
            root.right = self.deleteNode(root.right, tmp.key)
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))
        return root

    # Metoda - usuwanie kilku elementów drzewa
    def deleteNodes(self, root):
        arr = [int(x)
               for x in input("Input keys you want to delete\n").split()]
        for i in arr:
            root = self.deleteNode(root, i)
        return root

    # Metoda - balansowanie drzewa metodą rotacji
    def balanceTree(self, root):
        tmp = Node(0)
        tmp.right = root
        count = self.__bstToVine(tmp)
        h = int(math.log2(count+1))
        m = pow(2, h) - 1
        self.__compress(tmp, count-m)
        for m in [m // 2**i for i in range(1, h+1)]:
            self.__compress(tmp, m)
        return tmp.right

    def printBalanceTree(self, root):
        print("Przed zbalansowaniem:\n")
        self.preOrder(root)
        root = self.balanceTree(root)
        print("Po zbalansowaniu:\n")
        self.preOrder(root)
        return root

    def __bstToVine(self, root):
        count = 0
        tmp = root.right
        while tmp:
            if tmp.left:
                oldTmp = tmp
                tmp = tmp.left
                oldTmp.left = tmp.right
                tmp.right = oldTmp
                root.right = tmp
            else:
                count += 1
                root = tmp
                tmp = tmp.right
        return count

    def __compress(self, root, m):
        tmp = root.right
        for _ in range(m):
            oldTmp = tmp
            tmp = tmp.right
            root.right = tmp
            oldTmp.right = tmp.left
            tmp.left = oldTmp
            root = tmp
            tmp = tmp.right

    # Metoda - zwracanie wysokości
    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    # Metoda - zwracanie balansu
    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    # Metoda - zwracanie najmniejszego elementu
    def minValue(self, root):
        current = root
        while current.left is not None:
            current = current.left
        return current

    # Metoda - zwracanie największego elementu
    def maxValue(self, root):
        current = root
        while current.right is not None:
            current = current.right
        return current

    # Metoda - zwracanie najmniejszego elementu z pokazaniem kolejności od korzenia
    def printMinValue(self, root):
        print("Ścieżka do minimalnej wartości")
        if root.left is not None:
            print(root.key, end=" ")
            self.printMinValue(root.left)
        else:
            print(root.key)
            print(" ")

    # Metoda - zwracanie największego elementu z pokazaniem kolejności od korzenia
    def printMaxValue(self, root):
        print("Ścieżka do maksymalnej wartości")
        if root.right is not None:
            print(root.key, end=" ")
            self.printMaxValue(root.right)
        else:
            print(root.key)
            print(" ")

    # Metoda - sprawdzanie, czy istnieje element o danej wartości
    def searchValue(self, root, key):
        if root is None or root.key == key:
            return root
        if root.key < key:
            return self.searchValue(root.right, key)
        return self.searchValue(root.left, key)

    # Metoda - wypisanie elementów metodą in-order - od najmniejszego do największego
    def inOrder(self, root):
        if root:
            self.inOrder(root.left)
            print(root.key, end=" ")
            self.inOrder(root.right)
        print(" ")

    def inOrderNoPrint(self, root):
        if root:
            self.inOrderNoPrint(root.left)
            xd = root.key
            self.inOrderNoPrint(root.right)

    # Metoda - wypisanie elementów metodą pre-order
    def preOrder(self, root):
        if root is None:
            return
        print(root.key, end=" ")
        self.preOrder(root.left)
        self.preOrder(root.right)
        print(" ")

    # Metoda - wypisanie elementów metodą post-order
    def postOrder(self, root):
        if root is None:
            return
        self.postOrder(root.left)
        self.postOrder(root.right)
        print(root.key, end=" ")
        print(" ")

    # Metoda - usuwanie każdego elementu drzewa metodą post-order wraz z wypisaniem usuwanego elementu
    def printDeleteAll(self, root):
        if root is None:
            return
        self.postOrder(root.left)
        self.postOrder(root.right)
        print(root.key, end=" ")
        root = None
        return root

    # Metoda - wypisanie poddrzewa od danej wartości metodą pre-order
    def printSubTree(self, root, key):
        if root is None or root.key == key:
            self.preOrder(root)
        elif root.key < key:
            self.printSubTree(root.right, key)
        else:
            self.printSubTree(root.left, key)

    # Metoda - graficzna reprezentacja drzewa
    def visualPrint(self, currPtr, indent, last):
        if currPtr != None:
            print(indent, end="")
            if last:
                print("R----", end="")
                indent += "     "
            else:
                print("L----", end="")
                indent += "|    "
            print(currPtr.key)
            self.visualPrint(currPtr.left, indent, False)
            self.visualPrint(currPtr.right, indent, True)


class AVL(object):  # Obiekt - drzewo AVL
    # Metoda - wstawianie pojedynczego elementu do drzewa i obliczanie wysokości każdego korzenia
    def insert(self, root, key, balance):
        if root is None:
            return Node(key)
        if root.key == key:
            return root
        if root.key < key:
            root.right = self.insert(root.right, key, False)
        else:
            root.left = self.insert(root.left, key, False)
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))
        if balance:
            root = self.balanceTree(root)
        return root

    # Metoda - wstawianie listy z sortowaniem do drzewa i obliczanie wysokości każdego korzenia
    def insertArr(self, root, arr, balance):
        arr.sort()
        middle = len(arr)//2
        root = self.insert(root, arr[middle], False)
        if middle-1 >= 0:
            root = self.insertArr(root, arr[:middle], False)
        if middle+1 < len(arr):
            root = self.insertArr(root, arr[middle+1:], False)
        if balance:
            root = self.balanceTree(root)
        return root

    # Metoda - usuwanie elementu z obliczaniem nowej wysokości
    def deleteNode(self, root, key, balance):
        if root is None:
            return root
        if key < root.key:
            root.left = self.deleteNode(root.left, key, False)
        elif key > root.key:
            root.right = self.deleteNode(root.right, key, False)
        else:
            if root.left is None:
                tmp = root.right
                root = None
                return tmp
            if root.right is None:
                tmp = root.left
                root = None
                return tmp
            tmp = self.minValue(root.right)
            root.key = tmp.key
            root.right = self.deleteNode(root.right, tmp.key, False)
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))
        if balance:
            root = self.balanceTree(root)
        return root

    # Metoda - usuwanie kilku elementów drzewa
    def deleteNodes(self, root):
        arr = [int(x)
               for x in input("Input keys you want to delete\n").split()]
        for i in arr:
            root = self.deleteNode(root, i, False)
        root = self.balanceTree(root)
        return root

    # Metoda - balansowanie drzewa metodą rotacji
    def balanceTree(self, root):
        tmp = Node(0)
        tmp.right = root
        count = self.__bstToVine(tmp)
        h = int(math.log2(count+1))
        m = pow(2, h) - 1
        self.__compress(tmp, count-m)
        for m in [m // 2**i for i in range(1, h+1)]:
            self.__compress(tmp, m)
        return tmp.right

    def printBalanceTree(self, root):
        print("Przed zbalansowaniem:\n")
        self.preOrder(root)
        root = self.balanceTree(root)
        print("Po zbalansowaniu:\n")
        self.preOrder(root)
        return root

    def __bstToVine(self, root):
        count = 0
        tmp = root.right
        while tmp:
            if tmp.left:
                oldTmp = tmp
                tmp = tmp.left
                oldTmp.left = tmp.right
                tmp.right = oldTmp
                root.right = tmp
            else:
                count += 1
                root = tmp
                tmp = tmp.right
        return count

    def __compress(self, root, m):
        tmp = root.right
        for _ in range(m):
            oldTmp = tmp
            tmp = tmp.right
            root.right = tmp
            oldTmp.right = tmp.left
            tmp.left = oldTmp
            root = tmp
            tmp = tmp.right

    # Metoda - zwracanie wysokości
    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    # Metoda - zwracanie balansu
    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    # Metoda - zwracanie najmniejszego elementu
    def minValue(self, root):
        current = root
        while current.left is not None:
            current = current.left
        return current

    # Metoda - zwracanie największego elementu
    def maxValue(self, root):
        current = root
        while current.right is not None:
            current = current.right
        return current

    # Metoda - zwracanie najmniejszego elementu z pokazaniem kolejności od korzenia
    def printMinValue(self, root):
        if root.left is not None:
            print(root.key, end=" ")
            self.printMinValue(root.left)
        else:
            print(root.key)

    # Metoda - zwracanie największego elementu z pokazaniem kolejności od korzenia
    def printMaxValue(self, root):
        if root.right is not None:
            print(root.key, end=" ")
            self.printMaxValue(root.right)
        else:
            print(root.key)

    # Metoda - sprawdzanie, czy istnieje element o danej wartości
    def searchValue(self, root, key):
        if root is None or root.key == key:
            return root
        if root.key < key:
            return self.searchValue(root.right, key)
        return self.searchValue(root.left, key)

    # Metoda - wypisanie elementów metodą in-order - od najmniejszego do największego
    def inOrder(self, root):
        if root:
            self.inOrder(root.left)
            print(root.key, end=" ")
            self.inOrder(root.right)

    def inOrderNoPrint(self, root):
        if root:
            self.inOrderNoPrint(root.left)
            xd = root.key
            self.inOrderNoPrint(root.right)

    # Metoda - wypisanie elementów metodą pre-order
    def preOrder(self, root):
        if root is None:
            return
        print(root.key, end=" ")
        self.preOrder(root.left)
        self.preOrder(root.right)

    # Metoda - wypisanie elementów metodą post-order
    def postOrder(self, root):
        if root is None:
            return
        self.postOrder(root.left)
        self.postOrder(root.right)
        print(root.key, end=" ")

    # Metoda - usuwanie każdego elementu drzewa metodą post-order wraz z wypisaniem usuwanego elementu
    def printDeleteAll(self, root):
        if root is None:
            return
        self.postOrder(root.left)
        self.postOrder(root.right)
        print(root.key, end=" ")
        root = None
        return root

    # Metoda - wypisanie poddrzewa od danej wartości metodą pre-order
    def printSubTree(self, root, key):
        if root is None or root.key == key:
            self.preOrder(root)
        elif root.key < key:
            self.printSubTree(root.right, key)
        else:
            self.printSubTree(root.left, key)

    # Metoda - graficzna reprezentacja drzewa
    def visualPrint(self, currPtr, indent, last):
        if currPtr != None:
            print(indent, end="")
            if last:
                print("R----", end="")
                indent += "     "
            else:
                print("L----", end="")
                indent += "|    "
            print(currPtr.key)
            self.visualPrint(currPtr.left, indent, False)
            self.visualPrint(currPtr.right, indent, True)


bst = BST()
avl = AVL()

print("Constructing a tree test [Y/n]")
tmp1 = input()
print("Searching minimum test [Y/n]")
tmp2 = input()
print("In-order search [Y/n]")
tmp3 = input()
print("BST balancing [Y/n]")
tmp4 = input()

# Tworzenie struktury
if tmp1.upper() == "Y":
    table = [["", "BST", "AVL"]]
    for i in range(1000, 10001, 1000):
        result1, result2 = 0, 0
        arr = [x for x in range(i-1, -1, -1)]
        for _ in range(100):
            start = timer()
            root = bst.insertArr(None, arr)
            end = timer()
            result1 += (end-start)*1000
            start = timer()
            root = avl.insertArr(None, arr, False)
            end = timer()
            result2 += (end-start)*1000
        result1 /= 100
        result2 /= 100
        table.append([str(i), str(result1), str(result2)])
        print(i)
    print(tabulate(table, tablefmt="fancy_grid"))

# Minimum
if tmp2.upper() == "Y":
    table = [["", "BST", "AVL"]]
    for i in range(10000, 100001, 10000):
        result1, result2 = 0, 0
        arr = [x for x in range(i-1, -1, -1)]
        root1 = bst.insertArr(None, arr)
        root2 = avl.insertArr(None, arr, False)
        for _ in range(100):
            start = timer()
            bst.minValue(root1)
            end = timer()
            result1 += (end-start)*1000
            start = timer()
            avl.minValue(root2)
            end = timer()
            result2 += (end-start)*1000
        result1 /= 100
        result2 /= 100
        table.append([str(i), str(result1), str(result2)])
        print(i)
    print(tabulate(table, tablefmt="fancy_grid"))

# In-order (no print)
if tmp3.upper() == "Y":
    table = [["", "BST", "AVL"]]
    for i in range(10000, 100001, 10000):
        result1, result2 = 0, 0
        arr = [x for x in range(i-1, -1, -1)]
        root1 = bst.insertArr(None, arr)
        root2 = avl.insertArr(None, arr, False)
        for _ in range(100):
            start = timer()
            bst.inOrderNoPrint(root1)
            end = timer()
            result1 += (end-start)*1000
            start = timer()
            avl.inOrderNoPrint(root2)
            end = timer()
            result2 += (end-start)*1000
        result1 /= 100
        result2 /= 100
        table.append([str(i), str(result1), str(result2)])
        print(i)
    print(tabulate(table, tablefmt="fancy_grid"))

# BST balance
if tmp4.upper() == "Y":
    table = [["", "BST"]]
    for i in range(10000, 100001, 10000):
        result = 0
        arr = [x for x in range(i-1, -1, -1)]
        root = bst.insertArr(None, arr)
        for _ in range(100):
            start = timer()
            root = bst.balanceTree(root)
            end = timer()
            result += (end-start)*1000
        result /= 100
        table.append([str(i), str(result)])
        print(i)
    print(tabulate(table, tablefmt="fancy_grid"))
