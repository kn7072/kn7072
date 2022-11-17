package main

import (
	"sync"
)

//https://habr.com/ru/post/338718/
type AllWords struct {
	mx sync.RWMutex
	m map[string]Word
}

func NewAllWords() *AllWords {
	return &AllWords{m: make(map[string]Word)}
}

func (alw *AllWords) Load(key string) (Word, bool) {
	alw.mx.RLock()
	defer alw.mx.RUnlock()
	val, ok := alw.m[key]

	return val, ok
}

func (alw *AllWords) Store(key string, word Word) {
	alw.mx.Lock()
	defer alw.mx.Unlock()
	alw.m[key] = word
}

// func (alw *AllWords) GetWordStar(coutStar int) <-chan string {
// 	for wordName, val := range alw {
// 		if val.m.
// 	}
// } 

var AW *AllWords = NewAllWords()

type Word struct {
	Translate string  `json:"translate"`
	Transcription string `json:"transcription"`
	Comment []string `json:"comment"`
	Antonyms []string `json:"antonyms"`
	Mnemonic []string `json:"mnemonic"`
	Examples []string `json:"examples"`
	Synonyms []string `json:"synonyms"`
	Grups []string `json:"grups"`
	Example_translate []string `json:"example_translate"`
	Stars int `json:"stars"`
}


type Sentence struct {
	mx sync.RWMutex
	eng string
	rus string
	words []string
}

func newSentence(eng, rus, word string) *Sentence {
	return &Sentence{eng: eng, rus: rus, words: []string{word}}
}

func (s *Sentence) updateWords(word string) {
	s.mx.RLock()
	defer s.mx.RUnlock()

	s.words = append(s.words, word)
}