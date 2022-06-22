package main

import (
	"sync"
)

func repeat(
	done <-chan struct{}, 
	values ...interface{},
) <-chan interface{} {
	valueStream := make(chan interface{})
	go func() {
		defer close(valueStream)
		for {
			for _, val := range values {
				select {
				case <- done:
					return
				case valueStream <- val:	
				}
			}
		}
	}()
	return valueStream
}

func take(
	done <-chan struct{}, 
	valueStream <-chan interface{},
	num int,
) <-chan interface{} {
	takeStream := make(chan interface{})
	go func (){
		defer close(takeStream)
		for i := 0; i < num; i++ {
			select {
			case <- done:
				return
			case takeStream <- <-valueStream:
			}
		}
	}()
	return takeStream
}

func repeatFn(
	done <-chan struct{},
	fn func() interface{},
) <-chan interface{} {
	valueStream := make(chan interface{})
	go func() {
		defer close(valueStream)
		for {
			select {
			case <- done:
				return
			case valueStream <- fn():
			}
		}
	}()
	return valueStream
}

func fanIn(
	done <-chan struct{},
	channels ...<-chan interface{},
) <- chan interface{} {
	var wg sync.WaitGroup
	multiplexedStream := make(chan interface{})

	multiplex := func(c <-chan interface{}) {
		defer wg.Done()
		for i := range c {
			select {
			case <- done:
				return
			case multiplexedStream <- i:
			}
		}
	}

	// Select from all the channels
	wg.Add(len(channels))
	for _, c := range channels {
		go multiplex(c)
	}

	// Wait for all the reads to complete
	go func() {
		wg.Wait()
		close(multiplexedStream)
	}()

	return multiplexedStream
}