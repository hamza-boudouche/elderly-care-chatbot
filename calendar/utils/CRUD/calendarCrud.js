const { google } = require('googleapis');

/**
 * 
 * @param {google.auth.OAuth2} auth 
 * @param {string} min 
 * @param {string} max 
 */
function listEvents(auth, min = (new Date()).toISOString(), max = (new Date((new Date()).getTime() + 86400000)).toISOString()) {
	const calendar = google.calendar({ version: 'v3', auth });
	return new Promise((resolve, reject) => {
		calendar.events.list({
			calendarId: 'primary',
			timeMin: min,
			timeMax: max,
			singleEvents: true,
			orderBy: 'startTime',
		}, (err, res) => {
			if (err) reject('The API returned an error: ' + err);
			const events = res.data.items;
			resolve(events)
		});
	})
}

/**
 * 
 * @param {google.auth.OAuth2} auth 
 * @param {string} id 
 */
function getEvent(auth, id) {
	const calendar = google.calendar({ version: 'v3', auth });
	return new Promise((resolve, reject) => {
		calendar.events.get({
			auth: auth,
			calendarId: 'primary',
			eventId: id
		}, function (err, event) {
			if (err) {
				reject('There was an error contacting the Calendar service: ' + err);
			}
			resolve(event.data);
		});
	})
}


/**
 * 
 * @param {google.auth.OAuth2} auth 
 * @param {string} id 
 */
function deleteEvent(auth, id) {
	const calendar = google.calendar({ version: 'v3', auth });
	return new Promise((resolve, reject) => {
		calendar.events.delete({ eventId: id, calendarId: 'primary' }, function (err, event) {
			if (err) {
				reject('There was an error contacting the Calendar service: ' + err);
			}
			resolve(event);
		});
	})
}

/**
 * 
 * @param {google.auth.OAuth2} auth 
 * @param {string} summary 
 * @param {string} location 
 * @param {string} description 
 * @param {Object} start 
 * @param {string} start.dateTime
 * @param {string} start.timeZone
 * @param {Object} end 
 * @param {string} end.dateTime
 * @param {string} end.timeZone
 * @param {Array<string>} recurrence example: 'RRULE:FREQ=DAILY;COUNT=2'
 * @param {Object[]} attendees 
 * @param {string} attendees.email
 * @param {Object} reminders 
 * @param {boolean} reminders.useDefault
 * @param {Object[]} reminders.overrides
 * @param {"email" | "popup"} reminders.overrides.method
 * @param {number} reminders.overrides.minutes
 */
async function addEvent(auth, summary, location, description, start, end, recurrence, attendees, reminders) {
	const calendar = google.calendar({ version: 'v3', auth });
	const event = {
		'summary': summary,
		'location': location,
		'description': description,
		'start': {
			'dateTime': start.dateTime,
			'timeZone': start.timeZone
		},
		'end': {
			'dateTime': end.dateTime,
			'timeZone': end.timeZone
		},
		'recurrence': recurrence,
		'attendees': attendees,
		'reminders': reminders,
	};
	return new Promise((resolve, reject) => {
		calendar.events.insert({
			auth: auth,
			calendarId: 'primary',
			resource: event,
		}, function (err, event) {
			if (err) {
				reject('There was an error contacting the Calendar service: ' + err);
			}
			resolve(event.data);
		});
	})
}

/**
 * 
 * @param {google.auth.OAuth2} auth 
 * @param {string} id 
 * @param {string} summary 
 * @param {string} location 
 * @param {string} description 
 * @param {Object} start 
 * @param {string} start.dateTime
 * @param {string} start.timeZone
 * @param {Object} end 
 * @param {string} end.dateTime
 * @param {string} end.timeZone
 * @param {Array<string>} recurrence example: 'RRULE:FREQ=DAILY;COUNT=2'
 * @param {Object[]} attendees 
 * @param {string} attendees.email
 * @param {Object} reminders 
 * @param {boolean} reminders.useDefault
 * @param {Object[]} reminders.overrides
 * @param {"email" | "popup"} reminders.overrides.method
 * @param {number} reminders.overrides.minutes
 */
async function updateEvent(auth, id, summary, location, description, start, end, recurrence, attendees, reminders) {
	const calendar = google.calendar({ version: "v3", auth })
	try {
		const oldEvent = await getEvent(auth, id);
		const event = await calendar.events.update({
			auth: auth,
			calendarId: 'primary',
			eventId: id,
			requestBody: {
				'summary': summary || oldEvent.summary,
				'location': location || oldEvent.location,
				'description': description || oldEvent.description,
				'start': {
					'dateTime': start?.dateTime || oldEvent.start.dateTime,
					'timeZone': start?.timeZone || oldEvent.start.timeZone
				},
				'end': {
					'dateTime': end?.dateTime || oldEvent.end.dateTime,
					'timeZone': end?.timeZone || oldEvent.end.timeZone
				},
				'recurrence': recurrence || oldEvent.recurrence,
				'attendees': attendees || oldEvent.attendees,
				'reminders': reminders || oldEvent.reminders,
			}
		})
		return event.data
	} catch (error) {
		throw new Error(error)
	}
}

module.exports = {
	listEvents,
	deleteEvent,
	addEvent,
	updateEvent,
	getEvent
}
