const calendarID = "boudouchehamza2@gmail.com"; // id of the calendar used to store system events
const callbackURL = "https://833d-196-200-149-100.ngrok.io/reminder"; // url of the calendar microservice
const firstIntervalLength = 5; // in minutes
const secondIntervalLength = 30; // in minutes
const calendar = CalendarApp.getCalendarById(calendarID);
const now = new Date();
// get all events in time interval (between start and end)
function getEvents(intervalLength) {
  const start = new Date(now.getTime() + firstIntervalLength * 60 * 1000);
  const end = new Date(now.getTime() + (firstIntervalLength + 1) * 60 * 1000);
  let events = calendar.getEvents(start, end);
  events = events.filter(
    (event) =>
      Math.abs(event.getStartTime() - now) / (1000 * 60) >= intervalLength
  );
  console.log(events.length);
  return events;
}

function getNewEvents(intervalLength) {
  const start = now;
  const end = new Date(now.getTime() + intervalLength * 60 * 1000);
  let events = calendar.getEvents(start, end);
  events = events.filter(
    (event) =>
      Math.abs(event.getStartTime() - now) / (1000 * 60) >= intervalLength ||
      Math.abs(event.getLastUpdated() - now) / (1000 * 60) <= 1
  );
  console.log(events.length);
  return events;
}

function parseDescription(description) {
  if (description !== "") {
    const lines = description.split("\n");
    if (lines[0] === "meeting:" && lines.length > 2) {
      const meetingData = JSON.parse(lines[1]);
      lines.splice(0, 2);
      return {
        url: meetingData["url"],
        password: meetingData["password"],
        description: lines.join("\n"),
      };
    }
  }
  return {
    description,
  };
}

// send data param (obj) to callback URL in the body of a POST request
function sendReminder(event) {
  const data = {
    title: event.getTitle(),
    endTime: event.getEndTime(),
    startTime: event.getStartTime(),
    participants: event.getGuestList((includeOwner = true)).map((guest) => {
      return {
        email: guest.getEmail(),
        name: guest.getName(),
      };
    }),
    ...parseDescription(event.getDescription()),
  };
  const payload = JSON.stringify(data);
  const options = {
    method: "POST",
    contentType: "application/json",
    payload: payload,
  };
  UrlFetchApp.fetch(callbackURL, options);
}

// this is the function to use for the installable time-driver trigger
function main() {
  const eventsIn5mins = getEvents(firstIntervalLength);
  for (let i = 0; i < eventsIn5mins.length; i++) {
    sendReminder(eventsIn5mins[i]);
  }
  const newEventsIn5mins = getNewEvents(firstIntervalLength);
  for (let i = 0; i < newEventsIn5mins.length; i++) {
    sendReminder(newEventsIn5mins[i]);
  }
  const eventsIn30mins = getEvents(secondIntervalLength);
  for (let i = 0; i < eventsIn30mins.length; i++) {
    sendReminder(eventsIn30mins[i]);
  }
  const newEventsIn30mins = getNewEvents(secondIntervalLength);
  for (let i = 0; i < newEventsIn30mins.length; i++) {
    sendReminder(newEventsIn30mins[i]);
  }
}
