package main

type Node struct {
	Number int
	Neighbors []int
}

var (
	Graph = make(map[int]Node)
)

func init() {
	Graph[0] = Node{Number: 0, Neighbors: []int{18, 1, 14}}
	Graph[1] = Node{Number: 1, Neighbors: []int{0, 2, 15, 14}}
	Graph[2] = Node{Number: 2, Neighbors: []int{1, 3, 15, 17}}
	Graph[3] = Node{Number: 3, Neighbors: []int{2, 4, 7}}
	Graph[4] = Node{Number: 4, Neighbors: []int{3, 6, 5}}
	Graph[5] = Node{Number: 5, Neighbors: []int{4}}
	Graph[6] = Node{Number: 6, Neighbors: []int{4}}
	Graph[7] = Node{Number: 7, Neighbors: []int{3, 8, 9}}
	Graph[8] = Node{Number: 8, Neighbors: []int{7}}
	Graph[9] = Node{Number: 9, Neighbors: []int{7, 10}}
	Graph[10] = Node{Number: 10, Neighbors: []int{9, 11, 12}}
	Graph[11] = Node{Number: 11, Neighbors: []int{10}}
	Graph[12] = Node{Number: 12, Neighbors: []int{10, 13, 14}}
	Graph[13] = Node{Number: 13, Neighbors: []int{12}}
	Graph[14] = Node{Number: 14, Neighbors: []int{0, 1, 15, 16, 12}}
	Graph[15] = Node{Number: 15, Neighbors: []int{1, 2, 14}}
	Graph[16] = Node{Number: 16, Neighbors: []int{14}}
	Graph[17] = Node{Number: 17, Neighbors: []int{2}}
	Graph[18] = Node{Number: 18, Neighbors: []int{0}}

	Graph[100] = Node{Number: 100, Neighbors: []int{101}}
	Graph[101] = Node{Number: 101, Neighbors: []int{100}}

	Graph[102] = Node{Number: 102, Neighbors: []int{}}

}
