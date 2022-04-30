from station_admin.models import ParkingSession, RentSession
from station_admin.repository import renting_session_repository
from station_admin.repository.parking_session_repository import ParkingSessionRepository


MINUTES_UNTIL_NOTIFICATION = 30

class SessionSmsCommand:

    def run(self) -> None:
        parking_sessions: list[ParkingSession] = ParkingSessionRepository.find_all_active_sessions()
        rent_sessions: list[RentSession] = renting_session_repository.find_all_active_sessions()

        for session in parking_sessions:
            if self._session_is_near_end(session):
                sm

    def _session_is_near_end(self, session: ParkingSession | RentSession) -> bool:
        return session.charge_rule.max_time_mins <= session.get_elapsed_seconds() / 60 + MINUTES_UNTIL_NOTIFICATION



if __name__ == '__main__':
    command = SessionSmsCommand()
    command.run()
