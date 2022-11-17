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

	// var allSentenceObject = generateObjectAllSentence(AW)
	// v, ok := allSentenceObject["Sadly, she inherited none of her father's musical talent."]
	// fmt.Println(v, ok)
	// allSentence(allSentenceObject)

	pathEng := "/home/stapan/GIT/kn7072/EnglishSimulate/Project/VERB_NON_FINITE_FORMS/INFINITIVE_ENG_PRINT.txt"
	pathRus := "/home/stapan/GIT/kn7072/EnglishSimulate/Project/VERB_NON_FINITE_FORMS/INFINITIVE_RUS_PRINT.txt"
	pathResult := "/home/stapan/TEST_VIM/INFINITEVE_RESULT.txt"

	convertNotFinteForms(pathEng, pathRus, pathResult)
}