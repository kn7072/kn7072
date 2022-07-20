package queue

import (
	"fmt"
)

type QueueStuct struct {
	Head, Tail *Node
	Size int
}

type Node struct {
	Value int
	Next, Parent *Node
}

func NewQueue() *QueueStuct {
	return &QueueStuct{}
}

func (q *QueueStuct) Push(v int) bool {
	node := Node{Value: v}
	
	if q.Tail == nil {
		q.Head = &node
		q.Tail = &node
	} else {
		q.Tail.Next = &node
		node.Parent = q.Tail
		q.Tail = &node
		
	}
	q.Size++
	return true
}


func (q *QueueStuct) Pop() (int, bool) {
	if q.Head == nil {
		return 0, false
	} else {
		nodePop := q.Head
		q.Size--
		if q.Head.Next != nil {
			q.Head = q.Head.Next
			q.Head.Parent = nil
		} else {
			q.Head = nil
		}
		return nodePop.Value, true
	}
}

func (q *QueueStuct) Print() {
	start := q.Head
	for start != nil {
		fmt.Println(start.Value)
		start = start.Next
	}
}