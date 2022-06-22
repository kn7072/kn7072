package main

import (
	"fmt"
)

func orDone(
	done <-chan interface{},
	ch <-chan interface{},
) <-chan interface{} {
	valStream := make(chan interface{})

	go func() {
		defer close(valStream)
		for {
			select {
			case <-done:
				fmt.Println("Done close 1")
				return
			case v, ok := <- ch:
				if !ok {
					fmt.Println("Done channel is closed")
					return
				} else {
					fmt.Println(v)
				}
				select {
				case <- done:
					fmt.Println("Done close 1")
					//https://translated.turbopages.org/proxy_u/en-ru.ru.3b794bdd-62976ccb-b9112e93-74722d776562/https/stackoverflow.com/questions/60491622/why-does-this-ordone-channel-implementation-receive-twice-from-done-channel
				case valStream <- v:
				}
			}
		}
	}()

	return valStream
}



func bridge(
	done <-chan interface{},
	chanStream <-chan <-chan interface{},
) <-chan interface{} {
	valStream := make(chan interface{})
	
	go func(){
		defer close(valStream)
		for {
			var stream <-chan interface{}
			select {
			case maybeStream, ok := <- chanStream:
				if !ok {
					return
				}
				stream = maybeStream
			case <- done:
				return	
			}
			for val := range orDone(done, stream) {
				select {
				case valStream <- val:
				case <- done:
				}
			}
		}
	}()

	return valStream
}