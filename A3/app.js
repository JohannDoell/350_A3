var username;

$("document").ready(function(){

    initUser();

    var fruits = ["Banana", "Orange", "Apple", "Mango"];
    var x = fruits.toString();
    x = fruits.join("<br>");

    document.getElementById("chatlog").innerHTML = x;

    // HTML calls the "send" labeled function on click.
    $("#send").click(function(){
        var message = $("#message").val();

            $.ajax({
            url: "http://localhost:5000/api/",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
              "username": username,
              "message": message
            })
                  }).done(function(data) {
            console.log(data);
                  });
                    });

});

function initUser() {
  username = prompt("Please input a username:");

  while (username === "") {
    username = prompt("Username cannot be empty");
  }

  $.ajax({
  url: "http://localhost:5000/api/",
  type: "POST",
  contentType: "application/json",
  data: JSON.stringify({
    "username": username,
  })
        }).done(function(data) {
  console.log(data);
        });

}

function displayChatlog() {

}
