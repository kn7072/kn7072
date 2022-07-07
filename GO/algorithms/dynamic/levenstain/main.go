package main

import (
	"fmt"
	"sort"
)

type F struct {
	Len int
	Action string
}

// 608
type FSlice []F

func (f FSlice) Len() int {
	return len(f)
}

func (f FSlice) Less(i, j int) bool {
	if f[i].Len < f[j].Len {
		return true
	}
	return false
}

func (f FSlice) Swap(i, j int) {
	f[i], f[j] = f[j], f[i]
}

func getMin(s ...F) F {
	sort.Sort(FSlice(s))
	return s[0]
}

func Print(data [][]F) {
	for _, row := range data {
		for _, col := range row {
			fmt.Printf("%v(%v) ", col.Len, col.Action)
		}
		fmt.Println()
	}
}


func levenstain(a, b string) {
	subA := []rune(a) // i
	subB := []rune(b) // j
	results := make([][]F, len(subB) + 1)
	for i := 0; i < len(results); i++ {
		results[i] = make([]F, len(subA) + 1)
	}

	for i := 0; i < len(subA) + 1; i++ {
		results[0][i] = F{Len: i, Action: "Add"}
	}
	for j := 0; j < len(subB) + 1; j++ {
		results[j][0] = F{Len: j, Action: "Add"}
	}
	results[0][0].Action = "Not"

	for j := 1; j < len(subB) + 1; j++ {
		for i := 1; i < len(subA) + 1; i++ {
			if subA[i-1] == subB[j-1] {
				results[j][i] = results[j-1][i-1]
			} else {
				minElement := getMin(results[j-1][i], results[j-1][i-1], results[j][i-1])
				results[j][i].Len =  minElement.Len + 1
				
				switch {
				case minElement == results[j-1][i-1]:
					results[j][i].Action = "Cha"
				case minElement == results[j-1][i]:
					results[j][i].Action = "Add"
				default:
					results[j][i].Action = "Del"
				}
				 
			}
		}
	} 

	Print(results)
}

func main() {
	a := "котик"
	b := "коржик"
	levenstain(a, b)
}