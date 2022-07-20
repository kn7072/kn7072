package main

import (
	"fmt"
)
 
func bitSwapRequired(a, b int) int {
	count := 0
	for c := a ^ b; c != 0; c = c >> 1 {
		count += c & 1
	}
	return count
}

func main() {
	a := 29
	b := 15
	fmt.Printf("a %b, b %b \n", a, b)
	res := bitSwapRequired(a, b)
	fmt.Println(res) // 2
}