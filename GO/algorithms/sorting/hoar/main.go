package main

import (
	"fmt"

)


func hoar(sliceSorted []int) []int {
	result := make([]int, 0, len(sliceSorted))
	if len(sliceSorted) == 1 {
		return sliceSorted
	}
	if len(sliceSorted) == 0 {
		return []int{}
	}

	lowBarier := make([]int, 0)
	highBarier := make([]int, 0)
	barier := sliceSorted[0]
	equalBarier := make([]int, 0)
	for _, v := range sliceSorted {
		switch {
		case v < barier:
			lowBarier = append(lowBarier, v)
		case v == barier:
			equalBarier = append(equalBarier, v)
	    default:
			highBarier = append(highBarier, v)
		}
	}
	lowBarier = hoar(lowBarier)
	highBarier = hoar(highBarier)

	result = append(result, lowBarier...)
	result = append(result, equalBarier...)
	result = append(result, highBarier...)
	return result
}

func main() {
	test := []int{2, 3, 1, 5}
	result := hoar(test)
	fmt.Printf("%v\n", result)
}