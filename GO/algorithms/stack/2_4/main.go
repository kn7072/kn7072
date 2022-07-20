package main

import (
	"fmt"
)

func SortStack(barrier int, originStack *Stack) *Stack{
	sortedStack := new(Stack)
	node := originStack.Head
	for node != nil {
		if node.Value < barrier {
			sortedStack.Push(node.Value)
		} else {
			sortedStack.PushDown(node.Value)
		}
		node = node.Next
	}
	return sortedStack
}

func main() {
	fmt.Println()

	firstStack := new(Stack)
	firstStack.Push(3)
	firstStack.Push(5)
	firstStack.Push(8)
	firstStack.PushDown(100)
	firstStack.Push(5)
	firstStack.Push(10)
	firstStack.Push(2)
	firstStack.Push(1)
	firstStack.PushDown(20)
	firstStack.PushDown(0)


	//firstStack.PrintStack()

	res := SortStack(5, firstStack)
	res.PrintStack()
}