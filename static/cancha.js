
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