import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict

from actions.utils import actionEventsToday
from actions.utils import actionEventsRange
from actions.utils import actionDeleteEvent
from actions.utils import actionAddEvent
from actions.utils import actionUpdateEvent
from actions.utils import actionAdditionalInfo

from deep_translator import GoogleTranslator
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration, BlenderbotConfig
import nltk
import wikipedia
import wikipediaapi

# BlenderBot model
mname = "./blenderbot-400M-distill"
model = BlenderbotForConditionalGeneration.from_pretrained(
    mname, local_files_only=True)
tokenizer = BlenderbotTokenizer.from_pretrained(mname, local_files_only=True)


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
        dispatcher.utter_message(text=f"Création d'un nouveau evenement ...")
        summary = tracker.get_slot('summary')
        start = tracker.get_slot('start')
        end = tracker.get_slot('end')
        description = tracker.get_slot('description')
        messages, newEvent = await actionAddEvent(summary, description, start, end)
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
        translated_text = GoogleTranslator(
            source='fr', target='en').translate(text)

        # POS tagging :
        preprocessed_text = nltk.word_tokenize(translated_text.lower())
        pos_val = nltk.pos_tag(preprocessed_text, tagset='universal')

        # delete indesirable words and construct the keyword
        to_delete = ['ADV', 'CONJ', 'PRT', 'PRON', 'VERB', '.',  'X']
        key_word = ''
        for tk in pos_val:
            if tk[0] in ['information', 'informations', 'about', 'wich']:
                pass
            else:
                if tk[1] not in to_delete:
                    key_word += tk[0] + ' '

        # search in wikipedia
        results = wikipedia.search(key_word, results=10, suggestion=False)
        if len(results) == 0:
            dispatcher.utter_message(text=f"Désolé, Aucun résultat correspond à votre recherche")
            return [SlotSet('search_query',key_word)]
        wiki = wikipediaapi.Wikipedia('en')
        exists = False
        for i in range(len(results)):
            page = wiki.page(results[i])
            if page.exists() == True:
                exists = True
                break

        # Display the answer
        if exists == False:
            dispatcher.utter_message(text=f"Désolé, La page que vous cherchez n'existe pas")
            return [SlotSet('search_query',key_word)]
        else:
            response_list = page.summary.split('.')
            response = ''

            if len(response_list) >= 2:
                for sent in response_list[:2]:
                    response += sent+'.'
                response = clean(response)
                translated_response = GoogleTranslator(
                    source='en', target='fr').translate(response)
                dispatcher.utter_message(text=f"{translated_response}")
            else:
                response = response_list[0]+'.'
                response = clean(response)
                translated_response = GoogleTranslator(
                    source='en', target='fr').translate(response)
                dispatcher.utter_message(text=f"{translated_response}")
            return [SlotSet("search_query", key_word)]


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


class ActionOpenYoutube(Action):
    def name(self) -> Text:
        return "action_open_youtube"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url = tracker.get_slot('url')
        dispatcher.utter_message(json_message={
            "action": {
                "type": "selenium.youtube.open",
                "payload": {
                    "url": url
                }
            }
        })
        return [SlotSet("url", None)]


class ActionCloseYoutube(Action):
    def name(self) -> Text:
        return "action_close_youtube"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(json_message={
            "action": {
                "type": "selenium.youtube.close"
            }
        })
        return []


class ActionPlayPauseYoutube(Action):
    def name(self) -> Text:
        return "action_play_pause_youtube"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(json_message={
            "action": {
                "type": "selenium.youtube.playPause"
            }
        })
        return []


class ActionSkipForwardYoutube(Action):
    def name(self) -> Text:
        return "action_skip_forward_youtube"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(json_message={
            "action": {
                "type": "selenium.youtube.skipForward"
            }
        })
        return []


class ActionSkipBackwardYoutube(Action):
    def name(self) -> Text:
        return "action_skip_backward_youtube"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(json_message={
            "action": {
                "type": "selenium.youtube.skipBackward"
            }
        })
        return []


class ActionPrevVideoYoutube(Action):
    def name(self) -> Text:
        return "action_prev_video_youtube"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(json_message={
            "action": {
                "type": "selenium.youtube.prevVideo"
            }
        })
        return []


class ActionNextVideoYoutube(Action):
    def name(self) -> Text:
        return "action_next_video_youtube"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(json_message={
            "action": {
                "type": "selenium.youtube.nextVideo"
            }
        })
        return []
