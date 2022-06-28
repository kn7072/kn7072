package main

import (
	"fmt"
	//"os"
	"english/config"
)

func main() {

	// data, err := os.ReadFile("/home/stapan/GIT/kn7072/ANKI/WORDS/a/accommodation.json")
	// if err != nil {
	// 	fmt.Println(data)
	// }

	fmt.Println(AW.m["dog"].Translate)
	fmt.Println(config.ConfReader.GetAllKeys())
}