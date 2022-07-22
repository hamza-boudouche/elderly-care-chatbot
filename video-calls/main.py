from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from app.utils import createMeeting

app = FastAPI()


class MeetingInfo(BaseModel):
    time: datetime
    duration: int
    title: str | None = "Meeting"


@app.post("/meeting/")
async def getmeeting(meetingInfo: MeetingInfo):
    join_URL, meetingPassword = await createMeeting(
        title="The title of your zoom meeting",
        time=meetingInfo.time.strftime("%Y-%m-%dT%H:%M:%S"), duration=str(meetingInfo.duration)
    )
    return {
        "url": join_URL,
        "password": meetingPassword
    }
