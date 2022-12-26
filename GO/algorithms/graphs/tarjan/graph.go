package main

import (
	"fmt"
)

type Node struct {
	NodeName string
	Next []string
}

type Graph []Node
var G Graph


func (g Graph) PringGraph() {
	for _, v := range g {
		fmt.Printf("NodeName %v parents %+v\n", v.NodeName, v.Next)
	}
}

func init() {
	G = Graph{{NodeName: "1", Next: []string{"4"}},
	                {NodeName: "2", Next: nil},
				    {NodeName: "3", Next: nil},
				    {NodeName: "4", Next: []string{"2", "3"}},
	}
}