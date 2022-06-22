package main

func repeat(
	done <-chan interface{}, 
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
	done <-chan interface{}, 
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
	done <-chan interface{},
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


// tee := func(
// 	done <-chan interface{},
// 	in <-chan interface{},
// ) (_, _ <-chan interface{}) { <-chan interface{}) {
	
// 	out1 := make(chan interface{})
// 	out2 := make(chan interface{})
	
// 	go func() {
// 		defer close(out1)
// 		defer close(out2)
// 		for val := range orDone(done, in) {
// 			var out1, out2 = out1, out2
// 			for i := 0; i < 2; i++ {
// 				select {
// 				case <-done:
// 				case out1<-val:
// 					out1 = nil
// 				case out2<-val:
// 					out2 = nil
// 				}
// 			}
// 		}
// 	}()
// 	return out1, out2
// }	