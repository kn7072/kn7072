package main

import (
	"fmt"
	"math/rand"
	"time"
)

// если закрывается канал done или канал с -
// закрываем канал valStream
func orDone(
	done <-chan interface{},
	ch <-chan int,
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

func generate(done <-chan interface{}) <-chan int {
	ch := make(chan int)

	go func ()  {
		defer close(ch)
		for {
			time.Sleep(time.Millisecond * 300)
			select {
			case <- done:
				return
			case ch <- rand.Intn(100):	
			}
		}
	}()

	return ch
}

func read(ch <-chan interface{}) {
	for {
		select {
		case v, ok := <- ch:
			if !ok {
				return
			}
			fmt.Println(v)
		}
	}
}

func main() {
	doneGenerage := make(chan interface{})
	done := make(chan interface{})
	testChan := generate(doneGenerage)
	orChan := orDone(done, testChan)
	go read(orChan)

	time.Sleep(time.Second * 1)
	//close(doneGenerage) // закрываем канал чтения
	close(done) // закрываем done канал orDone
	time.Sleep(time.Second * 3)
}