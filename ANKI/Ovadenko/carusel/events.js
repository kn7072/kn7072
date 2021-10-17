document.addEventListener("DOMContentLoaded", () => {
    const delay = 60000;
    const content = document.querySelector('.content');
    let currentIndex = 0;
    let exercises;
    let len;
    let timerId;
    //let file = new File(fileParts, fileName, [options])

    clickLeft  = (e) => {
        currentIndex -= 2;
        currentIndex = setCorrectIndex(currentIndex);
        clearInterval(timerId);
        setContent(currentIndex)
        runSlide(currentIndex++)
    };

    clickRight  = (e) => {
        currentIndex = setCorrectIndex(currentIndex);
        clearInterval(timerId);
        setContent(currentIndex)
        runSlide(currentIndex++)
    };

    clickChoiceFile  = (e) => {
        let file = e.target.files[0];
        let reader = new FileReader();
        reader.readAsText(file)
        reader.onload = function() {
            exercises = reader.result.split('#');
            len = exercises.length
            setContent(currentIndex);
            runSlide(currentIndex++)
        };
    };
    document.querySelector('.left').addEventListener('click', clickLeft, false)
    document.querySelector('.right').addEventListener('click', clickRight, false)
    document.getElementById('file').addEventListener('change', clickChoiceFile, false)

    function setContent(index) {
        content.innerHTML = exercises[index];
    }

    function runSlide(index) {
        timerId = setInterval(() => {
            if (currentIndex == len ) {
                currentIndex = 0;
            }
            setContent(currentIndex);
            currentIndex++;
        }, delay)
    }

    function setCorrectIndex(index) {
        let result = index;
        if (index < 0 || index >= len) {
            result = 0;
        }
        return result;
    }
});

function getExercises() {
    return ["Lorem ipsum dolor sit amet consectetur, adipisicing elit. Sequi quaerat sunt expedita soluta nam veniam, saepe atque. Repellendus praesentium obcaecati accusantium natus repudiandae aspernatur, quas corporis deleniti asperiores quo ipsum. \n\n 77777777", "22222 \n 77777777", "333333 \n 77777777", "44444 \n 77777777", "555555",
"lore"];
}


