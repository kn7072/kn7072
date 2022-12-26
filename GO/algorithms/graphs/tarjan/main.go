package main

// https://habr.com/ru/post/100953/

import (
	"1/stack"
	"fmt"
	"strconv"
	"log"
)

var Stack *stack.Stack

func dfs(nodeName string, hash map[string]struct{}) {
	if _, ok := hash[nodeName]; !ok {
		hash[nodeName] = struct{}{}
		next, err :=  strconv.Atoi(nodeName)
		if err != nil {
			log.Panicf("Не преобразуется к int %v", nodeName)
		}
		for _, next := range G[next - 1].Next { // next - 1 так как вершины нумеруются с 1 а в срезе нумерация с 0
			dfs(next, hash)
		}
		Stack.Push(nodeName)
	} else {
		panic("Цыкл")
	}
}


func main() {
	Stack = stack.NewStack()
	dfs("1", map[string]struct{}{})
	
	Stack.PrintStack()
	
	//переименуем вершины
	newName := make(map[string]string, len(G))
	i := 1
	for {
		if v, ok := Stack.Pop(); ok {
			newName[v] = strconv.Itoa(i)
			i++
		} else {
			goto exitFor
		}
	}
	exitFor:
	
	for j, node := range G {
		fmt.Println(node.NodeName)
		G[j].NodeName = newName[node.NodeName]
		if node.Next != nil {
			newNext := make([]string, len(node.Next))
			for i, v := range node.Next {
				newNext[i] = newName[v]
			}
			G[j].Next = newNext
		}
	}
	
	G.PringGraph()
	fmt.Println()
}