package main

import (
	"fmt"
	"time"
)

func main() {

	var or func(channels ...<-chan struct{}) <-chan struct{}
	or = func(channels ...<-chan struct{}) <-chan struct{} {
		orDone := make(chan struct{})
		
		switch len(channels){
		case 0:
			return nil
		case 1:
			return channels[0]	
		}

		go func() {
			defer close(orDone)
			switch len(channels) {
			case 2:
				select {
					case <-channels[0]:
					case <-channels[1]:
				}
			default:
				select {
					case <-channels[0]:
					case <-channels[1]:
					case <-channels[2]:
					case <- or(append(channels[3:], orDone)...):
				}
			}
		}()
		return orDone
	}

	createChan := func(t time.Duration) chan struct{} {
		ch := make(chan struct{})
		
		go func(){
			defer close(ch)
			time.Sleep(t)
		}()

		return ch
	}

	//done := make(chan struct{})
	start := time.Now()
	<- or(
		createChan(time.Second * 7),
		createChan(time.Second * 2),
		createChan(time.Second * 5),
		// createChan(time.Second * 5),
		// createChan(time.Second * 5),
	)
	fmt.Printf("done after %v\n", time.Since(start))

	//пример удаления элемента из среза
	tempSlice := []int{0, 1, 2, 3, 4, 5, 6, 7}
	indexDel := 2
	tempSlice = tempSlice[:indexDel + copy(tempSlice[indexDel:], tempSlice[indexDel + 1:])]
	fmt.Println(tempSlice)
}