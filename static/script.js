let baseUrl = "http://localhost:5000";
$.get( `${baseUrl}/skills/`, function( data ) {
    let skills = data.data;
    localStorage.setItem('skills',JSON.stringify({"data": skills}));
});
const skillsNames = getAvailableSkillsNames();

function getSkillId(name){
  var skills = JSON.parse(localStorage.getItem("skills"))['data'];
  for(let skill of skills){
    if(skill['name'] == name){
      return skill['skill_id']
    }
  }
  return null
}

function getAvailableSkillsNames(){
  return JSON.parse(localStorage.getItem("skills"))['data'].map((value) => value['name']);
}

function getSkillValuesInForm(){
  skillsObject = {}
  for(let skillName of skillsNames){
    skillsObject[skillName] = parseInt($(`#${skillName}`).slider("value"));
  }
  return skillsObject
}

$("#nuevo-jugador").on("click",function(){
  var nombre = $("#nombre").val();
  var skillsObject = getSkillValuesInForm();
  var skills = [];
  for(let skill in skillsObject){
    let skillObject = {'id':getSkillId(skill),'strength':skillsObject[skill]};
    skills.push(skillObject);
  }
    // Save to DB
    $.ajax({
        type: "POST",
        url: `${baseUrl}/players/`,
        data: JSON.stringify({"name":nombre, "skills":skills}),
        success: function(response){
          let player_id = response.data['player_id'];
          $("#players-container").append(createPlayerCard(player_id, nombre ,skillsObject));
          alert(`Jugador ${player_id} creado con exito!`);
        },
        contentType: "application/json; charset=utf-8"
      });
});

$("#button-generate-teams").on("click",function(){
  let baseMatchUrl = `${baseUrl}/match?`;
  let numberOfPlayers = $("#tipo-futbol").val();
  let playersPerTeam = `players_per_team=${numberOfPlayers}`;
  let playersForMatch = "";
  let playerCards = $(".selected-player-card");
  for(let playerCard of playerCards){
    let playerId = $(playerCard).attr('id').split('-')[1];
    playersForMatch += `&player=${playerId}`;
  }
  let fullMatchUrl = baseMatchUrl + playersPerTeam + playersForMatch;
  $.get(fullMatchUrl, function( data ) {
    let positions = ['C_GK', 'LC_B', 'C_B', 'RC_B','C_DM', 'LC_M', 'RC_M'];
    let teamsNames = Object.keys(data['teams']);
    console.log(teamsNames);
    for(let i=0;i<teamsNames.length;i++){
      let playersPositions = [];
      for(let j=0;j<parseInt(numberOfPlayers);j++){
        let playerObject = {};
        playerObject['name'] = data['teams'][teamsNames[i]]['players'][j]['name'];
        playerObject['position'] = positions[j];
        playersPositions.push(playerObject);
      }
      $(`.team${i+1}`).soccerfield(playersPositions,{
          field: {
            width: "500px",
            height: "400px",
            img: '../static/Soccer-Field-Players-Positions/src/img/soccerfield_green.png',
            startHidden: false,
            animate: false,
            fadeTime: 1000,
            autoReveal:true
          },
          players: {
              font_size: 10,
              reveal: true,
              sim: true,
              timeout: 1000,
              fadeTime: 1000,
              img: false
          }
      });
    }
  });
});

$(".players-data-numeric-input").slider({
  min: 1,
  max: 10,
  create: function( event, ui ) {
    $(this).find(".ui-slider-handle").text($(this).slider("value"));
  },
  slide: function( event, ui ) {
    $(this).find(".ui-slider-handle").text( ui.value );
  }
});

$( ".form-control-range" ).slider();

$(document).on("click",".player-card",function(){
  $(this).toggleClass("selected-player-card");
  let listOfPlayers = "";
  let playerCards = $(".selected-player-card");
  for(let playerCard of playerCards){
    listOfPlayers += `<div class="card">${$(playerCard).find('.player-name-card').text()}</div>`
  }
  $("#available-players-container").html(listOfPlayers);
});


$.get( `${baseUrl}/players/`, function( data ) {
    let players_data = data.data;
    let nombre, id;
    for(let i=0; i < players_data.length; i++){
        nombre = players_data[i]['name'];
        id = players_data[i]['player_id'];
        let skillsObject = {};
        for(let j=0; j < players_data[i]['skills'].length; j ++){
            let skill = players_data[i]['skills'][j];
            skillsObject[skill['name']] = skill['strength'];
        }     
        $("#players-container").append(createPlayerCard(id, nombre, skillsObject));
    }
  });

  function createPlayerCard(id ,nombre, skillsObject){
    let amount_of_skills = Object.keys(skillsObject).length;
    let total_skills = 0
    let skills_html = ""
    for(let skill in skillsObject){
      total_skills += skillsObject[skill];
      skills_html += `<label style="text-transform:capitalize;">${skill}: </label><div class="progress"><div class="progress-bar bg-success" role="progressbar" style="width: ${skillsObject[skill] / 10 * 100}%" aria-valuenow="${skillsObject[skill]}" aria-valuemin="0" aria-valuemax="10">${skillsObject[skill]}</div></div>`
    }
    let promedio = (total_skills / amount_of_skills).toFixed(1);
    return `<div class="card player-card" id="player-${id}">
              <div class="card-header bg-success player-name-card">
              ${nombre}
              </div>
              <div class="row-fluid">
                <div class="text-center card">
                  <span class="average-skill">${promedio}</span>
                </div>
              </div>
              <div class="row-fluid">
                <div class="card-body">
                  ${skills_html}
                </div>
              </div>
            </div>`
  };
