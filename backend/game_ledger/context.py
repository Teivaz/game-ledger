from game_ledger.token_controller import TokenController
from game_ledger.user_comms import UserComms
from psycopg2 import connect


class Context:
    def __init__(self):
        self.conn = connect(
            dbname="game-ledger",
            user="admin",
            password="admin",
            host="localhost",
            port=5432,
        )
        self.token_controller = TokenController()
        self.user_comms = UserComms()

        self._start_db()

    def _start_db(self):
        # First check if tables exist and create if not
        pass

    def send_mail(self, to_email: str, from_email: str, subject: str, body: str):
        # TODO: remove when emails work
        print(f"email: {body}")

