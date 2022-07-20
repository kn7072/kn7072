package main

import (
	"fmt"
	"queue1/queue"

)

func main() {
	fmt.Println()
	queue := queue.NewQueue()
	queue.Push(1)
	//queue.Print()

	queue.Push(2)
	//queue.Print()

	queue.Push(5)
	//queue.Print()

	queue.Pop()
	queue.Pop()
	//queue.Print()

	queue.Push(100)
	queue.Print()
}