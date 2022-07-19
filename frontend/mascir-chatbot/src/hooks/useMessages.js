import { useReducer } from 'react';

const reducer = (state, action) => {
  switch (action.type) {
    case 'addMessage':
      return { messages: [...state.messages, action.message] };
    default:
      throw new Error(`Invalid action ${action.type}`);
  }
};

const useMessages = (messages) => {
  const [state, dispatch] = useReducer(reducer, { messages });
  return [state, dispatch];
};

export default useMessages;
