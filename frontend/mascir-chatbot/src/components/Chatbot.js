import React, { useContext, useRef, useCallback, useState, useEffect } from "react";
import Message from "./Message";
import useSend from "../hooks/useSend";
import MessagesContext from "../context/MessagesContext";
import useMessages from "../hooks/useMessages";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import FormMessage from './FormMessage';
// import { ipcRenderer } from "electron";
import useReminder from './../hooks/useReminder';

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
    ({ text }) => {
      let custom;
      try {
        custom = JSON.parse(text)
        window.api.send("message.receive", `action type: ${custom.action.type}`)
        switch (custom.action.type) {
          case "selenium.open":
            window.api.send("selenium.open", custom.action.payload)
            break;
          case "selenium.close":
            window.api.send("selenium.close", custom.action.payload)
            break;
          case "selenium.youtube.close":
            window.api.send("selenium.youtube.close", custom.action.payload)
            break;
          case "selenium.youtube.open":
            window.api.send("selenium.youtube.open", custom.action.payload)
            break;
          case "selenium.youtube.playPause":
            window.api.send("selenium.youtube.playPause", custom.action.payload)
            break;
          case "selenium.youtube.skipForward":
            window.api.send("selenium.youtube.skipForward", custom.action.payload)
            break;
          case "selenium.youtube.skipBackward":
            window.api.send("selenium.youtube.skipBackward", custom.action.payload)
            break;
          case "selenium.youtube.prevVideo":
            window.api.send("selenium.youtube.prevVideo", custom.action.payload)
            break;
          case "selenium.youtube.nextVideo":
            window.api.send("selenium.youtube.nextVideo", custom.action.payload)
            break;
          default:
            window.api.send("message.receive", "unsupported action type")
            break;
        }
      } catch (error) {
        addReplyMessage({ text })
        window.api.send("message.receive", text)
      }
    }, [addReplyMessage]
  );

  useEffect(() => {
    dummy.current.scrollIntoView({ behavior: "smooth" });
  }, [state.messages])

  const [sendMessageSocket] = useSend(checkReplyMessage);
  useReminder(addReplyMessage);

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
