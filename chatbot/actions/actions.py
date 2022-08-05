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


class ResetCreateForm(Action):

    def name(self) -> Text:
        return "action_reset_create"

    def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("summary", None), SlotSet("start", None), SlotSet("end", None), SlotSet("description", None)]


class ActionEventsToday(Action):

    def name(self) -> Text:
        return "action_get_events_today"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Here are the events you have for the next 24 hours")
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
        return [SlotSet("event", newEvent)]


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


class ValidateRestaurantForm(FormValidationAction):
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

    
