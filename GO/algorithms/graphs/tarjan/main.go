package main

import (
	"1/stack"
	"fmt"
)

var Stack *stack.Stack

func dfs(nodeName string, hash map[string]struct{}) {
	if _, ok := hash[nodeName]; !ok {
		hash[nodeName] = struct{}{}
		for _, next := range Graph[nodeName].Next {
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
	fmt.Println()
}