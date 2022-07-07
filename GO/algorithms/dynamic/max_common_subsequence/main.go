package main

import (
	"fmt"
)

type SubSequence struct {
	Len int
	Sequence string
}

func maxSubSequence(a,b SubSequence) SubSequence{
	if a.Len > b.Len {
		return a
	}
	return b
}

func gis(s1, s2 string) string {
	seq1 := []rune(s1)
	seq2 := []rune(s2)
	results := make([][]SubSequence, len(seq1) + 1)
	for i := 0; i < len(results); i++ {
		results[i] = make([]SubSequence, len(seq2) + 1)
	}
	
	for i := 1; i < len(seq1) + 1; i++ {
		for j := 1; j < len(seq2) + 1; j++ {
			if seq1[i-1] == seq2[j-1] {
				results[i][j].Len = results[i-1][j-1].Len + 1
				results[i][j].Sequence = results[i-1][j-1].Sequence + string(seq1[i-1])
			} else {
				results[i][j] = maxSubSequence(results[i-1][j], results[i][j-1])
			}
		}
	}
	return results[len(seq1)][len(seq2)].Sequence
}

func main() {
	s1 := "ACCGGTCGAGTGCGCGGAAGCCGGCCGAA"
	s2 := "GTCGTTCGGAATGCCGTTGCTCTGTAAA"
	res := gis(s1, s2)
	fmt.Println(res)  // GTCGTCGGAAGCCGGCCGAA
}
