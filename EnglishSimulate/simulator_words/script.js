document.addEventListener( "DOMContentLoaded", () => {
    let fieldMain = document.querySelector( ".fieldMain" ),
        btnNext = document.getElementById( "next" ),
        btnStart = document.getElementById( "start" ),
        btnCheck = document.getElementById( "check" ),
        rangeStart = document.getElementById( "rangeStart" ),
        rangeFInish = document.getElementById( "rangeFInish" ),
        activWord = document.getElementById( "activWord" ),
        typeExercise = document.getElementById( "typeExercise" ),

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

            xhr.open( "POST", "http://localhost:8088/send", true );

            xhr.setRequestHeader( "Content-Type", `multipart/form-data; boundary=${ boundary}` );

            xhr.onreadystatechange = function() {
                if ( xhr.readyState === 4 && xhr.status === 200 ) {
						 alert( this.responseText );
                }

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

    typeExercise.addEventListener( "change", ( e ) => {

    } );

    rangeStart.addEventListener( "change", ( e ) => {
        disableStart( e.currentTarget.value, rangeFInish.value );
    } );

    rangeFInish.addEventListener( "change", ( e ) => {
        disableStart( e.currentTarget.value, rangeStart.value );
    } );

    btnNext.addEventListener( "click", () => {


    } );
} );
