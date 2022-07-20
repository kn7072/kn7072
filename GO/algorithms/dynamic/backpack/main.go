package main

import (
	"fmt"
	"math"
)


type Good struct {
	Value, Size int
}

var SizeBackPack int
var Goods = make(map[int]Good)
var F [][]int


func PrintF() {
	for _, i := range F {
		for _, j := range i {
			fmt.Printf("%v  ", j)
		}
		fmt.Println()
	}
}

func main() {
	fmt.Println()
	SizeBackPack := 7 + 1
	CountGoods := 4 + 1
	F = make([][]int, SizeBackPack)

	Goods[1] = Good{Value: 1, Size: 10}
	Goods[2] = Good{Value: 2, Size: 2}
	Goods[3] = Good{Value: 3, Size: 3}
	Goods[4] = Good{Value: 4, Size: 4}
	
	// заполняем F
	for i := 0; i < SizeBackPack; i++{
		F[i] = make([]int, CountGoods)
	}

	for i := 0; i < SizeBackPack; i++{
		F[i][0] = 0
	}

	for i := 0; i < CountGoods; i++ {
		F[0][i] = 0 // если размер рюзкака равен 0
	}

	
	for i := 1; i < CountGoods; i++ {
		for j := 1; j < SizeBackPack; j++ {
			prevSize := j - Goods[i].Size
			if prevSize >= 0 {
				F[j][i] = int(math.Max(float64(F[prevSize][i-1] + Goods[i].Value), 
											  float64(F[j][i-1])))
			} else {
				F[j][i] = 0
			}
			
		}
	}
	PrintF()

}