let baseUrl = "http://localhost:5000";

$.get( `${baseUrl}/skills/`, function( data ) {
    let skills = data.data;
    localStorage.setItem('skills',JSON.stringify(skills));
});

$("#nuevo-jugador").on("click",function(){
    var nombre = $("#nombre").val();
    var ataque = parseInt($("#ataque").val());
    var defensa = parseInt($("#defensa").val());
    var stamina = parseInt($("#stamina").val());
    var tecnica = parseInt($("#tecnica").val());
    $("#tabla-jugadores-ingresados > tbody").prepend(`<tr>
    <td></td>
    <td>${nombre}</td>
    <td>${ataque}</td>
    <td>${defensa}</td>
    <td>${stamina}</td>
    <td>${tecnica}</td>
    </tr>`);
    // Save to DB
    $.ajax({
        type: "POST",
        url: `${baseUrl}/players/`,
        data: JSON.stringify({"name":nombre, "skills":[{"id":1,"strength":ataque},{"id":2,"strength":defensa},{"id":3,"strength":stamina},{"id":4,"strength":tecnica}]}),
        success: alert("Jugador creado con exito!"),
        contentType: "application/json; charset=utf-8"
      });
});

$.get( `${baseUrl}/players/`, function( data ) {
    let players_data = data.data;
    let nombre, ataque, defensa, stamina, tecnica;
    for(let i=0; i < players_data.length; i++){
        nombre = players_data[i]['name'];
        for(let j=0; j < players_data[i]['skills'].length; j ++){
            let skill = players_data[i]['skills'][j];
            switch(skill['name']) {
                case "ataque":
                  ataque = skill['strength'];
                  break;
                case "defensa":
                  defensa = skill['strength'];
                  break;
                case "stamina":
                  stamina = skill['strength'];
                case "tecnica":
                  tecnica = skill['strength'];
              }

        }     
        $("#tabla-jugadores-ingresados > tbody").prepend(`<tr>
        <td></td>
        <td>${nombre}</td>
        <td>${ataque}</td>
        <td>${defensa}</td>
        <td>${stamina}</td>
        <td>${tecnica}</td>
        </tr>`);
    }
  });
