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
      let skillObject = {'id':getSkillId(skill),'strength':skillsObject[skill]}
      skills.push(skillObject);
    }
    $("#players-container").append(createPlayerCard(nombre ,skillsObject));
    // Save to DB
    $.ajax({
        type: "POST",
        url: `${baseUrl}/players/`,
        data: JSON.stringify({"name":nombre, "skills":skills}),
        success: alert("Jugador creado con exito!"),
        contentType: "application/json; charset=utf-8"
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


$.get( `${baseUrl}/players/`, function( data ) {
    let players_data = data.data;
    let nombre;
    for(let i=0; i < players_data.length; i++){
        nombre = players_data[i]['name'];
        let skillsObject = {};
        for(let j=0; j < players_data[i]['skills'].length; j ++){
            let skill = players_data[i]['skills'][j];
            skillsObject[skill['name']] = skill['strength'];
        }     
        $("#players-container").append(createPlayerCard(nombre, skillsObject));
    }
  });

  function createPlayerCard(nombre, skillsObject){
    let amount_of_skills = Object.keys(skillsObject).length;
    let total_skills = 0
    let skills_html = ""
    for(let skill in skillsObject){
      total_skills += skillsObject[skill];
      skills_html += `<label style="text-transform:capitalize;">${skill}: </label><div class="progress"><div class="progress-bar bg-success" role="progressbar" style="width: ${skillsObject[skill] / 10 * 100}%" aria-valuenow="${skillsObject[skill]}" aria-valuemin="0" aria-valuemax="10">${skillsObject[skill]}</div></div>`
    }
    let promedio = (total_skills / amount_of_skills).toFixed(1);
    return `<div class="card player-card">
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

