document.addEventListener( "DOMContentLoaded", () => {
    let fieldMain = document.querySelector( ".fieldMain" ),
        btnNext = document.getElementById( "next" ),
		  passiveWord = document.getElementById( "passiveWord" ),
		  transcription = document.getElementById( "transcription" ),
        btnStart = document.getElementById( "start" ),
        btnCheck = document.getElementById( "check" ),
        rangeStart = document.getElementById( "rangeStart" ),
        rangeFInish = document.getElementById( "rangeFInish" ),
        activWord = document.getElementById( "activWord" ),
        typeExercise = document.getElementById( "typeExercise" ),
        finish = document.getElementById( "finish" ),
		 sound = document.getElementById( "sound" ),
		 result,
		 private = {
    		check: function(valid) {
				if (valid) {
					this.classList.remove('error');
					this.classList.add('success');
				} else {
					this.classList.add('error');
					this.classList.remove('success');
				}
    		}
		 },
        isValue = ( value ) => {
            return value ? value : false;
        },
        disableStart = ( v1, v2 ) => {
            let disabled = true;

            if ( isValue( v1 ) && isValue( v2 ) ) {
                disabled = false;
            }
            btnStart.disabled = disabled;
        },
        send = ( data ) => {
            let boundary = String( Math.random() ).slice( 2 ),
                boundaryMiddle = `--${ boundary }\r\n`,
                boundaryLast = `--${ boundary }--\r\n`,

                body = [ "\r\n" ];

            for ( let key in data ) {
                // добавление поля
                body.push( `Content-Disposition: form-data; name="${ key }"\r\n\r\n${ data[ key ] }\r\n` );
            }

            body = body.join( boundaryMiddle ) + boundaryLast;

            // Тело запроса готово, отправляем

            let xhr = new XMLHttpRequest();

            xhr.open( "POST", "http://localhost:8088/"+ data.type, true );

            xhr.setRequestHeader( "Content-Type", `multipart/form-data; boundary=${ boundary}` );

            xhr.onreadystatechange = function() {
                if ( xhr.readyState === 4 && xhr.status === 200 ) {
             if (!data.sound) {
               result = JSON.parse( this.responseText);
               passiveWord.innerText = result.translate;
             }

                }
            };

            xhr.send( body );
        },
	 		distbled = (Enable) => {
				let radio = document.querySelectorAll('[name="learn"]');
				for (var i = 0, len = radio.length; i < len; i++) {
					if (radio[i].value === '0') {
						radio[i].checked = true;
					}
					radio[i].disabled = Enable
				}
			};

    btnStart.addEventListener( "click", () => {
        let param = {
            "type": typeExercise.value,
            "start": rangeStart.value,
            "finish": rangeFInish.value
        };

        send( param );
    } );

	finish.addEventListener( "click", () => {
        let param = {
            "type": typeExercise.value,
            "finishWork": rangeFInish.value
        };

        send( param );
    } );

	sound.addEventListener( "click", () => {
		let param = {
			"type": 'en',
			"sound": true,
			"word": result.word
		};

		send( param );
	} );

	transcription.addEventListener( "mouseenter", () => {
		transcription.innerText = result.trancription;
    } );

	transcription.addEventListener( "mouseleave", () => {
		transcription.innerText = 'Посмотреть транскрипцию';
    } );

	btnCheck.addEventListener( "click", () => {
		let valid = false,
			desable = true;
		if (activWord.value === result.word) {
			desable = false;
			valid = true;
		} else {
			distbled(true);
		}

		btnNext.disabled = desable;
		private.check.call(activWord, valid);
	} );

    typeExercise.addEventListener( "change", ( e ) => {
    	if (e.currentTarget.value === 'ru') {
			transcription.classList.remove('hidden');
    	} else {
			transcription.classList.add('hidden');
		}
    } );

    rangeStart.addEventListener( "change", ( e ) => {
        disableStart( e.currentTarget.value, rangeFInish.value );
    } );

    rangeFInish.addEventListener( "change", ( e ) => {
        disableStart( e.currentTarget.value, rangeStart.value );
    } );

    btnNext.addEventListener( "click", () => {
		let param = {
			"type": typeExercise.value,
			"word": result.word,
			'know': document.querySelector('[name="learn"]:checked').value
		}
		 distbled(false);
		 send( param );
    } );
} );
