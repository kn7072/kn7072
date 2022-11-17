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
	fileOrigin, err := os.OpenFile(config.ConfReader.GetString("path.sentence_to_learn"), os.O_RDONLY, 0755)
	fileToConvert, err2 := os.OpenFile(config.ConfReader.GetString("path.new_file_with_sentence_and_words"), os.O_CREATE | os.O_WRONLY, 0755)

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
	

	for {
		line, err := reader.ReadString('\n')
		line = strings.TrimSpace(line)
		
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


func convertNotFinteForms(pathEng, pathRus, pathResult string) {

	wordsToIgnore := []string{"the", "an", "a", "as", "she", "we", "you", "her", "he", "him", "on", "no", "off", "of",
	 "for", "is", "be",	"to", "not", "in", "his", "i", "it", "me", "my", "if", "am", "are", "was", "at", "this", "they",
	 "that", "then", "than", "do", "out", "go", "too", "with", "us", "our", "from", "have", "has", "all", "their", "so",
	 "and", "but", "can", "your", "were"}
	mapIgnoreWords := createIgnoreWordsMap(wordsToIgnore)
	
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
	replacer := strings.NewReplacer(".", "", ",", "", "?", "", "!", "", "(", "", ")", "", "\n", "")
	templateRow := "%v;    %v;    %v\n"

	for {
		lineEng, errEng := readerEng.ReadString('\n')
		lineEng = strings.TrimSpace(lineEng)
		lineRus, _ := readerRus.ReadString('\n')
		lineRus = strings.TrimSpace(lineRus)
		sliceWordsEng := strings.Split(lineEng, " ")
		sliceWordsSentence := make([]string, 0)

		for _, wordI := range sliceWordsEng {
			if wordI != " " {
				wordI = replacer.Replace(wordI)
				wordI = strings.ToLower(wordI)
				if _, ok := mapIgnoreWords[wordI]; !ok {
					sliceWordsSentence = append(sliceWordsSentence, wordI)
				}
			}
		}

		words := strings.Join(sliceWordsSentence, ", ")
		writerResult.WriteString(fmt.Sprintf(templateRow, words, lineEng, lineRus))

		if errEng == io.EOF {
			writerResult.Flush()
			break
		}
	}
}