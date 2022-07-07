package main

import (
	"fmt"
)

func pi(str string) []int {
	runeS := []rune(str)
	lenS := len(runeS)
	pi := make([]int, len(runeS))
	for i := 1; i < lenS; i++ { // ищем pi-функцию до i индекса
		// fmt.Println(string(runeS[i]))
		// if i == 6 {
		// 	fmt.Println()
		// }

		p := pi[i-1]
		if p == 0 && runeS[i] == runeS[0]{
			pi[i] = 1
			continue
		}

		for p > 0 {
			if runeS[i] == runeS[pi[i-1]]{
				pi[i] = pi[i-1] + 1
				break
			} else {
				p = pi[pi[i-1]]
			}
			
		}
	}
	return pi
}

func main() {
	data := "abaYaxyzabaYa"
	res := pi(data)
	fmt.Println(res)
}
