package main

import (
	"fmt"
)

type Node struct {
	Value, Count int64
	Parrent, Left, Right *Node
}

type Tree struct {
	root *Node
}




func buildTree(n *Node, v int64) {
	newNode := &Node{Value: v, Parrent: n, Count: 1}
	
	if n.Value == v {
		n.Count += 1
		return
	}
	
	if newNode.Value < n.Value {
		if n.Left == nil {
			n.Left = newNode
		} else {
			buildTree(n.Left, v)
		}
	} else {
		if n.Right == nil {
			n.Right = newNode
		} else {
			buildTree(n.Right, v)
		}
	}
}

// Кормен 321 - симметричный обход дерева
func inorderTree(n *Node) {
	if n != nil {
		inorderTree(n.Left)
		fmt.Printf("value %v count %v\n", n.Value, n.Count)
		inorderTree(n.Right)
	}
}

func treeSearch(n *Node, v int64) *Node {
	if n == nil || n.Value == v {
		return n
	}
	if v <= n.Value {
		return treeSearch(n.Left, v)
	} else {
		return treeSearch(n.Right, v)
	}
}

func treeSearchWhile(n *Node, v int64) *Node {
	for n != nil && n.Value != v {
		if v <= n.Value {
			n = n.Left
		} else {
			n = n.Right
		}
	}
	return n
}

func treeMin(n *Node) *Node {
	for n.Left != nil {
		n = n.Left
	}
	return n
}

// добавлелние элемента в дерово
func TreeInsert(t *Tree, z *Node) {
	y := new(Node)
	x := t.root
	for x != nil {
		y = x
		if z.Value <= x.Value {
			x = x.Left
		} else {
			x = x.Right
		}
	}
	switch {
	case y == nil:
		t.root = z
	case z.Value <= y.Value:
		y.Left = z
	case z.Value > y.Value:
		y.Right = z
	} 

}

func transplant(t *Tree, u, v *Node) {
	switch {
	case u.Parrent == nil:
		t.root = v
	case u == u.Parrent.Left:
		u.Parrent.Left = v
	default:
		u.Parrent.Right = v
	}
	
	if v != nil {
		v.Parrent = u.Parrent
	}
}

func tree_delete(t *Tree, z *Node) {
	switch {
	case z.Left == nil:
		transplant(t, z, z.Right)
	case z.Right == nil:
		transplant(t, z, z.Left)
	default:
		y := treeMin(z.Right)
		if y.Parrent != z {
			transplant(t, y, y.Right)
			y.Right = z.Right
			y.Right.Parrent = y
		}
		transplant(t, z, y)
		y.Left = z.Left
		y.Left.Parrent = y
	}
}


func main() {
	data := []int64{5, 6, 2, 7, 1, 0, -1, 7, 10, 4}
	root := &Node{Value: 4, Count: 1}
	tree := &Tree{root: root}

	for _, i := range data {
		buildTree(root, i)
	}
	inorderTree(root)

	if elem := treeSearch(root, 0); elem != nil {
		fmt.Println(elem.Value)
	}

	if elem := treeSearch(root, 11); elem != nil {
		fmt.Println(elem.Value)
	}

	if elem := treeSearchWhile(root, 0); elem != nil {
		fmt.Println(elem.Value)
	}

	// минимум в дереве
	elem := treeMin(root)
	fmt.Println(elem.Value)

	TreeInsert(tree, &Node{Value: 100})

	inorderTree(root)

}