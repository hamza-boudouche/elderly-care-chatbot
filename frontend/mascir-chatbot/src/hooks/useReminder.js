import { useState, useEffect } from 'react';
import { io } from 'socket.io-client';

const useReminder = (callbackMessage) => {
	const url = 'http://localhost:4000';
	const [socket, setSocket] = useState();

	useEffect(() => {
		setSocket(
			io(url)
		);
		console.log("reminder socket set")
	}, []);

	useEffect(() => {
		socket && socket.emit("ready", "i guess the message shouldn't be empty");
		socket &&
			socket.on('reminder', (message) => {
				console.log(message);
				callbackMessage({
					text: message
				});
			});
		console.log("reply callback set")
	}, [callbackMessage, socket]);
};

export default useReminder;
