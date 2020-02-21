var username;
var connected;
var currentChatroom;
var timeBetweenNextChatlogCheck = 2000;

$("document").ready(function(){

    connected = true;

    initUser();

    if (connected) {
      setInterval(displayChatlog, timeBetweenNextChatlogCheck);
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
  currentChatroom = "General"
  joinRoom();
}

function joinRoom() {
  $.ajax({
  url: "http://localhost:5000/rooms/" + currentChatroom + "/join/",
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
  url: "http://localhost:5000/rooms/" + currentChatroom + "/sendmessage/",
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

  document.getElementById("channel title").innerHTML = currentChatroom + ":"

  $.get("http://localhost:5000/rooms/" + currentChatroom + "/chatlog/", function(data, status){
    console.log(data);
    console.log(status);
    var x = data.toString();
    x = data.join("<br>");
    document.getElementById("chatlog").innerHTML = x;
    });
}
