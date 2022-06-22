package main

import (
	"fmt"
	"time"
)

func multiply(done <-chan struct{}, ch <-chan int, multiplayer int) <-chan int {
	result := make(chan int)
	go func() {
		defer close(result)
		for i:= range ch {
			select {
			case result <- i * multiplayer:
			case <-done:
				return
			}
		}
	}()
	return result
}

func sum(done <-chan struct{}, ch <-chan int, x int) <-chan int {
	result := make(chan int)

	go func() {
		defer close(result)
		for i:= range ch {
			select {
			case <- done:
				return
			case result <- i + x:
			}
		}
	}()
	return result
}

func generator(done <-chan struct{}, integers ...int) <-chan int {
	intStream := make(chan int)

	go func() {
		defer close(intStream)
		for _, i := range integers {
			time.Sleep(time.Millisecond * 500)
			select {
			case <-done:
				return
			case intStream <- i:
			}
		}
	}()

	return intStream
}

func main() {
	dataSlice := []int{1, 2, 3, 4, 5, 6, 7}
	done := make(chan struct{})
	ch := generator(done, dataSlice...)
	// ch := make(chan int)
	// go func() {
	// 	defer close(ch)
	// 	for _, i := range dataSlice {
	// 		ch <- i
	// 		time.Sleep(time.Millisecond * 500)
	// 	}
	// }()
	
	go func(done chan struct{}, duration time.Duration) {
		defer close(done)
		time.Sleep(duration)
	}(done, time.Second * 3)
	
	result := sum(done, multiply(done, sum(done, ch, 2), 2), 1)
	for i := range result {
		fmt.Println(i)
	}
}