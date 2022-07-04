package main

import (
	"1/stack"
	"fmt"
)

func main() {

	b := stack.Push(1)
	fmt.Println(b)

	b = stack.Push(2)
	fmt.Println(b)

	v, b := stack.Pop()
	fmt.Printf("%v %v\n", v, b)

	v, b = stack.Pop()
	fmt.Printf("%v %v\n", v, b)

	v, b = stack.Pop()
	fmt.Printf("%v %v\n", v, b)
} 