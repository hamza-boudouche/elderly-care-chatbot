const calendarID = "boudouchehamza2@gmail.com"; // id of the calendar used to store system events
const callbackURL = "https://b020-196-200-149-100.ngrok.io/reminder"; // url of the calendar microservice
const intervalLength = 30; // in minutes
const now = new Date();
// 2 rappels 30 mins et 5 mins
// get all events in time interval (between start and end)
function getEvents(
  start = new Date(now.getTime() + intervalLength * 60 * 1000),
  end = new Date(now.getTime() + (intervalLength + 1) * 60 * 1000)
) {
  let calendar = CalendarApp.getCalendarById(calendarID);
  let events = calendar.getEvents(start, end);
  console.log(events.length);
  return events;
}

// send data param (obj) to callback URL in the body of a POST request
function sendReminder(data) {
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
  const events = getEvents();
  for (let i = 0; i < events.length; i++) {
    // console.log(events[i].getTitle(), events[i].getDescription(), events[i].getEndTime(), events[i].getStartTime(), events[i].getGuestList(includeOwner=true))
    sendReminder({
      title: events[i].getTitle(),
      description: events[i].getDescription(),
      endTime: events[i].getEndTime(),
      startTime: events[i].getStartTime(),
      participants: events[i]
        .getGuestList((includeOwner = true))
        .map((guest) => {
          return {
            email: guest.getEmail(),
            name: guest.getName(),
          };
        }),
    });
  }
}
