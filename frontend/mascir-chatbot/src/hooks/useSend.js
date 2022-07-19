import { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import { useAuth0 } from "@auth0/auth0-react";

const useSend = (callbackMessage) => {
  const url = 'http://localhost:5005';
  const [socket, setSocket] = useState();
  const { user, getAccessTokenSilently } = useAuth0();

  useEffect(() => {
    setSocket(
      io(url)
    );
    console.log("socket set")
  }, []);

  useEffect(() => {
    socket &&
      socket.on('reply', (message) => {
        console.log(message);
        callbackMessage({ text: message.text });
      });
    console.log("reply callback set")
  }, [callbackMessage, socket]);

  const sendMessage = ({ text }) => {
    socket.emit("message", {
      sender: user.email,
      message: text,
      session_id: user.email,
    });
  };

  return [sendMessage];
};

export default useSend;
