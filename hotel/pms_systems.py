from abc import ABC, abstractmethod
import inspect
import sys

from typing import Optional

from hotel.external_api import (
    get_reservations_for_given_checkin_date,
    get_reservation_details,
    get_guest_details,
    APIError,
)

from hotel.models import Stay, Guest, Hotel


class PMS(ABC):
    """
    Abstract class for Property Management Systems.
    """

    def __init__(self):
        pass

    @property
    def name(self):
        longname = self.__class__.__name__
        return longname[4:]

    @abstractmethod
    def clean_webhook_payload(self, payload: str) -> dict:
        """
        Clean the json payload and return a usable object.
        Make sure the payload contains all the needed information to handle it properly
        """
        raise NotImplementedError

    @abstractmethod
    def handle_webhook(self, webhook_data: dict) -> bool:
        """
        This method is called when we receive a webhook from the PMS.
        Handle webhook handles the events and updates relevant models in the database.
        Requirements:
            - Now that the PMS has notified you about an update of a reservation, you need to
                get more details of this reservation. For this, you can use the mock API
                call get_reservation_details(reservation_id).
            - Handle the payload for the correct hotel.
            - Update or create a Stay.
            - Update or create Guest details.
        """
        raise NotImplementedError

    @abstractmethod
    def update_tomorrows_stays(self) -> bool:
        """
        This method is called every day at 00:00 to update the stays with a checkin date tomorrow.
        Requirements:
            - Get all stays checking in tomorrow by calling the mock API endpoint get_reservations_for_given_checkin_date.
            - Update or create the Stays.
            - Update or create Guest details. Deal with missing and incomplete data yourself
                as you see fit. Deal with the Language yourself. country != language.
        """
        raise NotImplementedError

    @abstractmethod
    def stay_has_breakfast(self, stay: Stay) -> Optional[bool]:
        """
        This method is called when we want to know if the stay includes breakfast.
        Notice that the breakfast data is not stored in any of the models, we always want real time data.
        - Return True if the stay includes breakfast, otherwise False. Return None if you don't know.
        """
        raise NotImplementedError


class PMS_Mews(PMS):
    def clean_webhook_payload(self, payload: str) -> dict:
        # TODO: Implement the method
        return {}

    def handle_webhook(self, webhook_data: dict) -> bool:
        # TODO: Implement the method
        return True

    def update_tomorrows_stays(self) -> bool:
        # TODO: Implement the method
        return True

    def stay_has_breakfast(self, stay: Stay) -> Optional[bool]:
        # TODO: Implement the method
        return None


def get_pms(name):
    fullname = "PMS_" + name.capitalize()
    # find all class names in this module
    # from https://stackoverflow.com/questions/1796180/
    current_module = sys.modules[__name__]
    clsnames = [x[0] for x in inspect.getmembers(current_module, inspect.isclass)]

    # if we have a PMS class for the given name, return an instance of it
    return getattr(current_module, fullname)() if fullname in clsnames else False
