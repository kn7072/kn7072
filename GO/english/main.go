package main

import (
	"fmt"
	//"os"
	"english/config"
)

func main() {

	// data, err := os.ReadFile("/home/stepan/GIT/kn7072/ANKI/WORDS/a/accommodation.json")
	// if err != nil {
	// 	fmt.Println(data)
	// }

	fmt.Println(AW.m["dog"].Translate)
	fmt.Println(config.ConfReader.GetAllKeys())

	mapExistsWords, mapAdditionalWords := getMapsWordsFromSentence()
	createFileForAddSentence(mapExistsWords, mapAdditionalWords)

	var allSentenceObject = generateObjectAllSentence(AW)
	v, ok := allSentenceObject["Sadly, she inherited none of her father's musical talent."]
	fmt.Println(v, ok)
	allSentence(allSentenceObject)

	// pathEng := "/home/stepan/GIT/kn7072/EnglishSimulate/Project/VERB_NON_FINITE_FORMS/INFINITIVE_ENG_PRINT.txt"
	// pathRus := "/home/stepan/GIT/kn7072/EnglishSimulate/Project/VERB_NON_FINITE_FORMS/INFINITIVE_RUS_PRINT.txt"
	// pathResult := "/home/stepan/TEST_VIM/INFINITEVE_RESULT.txt"

	// pathEng := "/home/stepan/GIT/kn7072/EnglishSimulate/Project/VERB_NON_FINITE_FORMS/GERUND_ENG_PRINT.txt"
	// pathRus := "/home/stepan/GIT/kn7072/EnglishSimulate/Project/VERB_NON_FINITE_FORMS/GERUND_RUS_PRINT.txt"
	// pathResult := "/home/stepan/TEST_VIM/GERUND_RESULT.txt"

	// pathEng := "/home/stepan/GIT/kn7072/EnglishSimulate/Project/VERB_NON_FINITE_FORMS/PARTICIPLE_ENG_PRINT.txt"
	// pathRus := "/home/stepan/GIT/kn7072/EnglishSimulate/Project/VERB_NON_FINITE_FORMS/PARTICIPLE_RUS_PRINT.txt"
	// pathResult := "/home/stepan/TEST_VIM/PARTICIPLE_RESULT.txt"

	pathEng := "/home/stepan/GIT/kn7072/EnglishSimulate/Project/Preposition/EXERCISE_ENG.txt"
	pathRus := "/home/stepan/GIT/kn7072/EnglishSimulate/Project/Preposition/EXERCISE_RUS.txt"
	pathResult := "/home/stepan/TEST_VIM/PREPOSIION_RESULT.txt"

	convertNotFinteForms(pathEng, pathRus, pathResult)
}
