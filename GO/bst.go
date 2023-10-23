package main

import (
	"fmt"
	"time"
)

func Max(x, y int) int {
	if x < y {
		return y
	}
	return x
}

type Node struct {
	key    int
	left   *Node
	right  *Node
	height int
}

type BST struct {
	root *Node
}

type AVL struct {
	root *Node
}

// Node

func (node *Node) insert(data int) {
	if data <= node.key {
		if node.left == nil {
			node.left = &Node{key: data}
		} else {
			node.left.insert(data)
		}
	} else {
		if node.right == nil {
			node.right = &Node{key: data}
		} else {
			node.right.insert(data)
		}
	}
}

// Tree

func (tree *BST) insert(data int) {
	if tree.root == nil {
		tree.root = &Node{key: data}
	} else {
		tree.root.insert(data)
	}
}

func NewNode(key int) *Node {
	return &Node{
		key:    key,
		left:   nil,
		right:  nil,
		height: 1,
	}
}

func main() {
	for i := 10000; i <= 100000; i += 10000 {
		var result1 float64 = 0
		var result2 float64 = 0
		Arr := make([]int, i)
		for j := 0; j < i; j++ {
			Arr[j] = i - j - 1
		}
		bst := NewBST()
		bst.InsertArray(Arr)
		avl := NewAVL()
		avl.InsertArray(Arr)
		for k := 0; k < 10000; k++ {
			start := time.Now()
			bst.root.InOrder()
			duration := time.Since(start)
			result1 += float64(duration.Nanoseconds()) / 1000000.00
			start = time.Now()
			avl.root.InOrder()
			duration = time.Since(start)
			result2 += float64(duration.Nanoseconds()) / 1000000.00
		}
		result1 /= 10000.00
		result2 /= 10000.00
		fmt.Printf("%v elements: BST - %v ms, AVL - %v ms\n", i, result1, result2)
	}
}
