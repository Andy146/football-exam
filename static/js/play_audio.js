function play_audio(team){

    if(typeof(audio) != 'undefined'){
        audio.pause();
    }
    team_spans = document.getElementsByClassName('team-span');

    for(i=0; i<team_spans.length; i++){
        team_spans[i].children[0].style = ""
        team_spans[i].children[1].style = ""
        if(typeof(time) != "undefined"){
            clearTimeout(time)
        }
    }

    audio = new Audio('/static/assets/' + team + '.mp3');
    audio.play();

    team_name = document.getElementById(team).parentNode.children[1];
    team_name.style = "display: flex; color: white;";

    team_image = document.getElementById(team);
    team_image.style = "animation: team-spin 1s infinite";

    time = setTimeout(remove_spin, 4000, team_name, team);
}

function remove_spin(team_name, team_image){
    team_name.style = "";
    document.getElementById(team_image).style = "";
}