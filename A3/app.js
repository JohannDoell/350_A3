var username;
var connected;

$("document").ready(function(){

    connected = true;

    initUser();

    if (connected) {
      setInterval(displayChatlog, 2000);
    }

    // HTML calls the "send" labeled function on click.
    $("#send").click(function(){
        var message = $("#message").val();
        sendMessage(message);
    });

});

function initUser() {
  username = prompt("Please input a username:");

  while (username === "") {
    username = prompt("Username cannot be empty");
  }

  $.ajax({
  url: "http://localhost:5000/user/setuser/",
  type: "POST",
  contentType: "application/json",
  data: JSON.stringify({
    "username": username,
  })
        }).done(function(data) {
  console.log(data);
        });
}

function sendMessage(message) {
  $.ajax({
  url: "http://localhost:5000/rooms/room/sendmessage/",
  type: "POST",
  contentType: "application/json",
  data: JSON.stringify({
    "username": username,
    "message": message
  })
        }).done(function(data) {
  console.log(data);
        });
}

function displayChatlog() {
  $.get("http://localhost:5000/rooms/room/chatlog/", function(data, status){
    console.log(data);
    console.log(status);
    var x = data.toString();
    x = data.join("<br>");
    document.getElementById("chatlog").innerHTML = x;
    });
}
