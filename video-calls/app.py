from utils import createMeeting

if __name__ == "__main__":
    # tests
    # run the create meeting function
    join_URL, meetingPassword = createMeeting(
        title="The title of your zoom meeting",
        time="2019-06-14T10: 21: 57", duration="45"
    )
    print(join_URL, meetingPassword)
