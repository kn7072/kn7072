package main

import (
	"fmt"
	"log"
	"os"
	"path"
	"runtime"
	"encoding/json"
	"sync"
	"sort"
	"strings"
	"bufio"
	"english/config"
	"io"
)

var (
	wordsToIgnore = []string{"the", "an", "a", "as", "she", "we", "you", "her", "he", "him", "on", "no", "off", "of",
	 "for", "is", "be",	"to", "not", "in", "his", "i", "it", "me", "my", "if", "am", "are", "was", "at", "this", "they",
	 "that", "then", "than", "do", "out", "go", "too", "with", "us", "our", "from", "have", "has", "all", "their", "so",
	 "and", "but", "can", "your", "were", "had", "being", "what", "why", "some", "use", "would", "could", "more", "very", 
	 "when", "even", "about", "many", "best", "alone", "such", "there", "one", "order", "enough", "over", "by",

	 "ann", "oleg", "olga", "din't", "don't", "tom", "mrs", "i'v", "u've", "it's", "teter", "must", "will", "nothing", 
	 "tv", "home", "girl", "look", "way", "late", "left", "right", "down", "day", "never", "time", "life", "take", "work", 
	 "car", "how", "water", "like", "mind", "help", "seems", "went"}

	replacerCharacters = []string{".", "", ",", "", "?", "", "!", "", "(", "", ")", "", "\n", ""}
)

func trimeSpaceSlice(slice *[]string) {
	for i, v := range *slice {
		(*slice)[i] = strings.TrimSpace(v)
	}
}


func getAllPathes(pathDir string) <-chan string {
	
	ch := make(chan string)
	chFinish := make(chan string, 2)
	root_dir := config.ConfReader.GetString("path.dir_all_word_files")

	var temp func(string)
	temp = func(pathDir string) {
		files, err := os.ReadDir(pathDir)
		chFinish <- pathDir
		if err != nil {
			log.Fatal(err)
		} else {
			for _, fileI := range files {
				if fileI.IsDir() {
					subpath := path.Join(root_dir, fileI.Name())
					temp(subpath)
				} else {
					pathToFile := path.Join(pathDir, fileI.Name())
					ch <- pathToFile
				}
			}
		}
		<- chFinish
		if len(chFinish) == 0 {
			close(ch)
			log.Print("getAllPathes finished")
			return
		}
	}
	go temp(pathDir)
	return ch
}

func generateObjectAllWords(wg *sync.WaitGroup, chPath<-chan string, allWords *AllWords) {
	defer wg.Done()
	for {
		select {
		case pathI, ok := <- chPath:
			{
				if !ok {
					return
				}
				//fmt.Println(pathI)
				data, err := os.ReadFile(pathI)
				if err==nil {
					if valid := json.Valid(data); valid {
						tempMap := map[string]interface{}{}
						if err := json.Unmarshal([]byte(data), &tempMap); err==nil {
							wordData := Word{}
							for nameWord, val := range tempMap {
								
								bytes, err := json.Marshal(val)
								if err==nil {
									if err := json.Unmarshal(bytes, &wordData); err==nil {
										allWords.Store(nameWord, wordData)
									} else {
										log.Fatal(err)
									}	
								} else {
									log.Fatal("Не смогли преобразовать данные в json")
								}
							}
						}
					} else {
						log.Fatal("Json in not valid")
					}
				}
			}	
		}	
	}
}

func init() {
	var logger = log.New(log.Writer(), "prefix: ",
					 	 log.Flags() | log.Lmsgprefix)

	root_dir := config.ConfReader.GetString("path.dir_all_word_files")
	logger.Printf("Invoked with %v values", "something to print")

	log.SetFlags(log.Lshortfile | log.Ltime)
	wg := &sync.WaitGroup{}
	chPath := getAllPathes(root_dir)
	fmt.Println(runtime.NumCPU())
    for i :=0; i < runtime.NumCPU(); i++ {
		wg.Add(1)
		go generateObjectAllWords(wg, chPath, AW)
	}
	wg.Wait()
}


func creteFileUniqueWords() {
	file, err := os.OpenFile(config.ConfReader.GetString("path.words_for_learn"),
							 os.O_RDONLY, 0755)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	reader := bufio.NewReader(file)
	tempMap := make(map[string]struct{})

	for {
		line, err := reader.ReadString('\n')

		line = strings.TrimSpace(line)
		if line == "##########" {
			continue
		} else {
			if _, ok := tempMap[line]; !ok {
				tempMap[line] = struct{}{}
			}
		}
		if err == io.EOF {
			break
		}
	}

	allWords := make([]string, 0, len(tempMap))
	for word, _ := range tempMap {
		allWords = append(allWords, word)
	}
	sort.Strings(allWords)

	fileOut, err := os.OpenFile(config.ConfReader.GetString("path.words_for_learn_clean"), 
								os.O_CREATE|os.O_RDWR, 0755)
	if err != nil {
		panic(err)
	}
	fileOut.Truncate(0)
	for word, _ := range tempMap {
		fileOut.WriteString(word + "\n")
	}
}


func differnceSlices(sliceOne, sliceTwo []string) []string {
	mOne := make(map[string]struct{}, len(sliceOne))
	diff := make([]string, 0)

	for _, vOne := range sliceOne {
		mOne[vOne] = struct{}{}
	}
	
	for _, vTwo := range sliceTwo {
        if _, found := mOne[vTwo]; !found {
            diff = append(diff, vTwo)
        }
    }

    return diff
}

// анализирует предложения
func createFileForAddSentence(mapExistsWords, mapAdditionalWords map[string][]string) {
	pathToFile := config.ConfReader.GetString("path.file_to_add_sentence")
	countSentenceForWord := config.ConfReader.GetInt("path.count_sentence_for_word")
	// tempADD := "%v %v %v %v\n"
	tempInfo := "%v %v\n"

	if file, errFile := os.OpenFile(pathToFile, os.O_CREATE|os.O_WRONLY, 0o555); errFile == nil {
		defer file.Close()

		for wordI, sentenceForWordI := range mapExistsWords {
			
			countSentenceWord := len(sentenceForWordI)
			if countSentenceWord < countSentenceForWord {
				// среди известных предложений, для слова wordI нашлось менее чем countSentenceForWord примеров
				
				// попробуем найти дополнительные примеры
				if sentenceAdditionalForWords, ok := mapAdditionalWords[wordI]; ok {
					lenAdditional := len(sentenceAdditionalForWords)
					if countSentenceWord + lenAdditional >= countSentenceForWord {
						// for _, sentenseI := range sentenceAdditionalForWords {
						// 	if _, err := file.WriteString(fmt.Sprintf(tempADD, wordI, "DONE", countSentenceWord+lenAdditional, sentenseI)); err != nil {
						// 		panic(err.Error())
						// 	}
						// }
					} else {
						// for _, sentenseI := range sentenceAdditionalForWords {
						// 	if _, err := file.WriteString(fmt.Sprintf(tempADD, wordI, "NEED ADD", countSentenceWord+lenAdditional, sentenseI)); err != nil {
						// 		panic(err.Error())
						// 	}
						// }
					}
				} else {
					if _, err := file.WriteString(fmt.Sprintf(tempInfo, wordI, countSentenceWord)); err != nil {
						panic(err.Error())
					}
				}
			}
			// if sentence, ok := wordsSentence[wordI]; ok {
			// 	if len(sentence) < countSentenceForWord {
			// 		if _, err := file.WriteString(wordI + "\n"); err != nil {
			// 			panic(err.Error())
			// 		}
			// 	}
			// } else {
			// 	if _, err := file.WriteString(wordI + "\n"); err != nil {
			// 		panic(err.Error())
			// 	}
			// }
		}
	} else {
		panic(errFile.Error())
	}
}

// анализирует файл Предложения.txt, считает сколько предложений приходится на каждое слово
func getMapsWordsFromSentence() (map[string][]string, map[string][]string) {
	result := make(map[string][]string)
	resultAdditional := make(map[string][]string)  // потенциальные кандидаты, слова к которым можно добавить предложение
	mapIgnoreWords := createIgnoreWordsMap(wordsToIgnore)
	replacer := strings.NewReplacer(replacerCharacters...)

	fillMap := func(sliceWords *[]string, mapToAdd map[string][]string, sentence, translate string) {
		for _, wordI := range *sliceWords {
			if _, ok := mapToAdd[wordI]; !ok {
				mapToAdd[wordI] = make([]string, 0)
			}

			mapToAdd[wordI] = append(mapToAdd[wordI], fmt.Sprintf("%s;%s", sentence, translate))
		}
	}
	
	pathToFileSentence := config.ConfReader.GetString("path.path_to_sentence")
	if file, errFile := os.OpenFile(pathToFileSentence, os.O_RDONLY, 0o755); errFile == nil {
		defer file.Close()
		reader := bufio.NewReader(file)

		for {
			line, errLine := reader.ReadString('\n')
			switch errLine {
			case nil:
				sliceW := strings.Split(line, ";")
				sentence := strings.TrimSpace(sliceW[1])
				translate := strings.TrimSpace(sliceW[2])
				tempWordsSlice := strings.Split(sliceW[0], ",")

				searchWordsIntoSentence := getWordsForSentence(sentence, replacer, mapIgnoreWords)
				
				trimeSpaceSlice(&tempWordsSlice)
				diffWords := differnceSlices(tempWordsSlice, searchWordsIntoSentence)

				fillMap(&tempWordsSlice, result, sentence, translate)
				fillMap(&diffWords, resultAdditional, sentence, translate)

				// for _, wordI := range tempWordsSlice {
				// 	if _, ok := result[wordI]; !ok {
				// 		result[wordI] = make([]string, 0)
				// 	}

				// 	result[wordI] = append(result[wordI], fmt.Sprintf("%s;%s", sentence, translate))
				// }

			case io.EOF:
				goto exit
			default:
				panic(errLine)
			}
		}
	} else {
		panic(errFile)
	}

exit:
	fmt.Println("Всего уникальных слов с примерами", len(result))

	return result, resultAdditional
}


func generateObjectAllSentence(allWord *AllWords) map[string]*Sentence {
	allWord.mx.RLock()
	defer allWord.mx.RUnlock()

	result := make(map[string]*Sentence)

	for wordI, valueI := range allWord.m {
		for i, sentenceEngI := range valueI.Examples {
			if sentence, ok := result[sentenceEngI]; ok {
				sentence.updateWords(wordI)
			} else {
				result[sentenceEngI] = newSentence(sentenceEngI, valueI.Example_translate[i], wordI)
			}
		}
	}

	return result
}

func allSentence(mapSentence map[string]*Sentence) map[string]*Sentence {
	result := make(map[string]*Sentence)
	fileOrigin, err := os.OpenFile(config.ConfReader.GetString("path.sentence_to_learn"), os.O_RDONLY, 0555)
	fileToConvert, err2 := os.OpenFile(config.ConfReader.GetString("path.new_file_with_sentence_and_words"), os.O_CREATE | os.O_WRONLY, 0555)

	if err != nil {
		panic(err)
	}

	if err2 != nil {
		panic(err2)
	}

	defer fileOrigin.Close()
	defer fileToConvert.Close()

	reader := bufio.NewReader(fileOrigin)
	fileToConvert.Truncate(0)
	writer := bufio.NewWriter(fileToConvert)
	sliceRepeatSentence := make(map[string]struct{})


	for {
		line, err := reader.ReadString('\n')
		line = strings.TrimSpace(line)

		if _, ok := sliceRepeatSentence[line]; ok {
			continue
		} else {
			sliceRepeatSentence[line] = struct{}{}
		}
		
		if sentence, ok := mapSentence[line]; ok {
			words := strings.Join(sentence.words, ", ")
			writer.WriteString(fmt.Sprintf("%v;    %v;    %v\n", words, sentence.eng, sentence.rus))
		} else {
			panic("Не обнаружили " + line)
		}

		if err != nil {
			if err == io.EOF {
				writer.Flush()
				break
			} else {
				panic(err)
			}
		}
	}

	return result
}


func createIgnoreWordsMap(words []string) map[string]struct{} {
	tempMap := make(map[string]struct{})
	for _, word := range words {
		tempMap[word] = struct{}{}
	}

	return tempMap
}


func addElementToSlice(s *[]string, word string) bool {
	if _, ok := AW.m[word]; ok {
		*s = append(*s, word)
		return true
	}

	return false
}


// приниммает на вход предложение, разделяет его на слова и проверяет есть ли слово в списке для изучения,
// если слово в списке - складываем его в срез
func getWordsForSentence(lineEng string, replacer *strings.Replacer, mapIgnoreWords map[string]struct{}) []string {
	lineEng = strings.TrimSpace(lineEng)
	sliceWordsEng := strings.Split(lineEng, " ")
	sliceWordsSentence := make([]string, 0)

	for _, wordI := range sliceWordsEng {
		if wordI != " " {
			wordI = replacer.Replace(wordI)
			wordI = strings.ToLower(wordI)
			if _, ok := mapIgnoreWords[wordI]; !ok {
				if addElementToSlice(&sliceWordsSentence, wordI) {
					continue
				} else if strings.HasSuffix(wordI, "s") {
					wordIWithOutS := strings.TrimRight(wordI, "s")
					addElementToSlice(&sliceWordsSentence, wordIWithOutS)
				} else if strings.HasSuffix(wordI, "ed") { 
					wordIWithOutD := strings.TrimRight(wordI, "d")
					if addElementToSlice(&sliceWordsSentence, wordIWithOutD) {
						continue
					} else {
						wordIWithOutEd := strings.TrimRight(wordIWithOutD, "e")
						addElementToSlice(&sliceWordsSentence, wordIWithOutEd)
					}
				}
			}
		}
	}

	return sliceWordsSentence
}


func convertNotFinteForms(pathEng, pathRus, pathResult string) {

	mapIgnoreWords := createIgnoreWordsMap(wordsToIgnore)
	sentenceWithoutWords := make([]string, 0)
	countWordToSuccess := 3  // у каждого предложения должно быть как минимут столько слов, чтобы предожение дублировалось
	replacer := strings.NewReplacer(replacerCharacters...)
	
	fileEng, err := os.OpenFile(pathEng, os.O_RDONLY, 0755)
	if err != nil {
		log.Panic(err)
	}
	defer fileEng.Close()
	
	fileRus, err := os.OpenFile(pathRus, os.O_RDONLY, 0755)
	if err != nil {
		log.Panic(err)
	}
	defer fileRus.Close()

	fileResult, err := os.OpenFile(pathResult, os.O_RDWR|os.O_CREATE, 0755)
	if err != nil {
		log.Panic(err)
	}
	defer fileResult.Close()

	readerEng := bufio.NewReader(fileEng)
	readerRus := bufio.NewReader(fileRus)
	writerResult := bufio.NewWriter(fileResult)
	templateRow := "%v;    %v;    %v\n"

	for {
		lineEng, errEng := readerEng.ReadString('\n')
		
		lineRus, _ := readerRus.ReadString('\n')
		lineRus = strings.TrimSpace(lineRus)
		
		lineEng = strings.TrimSpace(lineEng)
		sliceWordsSentence := getWordsForSentence(lineEng, replacer, mapIgnoreWords)
		// sliceWordsEng := strings.Split(lineEng, " ")
		// sliceWordsSentence := make([]string, 0)

		// for _, wordI := range sliceWordsEng {
		// 	if wordI != " " {
		// 		wordI = replacer.Replace(wordI)
		// 		wordI = strings.ToLower(wordI)
		// 		if _, ok := mapIgnoreWords[wordI]; !ok {
					
		// 			if addElementToSlice(&sliceWordsSentence, wordI) {
		// 				continue
		// 			} else if strings.HasSuffix(wordI, "s") {
		// 				wordIWithOutS := strings.TrimRight(wordI, "s")
		// 				addElementToSlice(&sliceWordsSentence, wordIWithOutS)
		// 			} else if strings.HasSuffix(wordI, "ed") { 
		// 				wordIWithOutD := strings.TrimRight(wordI, "d")
		// 				if addElementToSlice(&sliceWordsSentence, wordIWithOutD) {
		// 					continue
		// 				} else {
		// 					wordIWithOutEd := strings.TrimRight(wordIWithOutD, "e")
		// 					addElementToSlice(&sliceWordsSentence, wordIWithOutEd)
		// 				}
		// 			}
		// 		}
		// 	}
		// }

		if len(sliceWordsSentence) < countWordToSuccess {
			sentenceWithoutWords = append(sentenceWithoutWords, lineEng)
		}
		
		words := strings.Join(sliceWordsSentence, ", ")
		writerResult.WriteString(fmt.Sprintf(templateRow, words, lineEng, lineRus))

		if errEng == io.EOF {
			writerResult.Flush()
			break
		}
	}

	if len(sentenceWithoutWords) > 0 {
		for i, sentenceI := range sentenceWithoutWords {
			fmt.Println(i, sentenceI)
		}
	}
}