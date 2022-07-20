package main

import (
	"fmt"
	"math"
)

type Node struct {
	Min, Max, L, R int64
}

var data []int64
var tree []Node

func buildTree(m []int64) []Node {
	lenM := len(m)
	log2 := int(math.Log2(float64(lenM)))
	sizeTree := lenM
	if math.Pow(2, float64(log2)) < float64(lenM) {
		sizeTree = int(math.Pow(float64(log2 + 1), 2))
	}
	tree := make([]Node, 2  * sizeTree)
	
	j := 0
	for i := sizeTree / 2 - 1; i < sizeTree; i++ {
		if j < lenM {
			tree[i] = Node{Min: m[j], Max: m[j], L: int64(i), R: int64(i + 1)}
		} else {
			tree[i] = Node{Min: math.MaxInt64, Max: math.MinInt64, L: int64(i), R: int64(i + 1)}
		}
		j++
	}

	return tree
}


func buildRecursive(index int) { // нумерация вершин с 1, чтобы просчитывать дочерних элементов
	if index * 2 + 1 < len(tree) {
		// если есть правый дочерний элемент
		buildRecursive(2 * index)  // left
		buildRecursive(2 * index + 1) // right
		// fmt.Printf("i %v, left %v, right %v, min_left %v min_right %v, max_left %v, max_right %v\n", 
		// index, 
		// 2 * index, 
		// 2 * index + 1, 
		// tree[2 * index - 1].Min, 
		// tree[2 * index].Min,
		// tree[2 * index - 1].Max, 
		// tree[2 * index].Max, 
		// )
		
		tree[index-1] = Node{Max: int64(math.Max(float64(tree[2 * index - 1].Max), float64(tree[2 * index].Max))),
			                 Min: int64(math.Min(float64(tree[2 * index - 1].Min), float64(tree[2 * index].Min))),
							 L: tree[2 * index - 1].L,
							 R: tree[2 * index].R}
	} else {
		// листья
		if index - 1 < len(tree) / 2 + len(data) - 1 {
			// это реальные данные массива
			//fmt.Printf("index tree %v, %v\n", index-1, data[index - len(tree) / 2])
			tree[index-1] = Node{Max: data[index - len(tree) / 2],
								 Min: data[index - len(tree) / 2],
								 L: int64(index - len(tree) / 2),
								 R: int64(index - len(tree) / 2),
								}
		} else {
			tree[index-1] = Node{Max: math.MinInt64,
								 Min: math.MaxInt64,
								 L: int64(index) - int64(len(tree) / 2),
								 R: int64(index) - int64(len(tree) / 2),
							}
			// fmt.Println(tree[index - 1])
		}
	}
}

func get_min(currentNode Node, l, r int64) int64 {
	 

	if l == r {
		return tree[l].Min
	}


	if l == currentNode.L && r == currentNode.R {
		return currentNode.Min
	}

	if l >= currentNode.L && r <= currentNode.R {
		// искомый интервал полностью помещается в отрезок currentIndex
		//intetvalSub := currentNode.R / currentNode.L
		
		lResult := get_min(tree[currentNode.L * 2 + 1], l, r)
		rResult := get_min(tree[currentNode.R * 2 + 2], l, r)
		return int64(math.Min(float64(lResult), float64(rResult)))
	}

	if l > currentNode.R || r < currentNode.L {
		// искомый отрезор нахотися за пределами currentNode
		return math.MaxInt64
	}

	if l >= currentNode.L {
		// искомый отрезок смещен вправо относительно currentNode
		lResult := get_min(tree[currentNode.L * 2 + 1], l, currentNode.R)
		rResult := get_min(tree[currentNode.R * 2 + 2], l, currentNode.R)
		return int64(math.Min(float64(lResult), float64(rResult)))
	}
	if r <= currentNode.R {
		// искомый отрезок смещен влево относительно currentNode
		lResult := get_min(tree[currentNode.L * 2 + 1], currentNode.L, r)
		rResult := get_min(tree[currentNode.R * 2 + 2], currentNode.L, r)
		return int64(math.Min(float64(lResult), float64(rResult)))

	}
	return math.MaxInt64
}

func PrintTree() {
	for _, n := range tree {
		fmt.Printf("Max %v, Min %v, L %v, R %v\n", n.Max, n.Min, n.L, n.R)
	}
}

func main() {
	data = []int64{3, 1, 2} //, 4, 6, 9, 10, 3, 8, 7

	lenM := len(data)
	log2 := int(math.Log2(float64(lenM)))
	sizeTree := lenM
	if math.Pow(2, float64(log2)) < float64(lenM) {
		sizeTree = int(math.Pow(float64(log2 + 1), 2))
	}
	tree = make([]Node, 2  * sizeTree)

	buildRecursive(1)
	PrintTree()

	//buildTree(data)
	fmt.Println()
	get_min(tree[0], 0, 1)
}