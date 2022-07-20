package main

import (
	"fmt"
)

func getPath(data [][]string) [][]string {
	lenRows := len(data)
	lenColumns := len(data[0])
	f := make([][]string, lenRows)
	
	for i, _ := range data {
		f[i] = make([]string, lenColumns)
	}
	// заполняем первую строку и первый столбец
	for i := 1; i < lenColumns; i++ {
		if data[0][i] == "0" {
			f[0][i] = ">"
		} else {
			break
		}
	}

	for i := 1; i < lenRows; i++ {
		if data[i][0] == "0" {
			f[i][0] = "v"
		} else {
			break
		}
	}

	for j := 1; j < lenRows; j++ {
		for i := 1; i < lenColumns; i++ {
			if data[j][i] == "0" {
				res := ""
				if data[j-1][i] == "0" {
					res += "v"
				}
				if data[j][i-1] == "0" {
					res += ">"
				}
				f[j][i] = res
			}
		}
	}
	return f
}

func Print(data [][]string) {
	for _, row := range data {
		for _, columnV := range row {
			if columnV == "" {
				fmt.Printf("%v", " ")
			} else {
				fmt.Printf("%v", columnV)
			}
			
		}
		fmt.Println()
	}
}

func main() {
	data := [][]string{ {"0", "0", "0", "0", "1", "0"},
						{"0", "0", "0", "0", "1", "0"},
						{"1", "0", "1", "0", "0", "0"},
						{"0", "0", "0", "0", "1", "1"},
						{"1", "0", "0", "0", "1", "0"},
	}
	f := getPath(data)
	Print(f)
}