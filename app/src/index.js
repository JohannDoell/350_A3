// ==== Import Statements ====

import React from 'react';
import ReactDOM from 'react-dom';
import $ from 'jquery';
import './index.css';

// ==== Global Variables ====

var username;
var connected;
var timeBetweenNextChatlogCheck = 1000;

var webServiceURL = 'http://localhost:8000/?wsdl'
// var webServiceURL = 'http://172.17.0.2:8000/?wsdl'

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

class CreateButton extends React.Component {
    render() {
        return (
            <button className="createbutton" onClick={this.props.onClick}>
                Create Room
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
            <button className="roombutton" onClick={this.props.onClick}>
                {this.props.text}
            </button>
        );
    }
}

class ShowRoomsButton extends React.Component {
    render() {
        return (
            <button className="showroomsbutton" onClick={this.props.onClick}>
                {this.props.text}
            </button>
        );
    }
}

class Chatbox extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            showchat: true,
            message: '',
            username: '',
            roomname: '',
            chatlog: [],
            rooms: []
        };
        this.handleMessageChange = this.handleMessageChange.bind(this);
        this.handleUsernameChange = this.handleUsernameChange.bind(this);
        this.handleRoomNameChange = this.handleRoomNameChange.bind(this);

        this.roomClick = this.roomClick.bind(this);
        this.showRoomsClick = this.showRoomsClick.bind(this);

        this.handleSendKeyPress = this.handleSendKeyPress.bind(this);
        this.handleLoginKeyPress = this.handleLoginKeyPress.bind(this);
        this.handleRoomNameKeyPress = this.handleRoomNameKeyPress.bind(this);

        this.initUser = this.initUser.bind(this);
        this.getChatlog = this.getChatlog.bind(this);
        this.getRooms = this.getRooms.bind(this);
    }

    // == Lifecycle ==

    componentDidMount() {
    }

    // == Rendering ==

    renderSendButton() {
        return (
            <SendButton
                onClick={() => this.sendClick()}
            />
        );
    }

    renderCreateButton() {
        return (
            <CreateButton
                onClick={() => this.createClick()}
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

    renderRoomButtons() {
        let buttons = [];

        for (let i = 0; i < this.state.rooms.length; i++) {
            buttons.push(<RoomButton
                text={this.state.rooms[i]}
                onClick={() => this.roomClick(i)}
                index={i}
            />);
        }
        return buttons;
    }

    renderShowRoomButton(_text) {
        return (
            <ShowRoomsButton
                onClick={() => this.showRoomsClick()}
                text={_text}
            />
        );
    }

    // == Handle ==

    sendClick() {
        this.sendMessage(this.state.message);
        this.setState({ message: '' });
    }

    createClick() {
        this.sendMessage("/room create " + this.state.roomname);
        this.setState({ roomname: '' });
    }

    loginClick() {
        this.initUser(this.state.username);
    }

    roomClick(i) {
        //alert(this.state.rooms[i]);
        this.sendMessage("/room join " + this.state.rooms[i]);
    }

    showRoomsClick(i) {
        if (this.state.showchat) {
            this.setState({ showchat: false });
        } else {
            this.setState({ showchat: true });
        }

    }

    handleSendKeyPress(event) {
        if (event.key === "Enter") {
            this.sendMessage(this.state.message);
            this.setState({ message: '' });
        }
    }

    handleLoginKeyPress(event) {
        if (event.key === "Enter") {
            this.initUser(this.state.message);
        }
    }

    handleRoomNameKeyPress(event) {
        if (event.key === "Enter") {
            this.sendMessage("/room create " + this.state.roomname);
            this.setState({ roomname: '' });
        }
    }

    handleMessageChange(event) {
        this.setState({ message: event.target.value });
    }

    handleUsernameChange(event) {
        this.setState({ username: event.target.value });
    }

    handleRoomNameChange(event) {
        this.setState({ roomname: event.target.value });
    }

    // == Functionality ==

    initUser() {
        username = this.state.username;

        console.log(username);

        if (username === "") {
            alert("Username cannot be empty");
        } else {
            this.registerUser();
            connected = true;
            setInterval(this.getChatlog, timeBetweenNextChatlogCheck);
            setInterval(this.getRooms, timeBetweenNextChatlogCheck);
            this.forceUpdate();
        }
    }

    // == Rest API ==

    // = POST =

    registerUser() {

        var soapMessage =
            '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:chat="chatroom">'+
            '<soapenv:Header/>'+
            '<soapenv:Body>'+
                '<chat:register_user>'+
                    '<chat:username>' + username + '</chat:username>'+
                '</chat:register_user>'+
            '</soapenv:Body>'+
            '</soapenv:Envelope>'

        $.ajax({
            url: webServiceURL,
            type: "POST",
            dataType: "xml",
            contentType: "text/plain",
            data: soapMessage,
        }).done(function (data) {
            console.log(data);
        });
    }

    sendMessage(message) {

        var soapMessage =
        '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:chat="chatroom">'+
        '<soapenv:Header/>'+
        '<soapenv:Body>'+
            '<chat:receive_message>'+
                '<chat:username>' + username + '</chat:username>'+
                '<chat:message>' + message + '</chat:message>'+
            '</chat:receive_message>'+
        '</soapenv:Body>'+
        '</soapenv:Envelope>'

        $.ajax({
            url: webServiceURL,
            type: "POST",
            dataType: "xml",
            contentType: "text/plain",
            data: soapMessage,
        }).done(function (data) {
            console.log(data);
        });
    }

    // = GET =

    getChatlog() {

        var soapMessage =
        '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:chat="chatroom">'+
        '<soapenv:Header/>'+
        '<soapenv:Body>'+
            '<chat:get_chatlog>'+
               '<chat:username>' + username + '</chat:username>'+
            '</chat:get_chatlog>'+
        '</soapenv:Body>'+
        '</soapenv:Envelope>'

        // Send Ajax JQuery Request and process the received JSON
        $.ajax({
            url: webServiceURL,
            type: "POST",
            dataType: "xml",
            contentType: "text/plain",
            data: soapMessage,
            complete: (data) => {
                // console.log(data);
                var processedData = JSON.parse(Object.values(data)[16]);
                // console.log(processedData);
                // console.log(processedData);
                this.setState({ chatlog: processedData });
            }
        });
    }

    getRooms() {

        var soapMessage =
        '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:chat="chatroom">'+
        '<soapenv:Header/>'+
        '<soapenv:Body>'+
            '<chat:get_rooms/>'+
        '</soapenv:Body>'+
        '</soapenv:Envelope>'

        // console.log("Get room initiated.")

        // Send Ajax JQuery Request and process the received JSON
        $.ajax({
            url: webServiceURL,
            type: "POST",
            dataType: "xml",
            contentType: "text/plain",
            data: soapMessage,
            complete: (data) => {
                // console.log(data);
                var processedData = JSON.parse(Object.values(data)[16]);
                // console.log(processedData);
                // console.log(processedData);
                this.setState({ rooms: processedData });
            }
        });
    }

    // == Render Self ==

    render() {
        // If connected, render out the chatbox and associated features.
        if (connected) {
            if (this.state.showchat) {
                return (
                    <div className="chat-box">
                        <div className="chat-title">
                            <p>Chatbox:</p>
                        </div>

                        <div className="chat-log">
                            {
                                this.state.chatlog.map(function (item, i) {
                                    //console.log("Item: " + item);
                                    return <p key={i}>{item}</p>
                                })
                            }
                        </div>

                        <div className="message-line">
                            Message: <input type="text" value={this.state.message} onChange={this.handleMessageChange} onKeyPress={this.handleSendKeyPress}></input>
                            {this.renderSendButton()}
                        </div>

                        <p>______________________________________________</p>

                        <div className="room-list">
                            <p>Rooms: </p>
                            {this.renderRoomButtons()}
                        </div>

                        <div className="create-room-line">
                            Room Name: <input type="text" value={this.state.roomname}
                                onChange={this.handleRoomNameChange}
                                onKeyPress={this.handleRoomNameKeyPress}>
                            </input>
                            {this.renderCreateButton()}
                        </div>

                        <div className="show-room-button">
                            {this.renderShowRoomButton("Show Rooms List")}
                        </div>

                    </div>
                );
            } else {
                return (
                    <div className="room-list">
                        <p>Active Rooms:</p>
                        {
                            this.state.rooms.map(function (item, i) {
                                return <p key={i}>{item}</p>
                            })
                        }
                        <div className="show-room-button">
                            {this.renderShowRoomButton("Hide Rooms List")}
                        </div>
                    </div>
                );
            }
        } else {
            // If not yet connected, display the not yet connected info.
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
