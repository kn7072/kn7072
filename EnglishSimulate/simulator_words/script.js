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
						 result = JSON.parse( this.responseText);
						 transcription.innerText = result.trancription;
						 passiveWord.innerText = result.translate;
                }
				//	Object { trancription: " |fɜːrm|", word: "firm", translate: "фирма, торговый дом, твердый, крепкий, твердо, крепко, укреплять" }
            };

            xhr.send( body );
        };

    btnStart.addEventListener( "click", () => {
        let param = {
            "type": typeExercise.value,
            "start": rangeStart.value,
            "finish": rangeFInish.value
        };

        send( param );
    } );

	btnCheck.addEventListener( "click", () => {
		let valid = false,
			desable = true;
		if (activWord.value === result.word) {
			desable = false;
			valid = true;
		}
		btnNext.disabled = desable;
		private.check.call(activWord, valid);
	} );

    typeExercise.addEventListener( "change", ( e ) => {

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
		 send( param );
    } );
} );
