import { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import { useAuth0 } from "@auth0/auth0-react";

const useSend = (callbackMessage) => {
  const url = 'http://localhost:5005/';
  const [socket, setSocket] = useState();
  const { user, getAccessTokenSilently, loginWithRedirect } = useAuth0();
  // const user = {
  //   email: "boudouchehamza2@gmail.com"
  // }

  // const loginWithRedirect = () => { }

  useEffect(() => {
    setSocket(
      io(url)
    );
    console.log("socket set")
  }, []);

  useEffect(() => {
    socket && socket.emit("session_request", {
      session_id: "some id"
    });
    socket &&
      socket.on('reply', (message) => {
        console.log(message);
        callbackMessage({ text: message.text });
      });
    console.log("reply callback set")
  }, [callbackMessage, socket]);

  const sendMessage = ({ text }) => {
    if (!user) {
      alert("Please log in first to be able to talk to the chatbot")
      loginWithRedirect()
    }
    socket.emit("message", {
      sender: user.email,
      message: text,
      session_id: "some id",
    });
  };

  return [sendMessage];
};

export default useSend;
