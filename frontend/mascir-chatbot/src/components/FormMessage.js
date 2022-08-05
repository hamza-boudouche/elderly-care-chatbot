import React, { useState, useRef } from 'react';
import MicNoneIcon from '@mui/icons-material/MicNone';
import MicIcon from '@mui/icons-material/Mic';
import SendIcon from '@mui/icons-material/Send';
import { createSpeechlySpeechRecognition } from '@speechly/speech-recognition-polyfill';
import SpeechRecognition, {
  useSpeechRecognition,
} from 'react-speech-recognition';

const appId = 'efdfa8e3-4e48-488e-a360-fd4bbf4104fe';
const SpeechlySpeechRecognition = createSpeechlySpeechRecognition(appId);
SpeechRecognition.applyPolyfill(SpeechlySpeechRecognition);

const FormMessage = ({ sendMessage, dummy }) => {
  const [messageValue, setMessageValue] = useState('');
  const [listening, setListening] = useState(false);
  const { transcript, resetTranscript } = useSpeechRecognition();

  const microphoneRef = useRef(null);

  const startListening = (e) => {
    e.preventDefault();
    resetTranscript();
    setListening(true);
    SpeechRecognition.startListening({ continuous: true, language: "fr-FR" });
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
    if (messageValue) {
      e.preventDefault();
      sendMessage(messageValue);
      setMessageValue('');
      dummy.current.scrollIntoView({ behavior: "smooth" })
    }
  }

  return (
    <form onSubmit={handleSubmit} className="form">
      <input
        value={listening ? transcript.toLowerCase() : messageValue.toLowerCase()}
        onChange={(e) => setMessageValue(e.target.value)}
        placeholder="Message #Chatbot"
        type="text"
        className="message-field"
      />
      <div className='form-btn voice-btn' style={{
        display: 'grid',
        alignItems: "center",
        justifyContent: "center"
      }}>
        {
          listening ?
            <MicIcon fontSize='large' onClick={stopListening} />
            :
            <MicNoneIcon fontSize='large' onClick={startListening} />
        }
      </div>
      <div className='form-btn voice-btn' style={{
        display: 'grid',
        alignItems: "center",
        justifyContent: "center"
      }}>
        <SendIcon onClick={handleSubmit} />
      </div>
    </form>
  );
};

export default FormMessage;
