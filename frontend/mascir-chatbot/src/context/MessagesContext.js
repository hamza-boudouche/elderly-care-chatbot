import React from 'react';

const MessagesContext = React.createContext([
  {
    local: true,
    text: 'hello world',
  },
  {
    local: false,
    text: 'hello',
  },
]);

export default MessagesContext;
