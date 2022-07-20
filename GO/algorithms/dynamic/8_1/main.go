package main

import (
	"fmt"

)

func maxCountPathes(n int, sliceSteps []int) int {
	f := make([]int, n)
	f[0] = 1
	for i := 1; i < n; i++ {
		for _, step := range sliceSteps {
			if step <= i {
				f[i] += f[i - step]
			} else {
				break
			}
		}
	}
	return f[len(f) - 1]
}

func main() {
	n := 5
	sliceSteps := []int{1, 2, 3}
	res := maxCountPathes(n, sliceSteps)
	fmt.Println(res)
}