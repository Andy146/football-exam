function play_audio(team){

    if(typeof(audio) != 'undefined'){
        audio.pause()
    }

    audio = new Audio('/static/assets/' + team + '.mp3')
    audio.play()
}