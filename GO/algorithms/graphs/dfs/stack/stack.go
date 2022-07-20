package stack

import "fmt"

type Node struct {
	Value int
	Next *Node
	Parrent *Node
}

type Stack struct {
	Head *Node
	Tail *Node
	Size int
}

func NewStack() *Stack {
	return &Stack{}
}


func (s *Stack) Push(v int) bool {
	newNode := &Node{Value: v}
	if s.Head == nil {
		// впервые кладем значение
		s.Head = newNode
		s.Tail = newNode
	} else {
		newNode.Next = s.Head  // новая нода становится головой
		s.Head.Parrent = newNode  // у старой головы появился родитель - новая нода
		s.Head = newNode
	}
	s.Size++
	return true
}

// добавляем значения снизу
func (s *Stack) PushDown(v int) bool {
	newNode := &Node{Value: v}
	if s.Head == nil {
		// впервые кладем значение
		s.Head = newNode
		s.Tail = newNode
	} else {
		newNode.Parrent = s.Tail
		s.Tail.Next = newNode
		s.Tail = newNode // новая нода становится хвостом
	}
	s.Size++
	return true
}

func (s *Stack) Pop() (int, bool) {
	if s.Head == nil {
		return 0, false
	} else {
		node := s.Head
		s.Head = node.Next
		if node.Next != nil {
			node.Next.Parrent = nil
		}
		
		s.Size--
		return node.Value, true
	}
}

func (s *Stack) PrintStack() {
	node := s.Head
	for node != nil {
		fmt.Println(node.Value)
		node = node.Next
	}
}
