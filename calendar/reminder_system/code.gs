function getEvents() {
  const calendarID = "boudouchehamza2@gmail.com";
  const callbackURL = "https://e4f5-196-200-149-100.ngrok.io/echo";
  let calendar = CalendarApp.getCalendarById(calendarID);
  let now = new Date();
  let after24hours = new Date(now.getTime() + 24 * 60 * 60 * 1000);
  let events = calendar.getEvents(now, after24hours);
  console.log(events.length);
  for (let i = 0; i < events.length; i++) {
    const resp = UrlFetchApp.fetch(callbackURL);
    console.log(resp);
  }
}
