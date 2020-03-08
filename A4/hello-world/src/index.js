// ==== Import Statements ====

import React from 'react';
import ReactDOM from 'react-dom';
import $ from 'jquery';
import './index.css';

// ==== Global Variables ====

var username;
var connected;
var timeBetweenNextChatlogCheck = 1000;

// ==== Classes ====

class SendButton extends React.Component {
    render() {
        return (
            <button className="sendbutton" onClick={this.props.onClick}>
                Send
            </button>
        );
    }
}

class LoginButton extends React.Component {
    render() {
        return (
            <button className="loginbutton" onClick={this.props.onClick}>
                Login
            </button>
        );
    }
}

class RoomButton extends React.Component {
    render() {
        return (
            <button className="roombutton">

            </button>
        );
    }
}

class Chatbox extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            message: '',
            username: '',
            chatlog: [],
            rooms: []
        };
        this.handleMessageChange = this.handleMessageChange.bind(this);
        this.handleUsernameChange = this.handleUsernameChange.bind(this);
        this.handleSendKeyPress = this.handleSendKeyPress.bind(this);
        this.handleLoginKeyPress = this.handleLoginKeyPress.bind(this);
        this.initUser = this.initUser.bind(this);
        this.getChatlog = this.getChatlog.bind(this);
    }

    // == Lifecycle ==

    componentDidMount() {
        if (connected) {
        }
    }

    // == Rendering ==

    renderSendButton() {
        return (
            <SendButton
                onClick={() => this.sendClick()}
            />
        );
    }

    renderLoginButton() {
        return (
            <LoginButton
                onClick={() => this.loginClick()}
            />
        );
    }

    // == Handle ==

    sendClick() {
        this.sendMessage(this.state.message);
    }

    loginClick() {
        this.initUser(this.state.username);
    }

    handleSendKeyPress(event) {
        if (event.key === "Enter") {
            this.sendMessage(this.state.message);
        }
    }
    
    handleLoginKeyPress(event) {
        if (event.key === "Enter") {
            this.initUser(this.state.message);
        }
    }

    handleMessageChange(event) {
        this.setState({ message: event.target.value });
    }

    handleUsernameChange(event) {
        this.setState({ username: event.target.value });
    }

    // == Functionality ==

    initUser() {
        username = this.state.username;

        console.log(username);

        if (username === "") {
            alert("Username cannot be empty");
        } else {
            this.joinRoom();
            connected = true;
            setInterval(this.getChatlog, timeBetweenNextChatlogCheck);
            this.forceUpdate();
        }
    }

    // == Rest API ==

    // = POST =

    joinRoom() {
        $.ajax({
            url: "http://localhost:5000/chatroom/register/",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                "username": username,
            })
        }).done(function (data) {
            console.log(data);
        });
    }

    sendMessage(message) {
        this.setState({message: ''});

        $.ajax({
            url: "http://localhost:5000/chatroom/sendmessage/",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                "username": username,
                "message": message
            })
        }).done(function (data) {
            console.log(data);
        });
    }

    sendCommand(command) {
        // TODO

        $.ajax({
            url: "http://localhost:5000/chatroom/command/",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                "username": username,
                "command": command
            })
        }).done(function (data) {
            console.log(data);
        });

    }

    // = GET =

    getChatlog() {
        fetch("http://localhost:5000/chatroom/chatlog/" + username + "/")
            .then(res => res.json())
            .then(
                (result) => {
                    console.log(result);
                    this.setState({ chatlog: result });
                }
            )
    }

    // == Render Self ==

    render() {
        if (connected) {
            return (
                <div className="chat-box">
                    <div className="chat-title">
                        <p>Chatbox:</p>
                    </div>
    
                    <div className="chat-log">
                        {
                        this.state.chatlog.map(function(item, i){
                            //console.log("Item: " + item);
                            return <p key={i}>{item}</p>
                        })
                        }
                    </div>
    
                    <div className="message-line">
                        Message: <input type="text" value={this.state.message} onChange={this.handleMessageChange} onKeyPress={this.handleSendKeyPress}></input>
                        {this.renderSendButton()}
                    </div>

                    <div className="room-list">

                    </div>
                </div>
            );
        } else {
            return (
                <div className="not-connected">
                    Username: <input type="text" value={this.state.username} onChange={this.handleUsernameChange} onKeyPress={this.handleLoginKeyPress}></input>
                    {this.renderLoginButton()}
                </div>
            );
        }

    }
}

// ========================================



ReactDOM.render(
    <Chatbox />,
    document.getElementById('root')
);
