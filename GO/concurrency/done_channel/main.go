package main

import (
	"fmt"
	"time"
)

func readSelectCloseChan (ch <-chan interface{}) {
	count := 0
	for {
		select {
		case <- ch:
			count++
			if count == 2 {
				fmt.Println("readSelectCloseChan is finished")
				ch = nil
				//return
			}
		default:
			if ch == nil {
				return
			}
		}
	}
}

func main() {
	doWork := func(done <-chan interface{}, strings <-chan string) <-chan interface{}{
		terminated := make(chan interface{})
		count := 0
		go func() {
			defer fmt.Println("doWork exited")
			defer close(terminated)
			for {
				select {
				case s := <- strings:
					fmt.Println(s)
				case v, open := <- done:
					count++
					fmt.Println(v, open, count)
					if count == 3 {
						return
					}
				}
			}
		}()
		return terminated
	}

	done := make(chan interface{})
	terminated := doWork(done, nil)

	go func() {
		time.Sleep(1  * time.Second)
		fmt.Println("Canceling doWork goroutine...")
		close(done)
	}()

	<- terminated
	fmt.Println("Done.")
	go readSelectCloseChan(terminated)
	time.Sleep(time.Second * 20)

}
 