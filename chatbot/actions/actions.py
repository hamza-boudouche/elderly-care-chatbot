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

from deep_translator import GoogleTranslator
import nltk
import wikipedia
import wikipediaapi


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
        dispatcher.utter_message(
            text=f"Création d'un nouveau evenement ...")
        summary = tracker.get_slot('summary')
        start = tracker.get_slot('start')
        end = tracker.get_slot('end')
        description = tracker.get_slot('description')
        messages, newEvent = await actionAddEvent(summary, description, start, end)
        for message in messages:
            dispatcher.utter_message(text=message.get("text"))
        return [SlotSet("event", newEvent), SlotSet("summary", None), SlotSet("start", None), SlotSet("end", None), SlotSet("description", None)]


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

        # translate user question to english :
        text = tracker.latest_message['text']
        translated_text = GoogleTranslator(source='fr', target='en').translate(text)

        # POS tagging :
        preprocessed_text = nltk.word_tokenize(translated_text.lower())
        pos_val = nltk.pos_tag(preprocessed_text, tagset='universal')

        # delete indesirable words and construct the keyword
        to_delete = ['ADV', 'CONJ', 'PRT', 'PRON','VERB', '.',  'X']
        key_word = ''
        for tk in pos_val:
            if tk[1] not in to_delete:
                key_word += tk[0] + ' '

        # search in wikipedia
        results = wikipedia.search(key_word, results=10, suggestion=False)
        if len(results) == 0:
            dispatcher.utter_message(text=f"Désolé, Aucun résultat correspond à votre recherche")
            return []
        
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
            return []
        else:
            reponse = page.summary.split('\n')[0]
            translated_reponse = GoogleTranslator(source='en', target='fr').translate(reponse)
            dispatcher.utter_message(text=f"{translated_reponse}")
            return []


    
