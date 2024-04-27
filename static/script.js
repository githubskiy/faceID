var width = 1200; // We will scale the photo width to this
var height = 0; // This will be computed based on the input stream

var streaming = false;

var video = null;
var canvas = null;
var photo = null;
var register_button = null;
var login_button = null;
var nameElement = null;
var ageElement = null;


function startup() {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    photo = document.getElementById('photo');
    register_button = document.getElementById('register_button');
    login_button = document.getElementById('login_button');
    nameElement = document.getElementById("name-input");
    ageElement = document.getElementById("age-input");

    navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false
        })
        .then(function(stream) {
            video.srcObject = stream;
            video.play();
        })
        .catch(function(err) {
            console.log("An error occurred: " + err);
        });

    video.addEventListener('canplay', function(ev) {
        if (!streaming) {
            height = video.videoHeight / (video.videoWidth / width);

            if (isNaN(height)) {
                height = width / (4 / 3);
            }

            video.setAttribute('width', width);
            video.setAttribute('height', height);
            canvas.setAttribute('width', width);
            canvas.setAttribute('height', height);
            streaming = true;
        }
    }, false);

    register_button.addEventListener('click', function(ev) {
        takepicture_for_register();
        ev.preventDefault();
    }, false);

    login_button.addEventListener('click', function(ev) {
        takepicture_for_login();
        ev.preventDefault();
    }, false);

    clearphoto();


}


function clearphoto() {
    var context = canvas.getContext('2d');
    context.fillStyle = "#AAA";
    context.fillRect(0, 0, canvas.width, canvas.height);

    // var data = canvas.toDataURL('image/png');
    // photo.setAttribute('src', data);
}
function isNumber(value) {
    return typeof value === 'number' && !isNaN(value);
  }


async function takepicture_for_register() {
    var context = canvas.getContext('2d');
    if (width && height) {
        canvas.width = width;
        canvas.height = height;
        context.drawImage(video, 0, 0, width, height);
    
        // console.log("context.getImageData: "+context.getImageData(0,0,width,height).data);

        var dataURL = canvas.toDataURL('image/jpeg');
        // console.log("dataURL_lenght: "+dataURL);
        photo.setAttribute('src', dataURL);

        nameValue = nameElement.value;
        ageValue = ageElement.value;
        
        console.log("nameValue: "+ nameValue);
        console.log("ageValue: "+ ageValue);
  
      
            const response = await fetch("/user", { 
                method: "POST",
                headers: { "Accept": "application/json", "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_name: nameValue,
                    user_age: ageValue,
                    photo_base64: dataURL
                })
            });
        
            if (response.ok) {
                const data = await response.json();
                console.log("data response: "+ data);
                // document.getElementById("ajax").textContent = data.message;
            }
            else
                console.log("response: "+response);
        

    } 
    else 
    {
        clearphoto();
    }
}



async function takepicture_for_login() {
    var context = canvas.getContext('2d');
    if (width && height) {
        canvas.width = width;
        canvas.height = height;
        context.drawImage(video, 0, 0, width, height);
    
        // console.log("context.getImageData: "+context.getImageData(0,0,width,height).data);

        var dataURL = canvas.toDataURL('image/jpeg');
       
            photo.setAttribute('src', dataURL);

        const response = await fetch("/login", {
            method: "POST",
            headers: { "Accept": "application/json", "Content-Type": "application/json" },
            body: JSON.stringify({
                photo_base64: dataURL
            })
        });

        if (response.ok) {
            const data = await response.json();
            console.log("data response: "+ data['access_token']);
            localStorage.setItem("accessToken",  data['access_token']);
            currentURL = window.location.href;
            window.location.assign(currentURL + "user_cabinet")
            console.log(currentURL);
            console.log(currentURL + "user_cabinet");
        }
        else
            console.log("response: "+response);

    } else {
        clearphoto();
    }
}

window.addEventListener('load', startup, false);