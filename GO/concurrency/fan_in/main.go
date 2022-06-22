package main

import (
	"fmt"
	"math/rand"
	"runtime"
	"time"
)

func main() {
	done := make(chan struct{})
	start := time.Now()
	defer close(done)

	for num := range take(done, repeat(done, 1, 2), 10) {
		fmt.Printf("%v \n", num)
	}

	rand := func() interface{} {return rand.Intn(1000)}
	for num := range take(done, repeatFn(done, rand), 10) {
		fmt.Printf("rand %v\n", num)
	}

	numFinders := runtime.NumCPU()
	fmt.Printf("Count NumCPU %v", numFinders)
	finders := make([]<-chan interface{}, numFinders)
	for i := 0; i < numFinders; i++ {
		finders[i] = take(done, repeatFn(done, rand), 10)
	}

	fmt.Println("Primes:")
	for prime := range take(done, fanIn(done, finders...), 10) {
		fmt.Printf("\t%d\n", prime)
	}

	fmt.Printf("Search took: %v", time.Since(start))
}