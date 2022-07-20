package main

type Node struct {
	Name string
	Next []string
	Invert []string
}

var (
	Graph = make(map[string]Node)
)

func init() {
	Graph["A"] = Node{Name: "A", Next: []string{"B"},      Invert: []string{"C"}}
	Graph["B"] = Node{Name: "B", Next: []string{"C", "D"}, Invert: []string{"A"}}
	Graph["C"] = Node{Name: "C", Next: []string{"A"},      Invert: []string{"B"}}
	Graph["D"] = Node{Name: "D", Next: []string{"E"},      Invert: []string{"B", "F"}}
	Graph["E"] = Node{Name: "E", Next: []string{"F"},      Invert: []string{"D"}}
	Graph["F"] = Node{Name: "F", Next: []string{"D"},      Invert: []string{"E", "G"}}
	Graph["G"] = Node{Name: "G", Next: []string{"F", "H"}, Invert: []string{"J"}}
	Graph["H"] = Node{Name: "H", Next: []string{"I"},      Invert: []string{"G"}}
	Graph["I"] = Node{Name: "I", Next: []string{"J"},      Invert: []string{"H"}}
	Graph["J"] = Node{Name: "J", Next: []string{"G"},      Invert: []string{"I", "K"}}
	Graph["K"] = Node{Name: "K", Next: []string{"J"},      Invert: []string{}}
}
