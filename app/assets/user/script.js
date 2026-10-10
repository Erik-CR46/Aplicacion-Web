const container = document.querySelector(".container");

const showRegister = document.getElementById("showRegister");
const showLogin = document.getElementById("showLogin");


showRegister.addEventListener("click", function(event) {

    event.preventDefault();

    container.classList.add("active");

});


showLogin.addEventListener("click", function(event) {

    event.preventDefault();

    container.classList.remove("active");

});