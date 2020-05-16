$("#nuevo-jugador").on("click",function(){
    let nombre = $("#nombre").val();
    let ataque = $("#ataque").val();
    let defensa = $("#defensa").val();
    let stamina = $("#stamina").val();
    let tecnica = $("#tecnica").val();
    $("#tabla-jugadores-ingresados").append(`<tr>
    <td>${nombre}</td>
    <td>${ataque}</td>
    <td>${defensa}</td>
    <td>${stamina}</td>
    <td>${tecnica}</td>
    </tr>`);
})