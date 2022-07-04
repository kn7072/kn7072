package main

import (
	"fmt"
	"math"
)

const (
    UPPER  = 1<<iota // upper case
    LOWER            // lower case
    CAP              // capitalizes
    REV              // reverses
)

const INF int64  = math.MaxInt64

func build_tree(vector []int64) {
	logLen := int(math.Log2(float64(len(vector))))
	lenVector := len(vector)
	sizeLog := logLen
	if len(vector) > int(1 << logLen) {
		sizeLog = logLen + 1
	}
	size := int(1 << sizeLog) * 2
	tree := make([]int64, size)
	for i :=0; i < size; i++ {
		tree[i] = INF
	}

	// инициализируем листья
	middleIndex := size / 2
	for i := 0; i < lenVector; i++ {
		tree[middleIndex + i] = vector[i]
	}
	
	// и все остальные вершины
	for i := middleIndex - 1; i >= 0; i-- {
		tree[i] = int64(math.Min(float64(tree[2 * i]), float64(tree[2 * i + 1])))
	}
	
	fmt.Println(tree)
}


func main() {
	//fmt.Println(INF)
	//fmt.Println(UPPER, CAP, REV)
	testData := []int64{1, 2, 3, 4, 5, 6, 7, 8, 9}
	build_tree(testData)
}