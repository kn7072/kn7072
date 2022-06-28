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