package main

import (
	"fmt"
)

type Data []int

func search(data *Data, element int) (int, error) {
	if len(*data) == 0 {
		return 0, fmt.Errorf("data is empty")
	}
	left := 0
	right := len(*data)-1
	for {
		middleIndex := left + ((right - left) / 2)

		switch {
		case element > (*data)[middleIndex]:
			left = middleIndex
		case element < (*data)[middleIndex]:
			right = middleIndex
		default:
			return middleIndex, nil
		}

		if right - left == 1 {
			switch {
			case element == (*data)[left]:
					return left, nil
			case element == (*data)[right]:
					return right, nil
			default:
				return 0, fmt.Errorf("element %v not found", element)
			}
			
		}
	}
}

func main() {
	element := 1// 1 8 3
	data := Data{1, 2, 3, 4, 5, 6, 7, 8}
	index, ok := search(&data, element)
	fmt.Printf("%v, %v", index, ok)
}