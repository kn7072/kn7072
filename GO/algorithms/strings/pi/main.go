package main

import (
	"fmt"
)

func KMPMathcher(t, p string) {
	runT := []rune(t)
	runP := []rune(p)
	lenT := len(runT)
	pPi := pi(p)
	lenP := len(pPi)
	q := 0 // количество совпадающих символов

	for i := 0; i < lenT; i++ { // сканирование текста слева направо
		for q > 0 && runP[q+1] != runT[i] {
			q = pPi[q] // следующий символ не совпадает
		}
		
		if runP[q+1] == runT[i] {
			q += 1
		}
		if q == lenP {
			fmt.Printf("Образец находится со смещение %v\n", i - lenP)
			q = pPi[q]
		}
	}
}

func KMPMathcher2(s, sub string) []int{
	str := sub + "@" + s
	lenSubRune := len([]rune(sub))
	result := make([]int, 0)
	piStr := pi(str)
	for i, v := range piStr {
		if v == lenSubRune {
			result = append(result, i - 2 * lenSubRune)
		}
	}
	return result
}

func pi(str string) []int {
	runeS := []rune(str)
	lenS := len(runeS)
	pi := make([]int, len(runeS))
	for i := 1; i < lenS; i++ { // ищем pi-функцию до i индекса
		p := pi[i-1]

		if p == 0 && runeS[i] == runeS[0]{
			// если pi[i-1] = 0, значит pi[i] может быть только 1 если символ совпадает с нулевым символом строки
			pi[i] = 1
			continue
		}

		for p > 0 {
			// пытаемся найти максимальное pi
			if runeS[i] == runeS[pi[i-1]]{
				pi[i] = pi[i-1] + 1
				break
			} else {
				p = pi[pi[i-1]-1]  // pi содержит количество символов для указанного индекса, 
			}
		}

		if p == 0 && runeS[i] == runeS[0]{
			pi[i] = 1
		}

	}
	return pi
}

func main() {
	data := "Yaxy@abaYaxyzabaYaYaxy"//"abaYaxyzabaYaYaxy"
	res := pi(data)
	fmt.Println(res)

	subStr := "Yaxy"
	res = KMPMathcher2(data, subStr)
	fmt.Println(res)
}
