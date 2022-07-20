package main

type Node struct {
	NodeName string
	Next []string
}

var Graph map[string]Node


func init() {
	Graph = map[string]Node{"1": {NodeName: "1", Next: []string{"4"}},
	                        "2": {NodeName: "2", Next: []string{}},
				            "3": {NodeName: "3", Next: []string{}},
				            "4": {NodeName: "4", Next: []string{"2", "3"}},
	}
}