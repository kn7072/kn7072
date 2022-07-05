package main

import (
	"fmt"
)

func gis(data []int) []int {
	result := make([]int, len(data))
	result[0] = 1

	for i := 1; i < len(data); i++ {
		m := 0
		for j := 0; j < i; j++ {
			if data[i] > data[j] && result[j] > m {
				m = result[j]
			}
		}
		result[i] = m + 1
	}
	return result
}

func main() {
	data := []int{5, 3, 2} //, 1, 2, 5
	res := gis(data)
	fmt.Println(res)
}