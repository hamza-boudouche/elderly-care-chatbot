import React, { useRef, useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import botPic from "../assets/bot.png";
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

const Message = ({ message: { local, text }, hidden, end }) => {
  const { user } = useAuth0();
  const messageClass = local ? 'sent' : 'received';
  const ref = useRef(null)
  console.log(user)

  useEffect(() => {
    console.log(ref.current);
  }, [ref]);

  return (
    <div className={`message ${messageClass} ${hidden ? "hidden" : ""}`} id={end ? "end" : ""} ref={ref}>
      <div className="avatar">
        <img
          src={messageClass === "sent" && user?.picture ? user?.picture : botPic}
          alt="avatar"
          style={{
            width: 50,
            height: 50,
            borderRadius: "50%",
            backgroundColor: "rgb(167, 171, 174)",
            border: "1px solid grey"
          }}
        />
      </div>
      <div className="message-body">
        <p>
          <ReactMarkdown remarkPlugins={[remarkGfm]} >
            {
              text
            }
          </ReactMarkdown>
        </p>
      </div>
    </div >
  );
};

export default Message;
