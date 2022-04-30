from station_admin.models.parking_session import ParkingSession
from station_admin.models.rent_session import RentSession
from station_admin.repository import renting_session_repository
from station_admin.repository.parking_session_repository import ParkingSessionRepository
from station_admin.service import sms_notifier
from django.core.management.base import BaseCommand, CommandError

MINUTES_UNTIL_NOTIFICATION = 30


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        parking_sessions: list[ParkingSession] = ParkingSessionRepository.find_all_active_sessions()
        rent_sessions: list[RentSession] = renting_session_repository.find_all_active_sessions()

        for session in parking_sessions:
            if self._session_is_near_end(session):
                phone_number = session.user.userprofile.phone_number
                print(f"Sending sms to: {phone_number}")
                sms_notifier.notify_user(phone_number)

        for session in rent_sessions:
            if self._session_is_near_end(session):
                phone_number = session.user.userprofile.phone_number
                print(f"Sending sms to: {phone_number}")
                sms_notifier.notify_user(phone_number)

    def _session_is_near_end(self, session: ParkingSession | RentSession) -> bool:
        return session.charge_rule.max_time_mins \
               and session.charge_rule.max_time_mins <= session.get_elapsed_seconds() / 60 + MINUTES_UNTIL_NOTIFICATION
