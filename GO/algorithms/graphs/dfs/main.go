package main

import (
	"fmt"
	"dfs/stack"
)

var hash map[int]struct{}

func PrintTree(ostov []int) {
	for _, node := range ostov {
		fmt.Printf("%v, ", node)
	}
	fmt.Println()
}

func dfs(startName int, hash map[int]struct{}) []int {
	path := make([]int, 0)
	//hash := make(map[int]struct{})
	stack := stack.NewStack()
	stack.Push(startName)

	for {
		nodeTop, b := stack.Pop()
		if b {
			if _, ok := hash[nodeTop]; !ok {
				hash[nodeTop] = struct{}{}
				path = append(path, nodeTop)
				for _, j := range Graph[nodeTop].Neighbors {
					stack.Push(j)
				}
			}	
		} else {
			goto ef
		}
		}
	ef:
	return path
}

func main() {
	//fmt.Println(Graph)
	hash := make(map[int]struct{})
	
	countComponentRelations := 0
	for name, _ := range Graph {
		if _, ok := hash[name]; !ok {
			//hash[name] = struct{}{}
			path := dfs(name, hash)
			countComponentRelations++
			PrintTree(path)
			} else {
				continue
		}
		
	}
	fmt.Printf("\nCount component relation %v\n", countComponentRelations)
}