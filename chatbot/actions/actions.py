from cgitb import text
import json
from typing import Any, Text, Dict, List
import aiohttp

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict

from actions.utils import actionEventsToday
from actions.utils import actionEventsRange
from actions.utils import actionDeleteEvent
from actions.utils import actionAddEvent
from actions.utils import actionUpdateEvent
from actions.utils import actionAdditionalInfo

from deep_translator import GoogleTranslator
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import nltk
import wikipedia
import wikipediaapi

import os
from pathlib import Path
import flair
from flair.data import Sentence
from flair.models import SequenceTagger

from youtubesearchpython.__future__ import VideosSearch


# POS-french
# model_2 = SequenceTagger.load('./pos-french/pytorch_model.bin')

# BlenderBot model
model = BlenderbotForConditionalGeneration.from_pretrained(
    "./blenderbot-400M-distill", local_files_only=True)
tokenizer = BlenderbotTokenizer.from_pretrained(
    "./blenderbot-400M-distill", local_files_only=True)

DOMAIN = "dev--r9nce6d.us.auth0.com"


class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Voici les événements que vous avez pour les prochaines 24 heures")
        events = await actionEventsToday()
        for event in events:
            dispatcher.utter_message(text=event.get("text"))
        return [SlotSet("events", events)]


class ActionAuthenticateUser(Action):
    def name(self) -> Text:
        return "action_authenticate_user"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        last_message = tracker.latest_message.text
        token = last_message.split(" ")
        if token[0] == "token":
            async with aiohttp.ClientSession() as session:
                res = await session.get(url=f"{DOMAIN}/userinfo", headers={
                    "Authorization": f"Bearer {token[1]}"
                })
                if res.status != 401:
                    data = await res.json()
                    return [SlotSet("email", data.email)]
        # implement logic to redirect user to authenticate before the first message (dispatch a json message with action = "auth.login.redirect")
        return []


class ActionEventsToday(Action):

    def name(self) -> Text:
        return "action_get_events_today"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Voici les événements que vous avez pour les prochaines 24 heures")
        events = await actionEventsToday()
        for event in events:
            dispatcher.utter_message(text=event.get("text"))
        return [SlotSet("events", events)]


class ActionEventsRange(Action):
    def name(self) -> Text:
        return "action_get_events_range"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        start = tracker.get_slot('start')
        end = tracker.get_slot('end')
        dispatcher.utter_message(
            text=f"Here are the events you have between {start} and {end}")
        events = await actionEventsRange(start, end)
        for event in events:
            dispatcher.utter_message(text=event.get("text"))
        return [SlotSet("events", events)]


class ActionDeleteEvent(Action):
    def name(self) -> Text:
        return "action_delete_event"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        events = tracker.get_slot('events')
        humanIndex = tracker.get_slot('human_index')
        event = tracker.get_slot('event')
        dispatcher.utter_message(
            text=f"deleting the event no {humanIndex}")
        messages, newEvents = await actionDeleteEvent(humanIndex, events, event)
        for message in messages:
            dispatcher.utter_message(text=message.get("text"))
        return [SlotSet("events", newEvents)]


class ActionAddEvent(Action):
    def name(self) -> Text:
        return "action_add_event"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        summary = tracker.get_slot('summary')
        start = tracker.get_slot('start')
        end = tracker.get_slot('end')
        description = tracker.get_slot('description')

        with_meeting = tracker.get_slot('with_meeting')
        withMeeting = False
        if with_meeting == 'oui':
            withMeeting = True

        messages, newEvent = await actionAddEvent(summary, description, start, end, withMeeting)

        if withMeeting == False:
            dispatcher.utter_message(text=f"Création d'un nouveau evenement ...")
        else:
            dispatcher.utter_message(text=f"Création d'une nouvelle réunion sur ZOOM...")

        for message in messages:
            dispatcher.utter_message(text=message.get("text"))
        return [SlotSet("event", newEvent)]


class ActionResetCreate(Action):
    def name(self) -> Text:
        return "action_reset_ceate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("summary", None), SlotSet("start", None), SlotSet("end", None), SlotSet("description", None)]


class ActionUpdateEvent(Action):
    def name(self) -> Text:
        return "action_update_event"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=f"modifying the event...")
        event = tracker.get_slot('event')
        summary = tracker.get_slot('summary')
        start = tracker.get_slot('start')
        end = tracker.get_slot('end')
        humanIndex = tracker.get_slot('human_index')
        description = tracker.get_slot('description')
        messages, updatedEvent = await actionUpdateEvent(event, humanIndex, summary, description, start, end)
        for message in messages:
            dispatcher.utter_message(text=message.get("text"))
        return []


class ActionAdditionalInfo(Action):
    def name(self) -> Text:
        return "action_additional_info"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("inside the additional info action")
        search_query = tracker.get_slot('search_query')
        messages = await actionAdditionalInfo(search_query)
        for message in messages:
            dispatcher.utter_message(text=message.get("text"))
        return []


class ValidateCreateForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_create_form"

    def validate_start(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate start value."""

        try:
            slot_value = slot_value['from']
            return {"start": slot_value}
        except:
            return {"start": slot_value}

    def validate_end(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate end value."""

        try:
            slot_value = slot_value['from']
            return {"end": slot_value}
        except:
            return {"end": slot_value}

    def validate_summary(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate description value."""

        return {"summary": slot_value}

    def validate_description(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate description value."""

        return {"description": slot_value}


class ActionWikipedia(Action):
    def name(self) -> Text:
        return "action_wikipedia"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Delete all what is between brackets :
        def clean(test_str):
            ret = ''
            skip1c = 0
            skip2c = 0
            for i in test_str:
                if i == '[':
                    skip1c += 1
                elif i == '(':
                    skip2c += 1
                elif i == ']' and skip1c > 0:
                    skip1c -= 1
                elif i == ')' and skip2c > 0:
                    skip2c -= 1
                elif skip1c == 0 and skip2c == 0:
                    ret += i
            return ret

        # translate user question to english :
        text = tracker.latest_message['text']

        # POS tagging :
        sentence = Sentence(text)
        model_2.predict(sentence)
        sentence.to_tagged_string()

        pos_val = []
        for token in list(sentence):
            pos_val.append((token.form, token.tag))

        # delete indesirable words and construct the keyword
        to_keep = ['PREP', 'PROPN', 'XFAMIL', 'NUM', 'PPOBJMS', 'PPOBJFS', 'VPPMS', 'VPPMP', 'VPPFS', 'VPPFP', 'DET', 'DETMS',
                   'DETFS', 'ADJ', 'ADJMS', 'ADJMP', 'ADJFS', 'ADJFP', 'NOUN', 'NMS', 'NMP', 'NFS', 'NFP', 'CHIF', 'MOTINC', 'X']
        keyword = ''
        for tk in pos_val:
            if tk[0] in ['des', 'information', 'informations', 'sur']:
                pass
            else:
                if tk[1] in to_keep:
                    keyword += tk[0] + ' '

        # search in wikipedia
        results = wikipedia.search(keyword, results=10, suggestion=False)

        # Translate keywword to english
        keyword = GoogleTranslator(source='fr', target='en').translate(keyword)

        if len(results) == 0:
            dispatcher.utter_message(
                text=f"Désolé, Aucun résultat correspond à votre recherche")
            return [SlotSet('search_query', keyword)]

        wiki = wikipediaapi.Wikipedia('en')
        exists = False
        for i in range(len(results)):
            page = wiki.page(results[i])
            if page.exists() == True:
                exists = True
                break

        # Display the answer
        if exists == False:
            dispatcher.utter_message(
                text=f"Désolé, La page que vous cherchez n'existe pas")
            return [SlotSet('search_query', keyword)]
        else:
            response_list = page.summary.split('.')
            response = ''

            if len(response_list) >= 2:
                for sent in response_list[:2]:
                    response += sent+'.'
                response = clean(response)
                response = GoogleTranslator(
                    source='en', target='fr').translate(response)
                dispatcher.utter_message(text=f"{response}")
            else:
                response = response_list[0]+'.'
                response = clean(response)
                response = GoogleTranslator(
                    source='en', target='fr').translate(response)
                dispatcher.utter_message(text=f"{response}")
            return [SlotSet("search_query", keyword)]


class ActionBlenderBot(Action):
    def name(self) -> Text:
        return "action_blenderbot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        NEXT_UTTERANCE = tracker.get_slot('NEXT_UTTERANCE')
        historics = tracker.get_slot('historics')
        if NEXT_UTTERANCE == None:
            NEXT_UTTERANCE = ("")
        if historics == None:
            historics = []

        user_input = tracker.latest_message['text']
        user_input = GoogleTranslator(
            source='fr', target='en').translate(user_input)
        user_input = "<s> " + user_input + " </s> "

        historics.append(user_input)

        NEXT_UTTERANCE += user_input
        inputs = tokenizer([NEXT_UTTERANCE], return_tensors="pt")

        # Delete first historics elements if historics_tokens_number > 128(max_length)
        while len(inputs['attention_mask'][0]) > 128:
            NEXT_UTTERANCE = ("")
            historics = historics[1:]
            for h in historics:
                NEXT_UTTERANCE += h
            inputs = tokenizer([NEXT_UTTERANCE], return_tensors="pt")

        next_reply_ids = model.generate(**inputs)
        output = tokenizer.batch_decode(
            next_reply_ids, skip_special_tokens=True)[0]

        reply = GoogleTranslator(source='en', target='fr').translate(output)
        dispatcher.utter_message(text=f"{reply}")

        output = "<s> " + output + " </s> "
        NEXT_UTTERANCE += output

        historics.append(output)

        return [SlotSet('historics', historics), SlotSet('NEXT_UTTERANCE', NEXT_UTTERANCE)]


class ActionSearchYoutube(Action):
    def name(self) -> Text:
        return "action_search_youtube"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        search_query = tracker.get_slot('youtube_query')

        videosSearch = VideosSearch(search_query, limit=5)
        videosResult = await videosSearch.next()
        for res in videosResult.get("result"):
            dispatcher.utter_message(text=res.get("title"))
        return [SlotSet("youtubeResults", videosResult.get("result")), SlotSet("youtube_query", None), FollowupAction("utter_ask_video_index")]


class ActionOpenYoutube(Action):
    def name(self) -> Text:
        return "action_open_youtube"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        humanIndex = tracker.get_slot('index')
        # dispatcher.utter_message(text=f"{humanIndex}")
        if humanIndex is not None:
            index = humanIndex - 1
            youtube_results = tracker.get_slot("youtubeResults")
            if not index < len(youtube_results):
                dispatcher.utter_message(text="invalid")
                return []

            video_launcher = {
                "action": {
                    "type": "selenium.youtube.open",
                    "payload": {
                        "url": youtube_results[index].get("link")
                    }
                }
            }
            video_launcher = json.dumps(video_launcher)
            dispatcher.utter_message(text=video_launcher)
        else:
            return [FollowupAction("utter_ask_video_index")]
        return [SlotSet("index", None), FollowupAction("utter_video_displayed")]


class ActionCloseYoutube(Action):
    def name(self) -> Text:
        return "action_close_youtube"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        reply = {
            "action": {
                "type": "selenium.youtube.close"
            }
        }
        dispatcher.utter_message(text=json.dumps(reply))
        print('Close')
        return []


class ActionPlayPauseYoutube(Action):
    def name(self) -> Text:
        return "action_play_pause_youtube"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        reply = {
            "action": {
                "type": "selenium.youtube.playPause"
            }
        }
        print('Play Pause')
        dispatcher.utter_message(text=json.dumps(reply))
        return []


class ActionSkipForwardYoutube(Action):
    def name(self) -> Text:
        return "action_skip_forward_youtube"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        reply = {
            "action": {
                "type": "selenium.youtube.skipForward"
            }
        }
        dispatcher.utter_message(text=json.dumps(reply))
        return []


class ActionSkipBackwardYoutube(Action):
    def name(self) -> Text:
        return "action_skip_backward_youtube"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        reply = {
            "action": {
                "type": "selenium.youtube.skipBackward"
            }
        }
        dispatcher.utter_message(text=json.dumps(reply))
        return []


class ActionPrevVideoYoutube(Action):
    def name(self) -> Text:
        return "action_prev_video_youtube"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        reply = {
            "action": {
                "type": "selenium.youtube.prevVideo"
            }
        }
        dispatcher.utter_message(text=json.dumps(reply))
        return []


class ActionNextVideoYoutube(Action):
    def name(self) -> Text:
        return "action_next_video_youtube"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        reply = {
            "action": {
                "type": "selenium.youtube.nextVideo"
            }
        }
        dispatcher.utter_message(text=json.dumps(reply))
        return []
