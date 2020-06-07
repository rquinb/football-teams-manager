function ingresar(){
    let usuario= document.getElementById("Usuario").value;
    let contraseña= document.getElementById("Contraseña").value;
    let datosUsuario= JSON.parse(localStorage.getItem("datosusuarios")); 
    for (let i=0; i<datosUsuario["datos"].lenght; i++){
        if(usuario==datosUsuario [i]["nuevoUsuario"]){
            if(contraseña==datosUsuario [i]["contraseña"]){
                    window.location.href="http://localhost:5000/administrador-de-equipos"
                } else {
                    alert("Contraseña incorrecta");//sino sde la comparación de las contraseñas
                }
            } else {
                alert("Usuario no existente")//sino de la comparación de los usuarios
            }
        }
}