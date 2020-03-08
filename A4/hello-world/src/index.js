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

class Chatbox extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            message: '',
            chatlog: []
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleKeyPress = this.handleKeyPress.bind(this);
        this.initUser = this.initUser.bind(this);
        this.displayChatlog = this.displayChatlog.bind(this);
    }

    // == Lifecycle ==

    componentDidMount() {
        this.initUser();

        if (connected) {
            setInterval(this.displayChatlog, timeBetweenNextChatlogCheck);
        }
    }

    // == Rendering ==

    renderSendButton() {
        return (
            <SendButton
                onClick={() => this.handleClick()}
            />
        );
    }

    // == Handle ==

    handleClick() {
        this.sendMessage(this.state.message);
    }

    handleKeyPress(event) {
        if (event.key === "Enter") {
            this.sendMessage(this.state.message);
        }
    }

    handleChange(event) {
        this.setState({ message: event.target.value });
    }

    // == Functionality ==

    initUser() {
        username = prompt("Please input a username:");

        while (username === "") {
            username = prompt("Username cannot be empty");
        }
        this.joinRoom();
        connected = true;
    }

    // = Rest API =

    joinRoom() {
        $.ajax({
            url: "http://localhost:5000/chatroom/join/",
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

    displayChatlog() {
        fetch("http://localhost:5000/chatroom/chatlog/" + username + "/")
            .then(res => res.json())
            .then(
                (result) => {
                    console.log(result);
                    //var x = result.toString();
                    //x = result.join("\n");
                    this.setState({ chatlog: result });
                }
            )
    }

    // == Render Self ==

    render() {
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
                    Message: <input type="text" value={this.state.message} onChange={this.handleChange} onKeyPress={this.handleKeyPress}></input>
                    {this.renderSendButton()}
                </div>
            </div>
        );
    }
}

// ========================================



ReactDOM.render(
    <Chatbox />,
    document.getElementById('root')
);
