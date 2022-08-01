const express = require('express')
const app = express()
const port = process.env.PORT || 3000
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

app.listen(port, () => {
	console.log(`Example app listening on port ${port}`)
})