const express = require('express')
const fetch = require("node-fetch")
const Server = require("socket.io")
const http = require('http');
const app = express()
const server = http.createServer(app);
const port = process.env.PORT || 4000
const {
	credentials,
	authorize,
	refreshAccessToken
} = require("./utils/auth/authClient")
const {
	listEvents,
	listEventsByAttendee,
	deleteEvent,
	addEvent,
	updateEvent,
	getEvent
} = require("./utils/CRUD/calendarCrud")

const DOMAIN = "dev--r9nce6d.us.auth0.com"

let creds;
let oAuth2Client;
const io = Server(server, {
	cors: {
		origin: "*",
		methods: ["GET", "POST"]
	}
});
const sockets = {};
const remind = (user, channel, message) => {
	if (user in sockets) {
		for (let socket in sockets[user]) {
			socket.emit(channel, message)
		}
	}
}

io.use(async (socket, next) => {
	if (socket.handshake.query && socket.handshake.query.token) {
		const res = await fetch(`https://${DOMAIN}/userinfo`, {
			headers: { 'Authorization': `Bearer ${socket.handshake.query.token}` },
		})
		if (res.status === 401) {
			next(new Error('Authentication error'));
		}
		const data = await res.json()
		socket.email = data.email
		next()
	}
	else {
		next(new Error('Authentication error'));
	}
})

io.on("connection", (socket) => {
	console.log(`user connected: ${socket.email}`)
	socket.on("ready", () => {
		if (socket.email in sockets) {
			sockets[socket.email].push(socket)
		} else {
			sockets[socket.email] = [socket]
		}
	});
});

(async () => {
	console.log("testing")
	creds = await credentials("./credentials.json")
	// oAuth2Client = await authorize(creds)
	while (true) {
		try {
			oAuth2Client = await authorize(creds)
			await listEvents(oAuth2Client)
			break;
		} catch (error) {
			await refreshAccessToken()
		}
	}
})()

app.use(express.json());

app.get('/single/:eventId', async (req, res) => {
	res.json(await getEvent(oAuth2Client, req.params.eventId))
})

app.get('/range/:minDate?/:maxDate?', async (req, res) => {
	const email = req.headers["X-mascir-chatbot-email"]
	const { minDate, maxDate } = req.params
	res.json(await listEventsByAttendee(
		oAuth2Client,
		email,
		minDate,
		maxDate
	))
	return
})

app.post('/reminder', async (req, res) => {
	// TODO: secure this endpoint (by a jtw token generated for the party allowed to send reminders to users (must be coming from a domain name owned by google))
	console.log(req.headers)
	console.log(req.body)
	const {
		title,
		description,
		endTime,
		startTime,
		participants,
		url,
		password,
	} = req.body
	if (remind) {
		for (let participant in participants) {
			if (url) {
				remind(participant.email, "reminder", `rappel: vous avez ${title} de ${startTime} a ${endTime}, rejoignez la reunion associée ${url} , mot de passe: ${password}`)
				remind(participant.email, "electron.zoom.open", url)
			} else {
				remind(participant.email, "reminder", `rappel: vous avez ${title} de ${startTime} a ${endTime}`)
			}
		}
	} else {
		console.log("no user connected")
	}
	res.json({
		ok: true
	})
})

app.post('/', async (req, res) => {
	const {
		summary,
		location,
		description,
		start,
		end,
		recurrence,
		attendees,
		reminders
	} = req.body;
	const data = await addEvent(oAuth2Client, summary, location, description, start, end, recurrence, attendees, reminders)
	res.json(data)
})

app.put('/:eventId', async (req, res) => {
	const {
		summary,
		location,
		description,
		start,
		end,
		recurrence,
		attendees,
		reminders
	} = req.body;
	const data = await updateEvent(oAuth2Client, req.params.eventId, summary, location, description, start, end, recurrence, attendees, reminders)
	res.json(data)
})

app.delete('/:eventId', async (req, res) => {
	await deleteEvent(oAuth2Client, req.params.eventId)
	res.json({ message: `event ${req.params.eventId} deleted` })
})

server.listen(port, () => {
	console.log(`Example app listening on port ${port}`)
})