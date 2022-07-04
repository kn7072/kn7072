package stack

type Node struct {
	Value int
	Next *Node
}

var size = 0
var Stack = new(Node)


func Push(v int) bool {
	if Stack == nil {
		Stack = &Node{Value: v}
		size = 1
		return true
	}
	Stack = &Node{Value: v, Next: Stack}
	size++
	return true
}

func Pop() (int, bool) {
	if size == 0 {
		return 0, false
	}

	elem := Stack
	Stack = Stack.Next
	size--
	return elem.Value, true
}