function validar(){
    let nuevoUsuario= document.getElementById("nuevoUsuario").value;
    let contraseña= document.getElementById("contraseña").value;
    let correo= document.getElementById("correo").value;

    if (nuevoUsuario===""){
        alert("El nombre de usuario está vacío");
        return false
    } else if (contraseña===""){
        alert("La contraseña está vacía");
        return false
    } else if (correo===""){
        alert("Debe introducir un correo electrónico");
        return false
    }
}

function guardarDatos(){
let nuevoUsuario= document.getElementById("nuevoUsuario").value;
let contraseña= document.getElementById("contraseña").value;
let correo= document.getElementById("correo").value;
let datosusu=localStorage.getItem("datosusuarios");
    if (datosusu==null){
    let datos={"datos":[{"nuevoUsuario": nuevoUsuario, "contraseña": contraseña, "correo": correo}]};
    localStorage.setItem("datosusuarios", JSON.stringify(datos));
    } else {
        datosusu=JSON.parse(datosusu);
        for(let i=0;i<datosusu["datos"].length;i++){
            if (datosusu["datos"][i]["nuevoUsuario"]==nuevoUsuario){
                alert("Usuario ya existente")
                return false
            }
        }
        datosusu["datos"].push({"nuevoUsuario": nuevoUsuario, "contraseña": contraseña, "correo": correo});
        localStorage.setItem("datosusuarios", JSON.stringify(datosusu));
    }
}