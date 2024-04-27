var usernameElement = null;
var ageElement = null;

function startup() {
    usernameElement = document.getElementById("username");
    ageElement = document.getElementById("userage");

    getUserData();

    // login_button.addEventListener('click', function(ev) {
    //     takepicture_for_login();
    //     ev.preventDefault();
    // }, false);

}


function getUserData() {
    const accessToken = localStorage.getItem("accessToken");
  
    fetch("/user/info", {
      headers: {
        Authorization: "Bearer " + accessToken,
      },
    })
      .then((response) => {
        if (response.ok) {
            
        
          return response.json();
        } 
        else {
          throw new Error("Error occurred");
        }
      })
      .then((data) => {
        // Обробка отриманих даних користувача
        console.log(data);
        // Виклик функції для відображення даних користувача на сторінці
        usernameElement.textContent = data["user_name"];
        ageElement.textContent = data["user_age"];
      })
      .catch((error) => {
        // Обробка помилок
        console.error(error);
      });
  }

window.addEventListener('load', startup, false);