import { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import { useAuth0 } from "@auth0/auth0-react";


const useReminder = (callbackMessage) => {
	const url = 'http://localhost:4000';
	const [socket, setSocket] = useState();
	const { user, getAccessTokenSilently, loginWithRedirect } = useAuth0();


	useEffect(() => {
		const fetchDataAndCreateSocket = async () => {
			const token = await getAccessTokenSilently();
			console.log(token)
			setSocket(
				io(url, {
					query: { token }
				})
			);
			console.log("reminder socket set")
		}
		fetchDataAndCreateSocket().catch(console.error)
	}, [getAccessTokenSilently]);

	useEffect(() => {
		socket && socket.emit("ready", "i guess the message shouldn't be empty");
		socket &&
			socket.on('reminder', (message) => {
				console.log(message);
				callbackMessage({
					text: message
				});
			});
		socket && socket.on('electron.zoom.open', (url) => {
			console.log(url);
			window.api.send("electron.zoom.open", url)
		});
		console.log("reply callback set")
	}, [callbackMessage, socket]);
};

export default useReminder;
