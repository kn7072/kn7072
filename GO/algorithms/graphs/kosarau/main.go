package main

import (
	"fmt"
	"kosarau/stack"
	"sort"
)

var hash map[string]struct{}
var hashReverse map[string]struct{}
var stackN *stack.Stack

var Start map[string]int
var End map[string]int

func PrintTree(ostov []int) {
	for _, node := range ostov {
		fmt.Printf("%v, ", node)
	}
	fmt.Println()
}

func dfsFillStack(startName string, hash map[string]struct{}){
	
	for {
		if _, ok := hash[startName]; !ok {
			stackN.Push(startName)
			hash[startName] = struct{}{}
			for _, j := range Graph[startName].Next {
				dfsFillStack(j, hash)
			}
		} else {
			return
		}

	}
}

func Mark() []string {
	result := make([]string, 0)
	for {
		if v, ok := stackN.Pop(); ok {
			result = append(result, v)
		} else {
			return result
		}
	} 
}

func dfs(nodeName string, hash map[string]struct{}) []string {
	result := make([]string, 0)
	steck := stack.NewStack()
	steck.Push(nodeName)

	hash[nodeName] = struct{}{}

	for {
		v, ok := steck.Pop()
		if !ok {
			return result
		} else {
			result = append(result, v)
			for _, nodeInvert := range Graph[v].Invert {
				if _, ok := hash[nodeInvert]; !ok {
					steck.Push(nodeInvert)
					hash[nodeInvert] = struct{}{}
				}
			}
		}
	}
}




// func dfsMark(nodeName string, in int, hash map[string]struct{}) int {
// 	if _, ok := hash[nodeName]; !ok {
// 		hash[nodeName] = struct{}{}
// 		in++
// 		Start[nodeName] = in
// 		for _, v := range Graph[nodeName].Next {
// 			in = dfsMark(v, in, hash)
// 		}
// 		in++
// 		End[nodeName] = in
// 	}
// 	return in
// }

type TimeNode struct {
	NodeName string
	Start, End int
}

type PairTimeNode []TimeNode
var xxx PairTimeNode = make(PairTimeNode, 0)

func (p PairTimeNode) Len() int { return len(p) }
func (p PairTimeNode) Less(i, j int) bool { return p[i].End > p[j].End }
func (p PairTimeNode) Swap(i, j int){ p[i], p[j] = p[j], p[i] }

func dfsMark(nodeName string, in int, hash map[string]struct{}) int {
	if _, ok := hash[nodeName]; !ok {
		hash[nodeName] = struct{}{}
		in++
		timeNode := TimeNode{Start: in, NodeName: nodeName}
	Start[nodeName] = in
		for _, v := range Graph[nodeName].Next {
			in = dfsMark(v, in, hash)
		}
		in++
	End[nodeName] = in
		timeNode.End = in
		xxx = append(xxx, timeNode)
	}
	return in
}


// func kosarau(hash map[string]struct{}) [][]string{
// 	result := make([][]string, 0)
// 	for {
// 		nodeName, ok := stackN.Pop()
// 		if !ok {
// 			goto exit
// 		} else {
// 			if _, ok := hash[nodeName]; !ok {
// 				fmt.Println(nodeName)
// 				result = append(result, dfs(nodeName, hash))
// 			}
// 		}
		
// 	}
// 	exit:
// 	return result
// }

// func kosarau(s []string, hash map[string]struct{}) [][]string{
// 	result := make([][]string, 0)
// 	for _, nodeName := range s {
// 		if _, ok := hash[nodeName]; !ok {
// 			fmt.Println(nodeName)
// 			result = append(result, dfs(nodeName, hash))
// 		}
// 	}
		
// 	return result
// }


func kosarau(hash map[string]struct{}) [][]string{
	result := make([][]string, 0)
	for _, node := range xxx {
		if _, ok := hash[node.NodeName]; !ok {
			fmt.Println(node.NodeName)
			result = append(result, dfs(node.NodeName, hash))
		}
	}
		
	return result
}

func main() {
	stackN = stack.NewStack()
	hash = make(map[string]struct{})
	hashReverse = make(map[string]struct{})

	Start = make(map[string]int)
	End = make(map[string]int)

	// заполнили стек узлами в порядке dfs
	
	for nodeName, _ := range Graph {
		dfsFillStack(nodeName, hash)
	}

	in := 0
	for nodeName, _ := range Graph {
		in = dfsMark(nodeName, in, hashReverse)
	}

	

	// t := []int{8, 1, 3, 0}
	// sort.Ints(t)

	
	sort.Sort(xxx)
	//sort.Reverse(xxx)
	res := kosarau(make(map[string]struct{}))


	// s := Mark()
	// fmt.Println(s)
	// res := kosarau(s, hashReverse)

	//res := kosarau(hashReverse)
	fmt.Println(res)

}