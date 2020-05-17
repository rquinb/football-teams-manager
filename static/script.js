$("#nuevo-jugador").on("click",function(){
    let nombre = $("#nombre").val();
    let ataque = $("#ataque").val();
    let defensa = $("#defensa").val();
    let stamina = $("#stamina").val();
    let tecnica = $("#tecnica").val();
    $("#tabla-jugadores-ingresados > tbody").prepend(`<tr>
    <td></td>
    <td>${nombre}</td>
    <td>${ataque}</td>
    <td>${defensa}</td>
    <td>${stamina}</td>
    <td>${tecnica}</td>
    </tr>`);
});

$("#cancha").soccerfield([{name: 'Matias', position: 'C_GK'}],{
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
