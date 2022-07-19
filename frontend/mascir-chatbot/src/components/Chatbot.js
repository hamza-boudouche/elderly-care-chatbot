import React, { useContext, useRef, useCallback, useState, useEffect } from "react";
import Message from "./Message";
import useSend from "../hooks/useSend";
import MessagesContext from "../context/MessagesContext";
import useMessages from "../hooks/useMessages";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import FormMessage from './FormMessage';

const Chatbot = () => {
  const myMessages = useContext(MessagesContext);
  const [state, dispatch] = useMessages(myMessages);
  const dummy = useRef();
  const [btnVisible, setBtnVisible] = useState(false)

  const observer = new IntersectionObserver(
    ([entry]) => {
      console.log(entry)
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

  useEffect(() => {
    dummy.current.scrollIntoView({ behavior: "smooth" });
  }, [state.messages])

  const [sendMessageSocket] = useSend(addReplyMessage);

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
