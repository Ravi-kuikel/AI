# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import zomato
import re
#
class mama(Action):
#
    def name(self) -> Text:
        return "action_find"
#
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            lo=tracker.get_slot('location')
            cu=tracker.get_slot('cuisine')
            restaurant=zomato.search(lo,cu)
            if restaurant==1:
                txt = "CUISINE NOT FOUND!PLEASE SELECT A DIFFERENT CUISINE"
            elif restaurant==0 or restaurant==2:
                txt="PLEASE SELECT A DIFFERENT LOCATION"

            else:
                txt = ""
                name = "AVAILABLE RESTAURANTS:\n"
                address = "ADDRESS:\n"
                websites = "WEBSITES:\n"
                count = 1
                for i in restaurant:
                    name=name+str(count)+'-'+i[0]+'\n'
                    address=address+str(count)+'-'+i[2]+'\n'
                    x = re.search('\?', i[1])
                    pos=x.start()
                    websites=websites+str(count)+'-'+(i[1])[:pos]+'\n'
                    count=count+1
                txt=name+address+websites


            dispatcher.utter_message(text=txt)

            return []
