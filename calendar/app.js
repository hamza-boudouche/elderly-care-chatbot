const express = require('express')
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
	deleteEvent,
	addEvent,
	updateEvent,
	getEvent
} = require("./utils/CRUD/calendarCrud")

let creds;
let oAuth2Client;
const io = Server(server, {
	cors: {
		origin: "*",
		methods: ["GET", "POST"]
	}
});
const sockets = [];
const remind = (message) => {
	for (let i = 0; i < sockets.length; i++) {
		sockets[i].emit("reminder", message)
	}
}

io.on("connection", (socket) => {
	socket.on("ready", () => {
		sockets.push(socket)
	});
});

(async () => {
	console.log("testing")
	creds = await credentials("./credentials.json")
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
	let { minDate, maxDate } = req.params
	res.json(await listEvents(
		oAuth2Client,
		minDate,
		maxDate
	))
	return
})

app.post('/reminder', async (req, res) => {
	console.log(req.body)
	const {
		title,
		description,
		endTime,
		startTime,
		participants
	} = req.body
	if (remind) {
		remind(`rappel: vous avez ${title} de ${startTime} a ${endTime}`)
	} else {
		console.log("no user connected")
	}
	// remind(req.body)
	// console.log(events[i].getTitle(), events[i].getDescription(), events[i].getEndTime(), events[i].getStartTime())
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