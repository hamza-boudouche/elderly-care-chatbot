import React, { useState, useRef } from 'react';
import SpeechRecognition, {
  useSpeechRecognition,
} from 'react-speech-recognition';

const FormMessage = ({ sendMessage, dummy }) => {
  const [messageValue, setMessageValue] = useState('');
  const [listening, setListening] = useState(false);
  const { transcript, resetTranscript } = useSpeechRecognition();

  const microphoneRef = useRef(null);

  const startListening = (e) => {
    e.preventDefault();
    resetTranscript();
    setListening(true);
    SpeechRecognition.startListening({ continuous: true });
  };

  const stopListening = (e) => {
    e.preventDefault();
    SpeechRecognition.stopListening();
    setMessageValue(transcript);
    setListening(false);
    microphoneRef.current.classList.remove('listening');
    resetTranscript();
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(messageValue);
    setMessageValue('');
    dummy.current.scrollIntoView({ behavior: "smooth" })
  }

  return (
    <form onSubmit={handleSubmit} className="form">
      <input
        value={listening ? transcript : messageValue}
        onChange={(e) => setMessageValue(e.target.value)}
        placeholder="Message #Chatbot"
        type="text"
        className="message-field"
      />
      <input
        type="button"
        className="form-btn voice-btn"
        value={listening ? 'stop' : 'start'}
        onClick={listening ? stopListening : startListening}
      />
      <input
        type="submit"
        className="form-btn send-btn"
        value="Send"
        disabled={!messageValue}
      />
    </form>
  );
};

export default FormMessage;
