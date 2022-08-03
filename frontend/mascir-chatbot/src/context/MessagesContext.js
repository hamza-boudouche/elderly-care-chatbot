import React from 'react';

const MessagesContext = React.createContext([
  {
    local: true,
    text: 'Hello',
  },
  {
    local: false,
    text: 'Hey, how can I help you ?',
  },
]);

export default MessagesContext;
