import React, { useContext, useRef, useCallback, useState, useEffect } from "react";
import Message from "./Message";
import useSend from "../hooks/useSend";
import MessagesContext from "../context/MessagesContext";
import useMessages from "../hooks/useMessages";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import FormMessage from './FormMessage';
// import { ipcRenderer } from "electron";

const Chatbot = () => {
  const myMessages = useContext(MessagesContext);
  const [state, dispatch] = useMessages(myMessages);
  const dummy = useRef();
  const [btnVisible, setBtnVisible] = useState(false)

  const observer = new IntersectionObserver(
    ([entry]) => {
      setBtnVisible(!entry.isIntersecting)
    }
  )

  useEffect(() => {
    observer.observe(dummy.current)
    return () => { observer.disconnect() }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [dummy])

  const addReplyMessage = useCallback(
    ({ text }) => {
      const msg = new SpeechSynthesisUtterance()
      const textForSpeech = text.replaceAll("-", "")
      msg.text = textForSpeech
      // window.speechSynthesis.speak(msg)
      dispatch({
        type: "addMessage",
        message: {
          text,
          local: false,
        },
      });
      dummy.current.scrollIntoView({ behavior: "smooth" });
      console.log(text);
    },
    [dispatch, dummy]
  );

  const checkReplyMessage = useCallback(
    (message) => {
        window.api.send("message.receive", message)
      if (message.custom?.action === undefined) {
        addReplyMessage({ text: message.text })
        console.log("sending message")
        window.api.send("message.receive", message.text)
      } else {
        switch (message.custom?.action.type) {
          case "selenium.open":
            window.api.send("selenium.open", message.custom?.action.payload)
            break;
          case "selenium.close":
            window.api.send("selenium.close", message.custom?.action.payload)
            break;
          case "selenium.youtube.close":
            window.api.send("selenium.youtube.close", message.custom?.action.payload)
            break;
          case "selenium.youtube.open":
            window.api.send("selenium.youtube.open", message.custom?.action.payload)
            break;
          case "selenium.youtube.playPause":
            window.api.send("selenium.youtube.playPause", message.custom?.action.payload)
            break;
          case "selenium.youtube.skipForward":
            window.api.send("selenium.youtube.skipForward", message.custom?.action.payload)
            break;
          case "selenium.youtube.skipBackward":
            window.api.send("selenium.youtube.skipBackward", message.custom?.action.payload)
            break;
          case "selenium.youtube.prevVideo":
            window.api.send("selenium.youtube.prevVideo", message.custom?.action.payload)
            break;
          case "selenium.youtube.nextVideo":
            window.api.send("selenium.youtube.nextVideo", message.custom?.action.payload)
            break;
          default:
            console.log("unsupported action type")
            break;
        }
      }
    }, [addReplyMessage]
  );

  useEffect(() => {
    dummy.current.scrollIntoView({ behavior: "smooth" });
  }, [state.messages])

  const [sendMessageSocket] = useSend(checkReplyMessage);

  const sendMessage = (messageValue) => {
    dispatch({
      type: "addMessage",
      message: {
        text: messageValue,
        local: true,
      },
    });
    sendMessageSocket({ text: messageValue });
    dummy.current.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="chatbot">
      <div className="messages-list">
        {btnVisible && <a href="#end">
          <div id="end-link" onClick={() => dummy.current.scrollIntoView({ behavior: "smooth" })}>
            <KeyboardArrowDownIcon />
          </div>
        </a>}
        {state.messages &&
          state.messages.map((msg, index) =>
            <Message
              key={index}
              message={msg}
              end={index === state.messages.length - 1}
              setBtnVisible={setBtnVisible}
            />
          )}
        <div ref={dummy} style={{
          width: 20,
          height: 20,
        }}></div>
        <Message message="" hidden={true} />
      </div>
      <FormMessage sendMessage={sendMessage} dummy={dummy} />
    </div>
  );
};

export default Chatbot;
