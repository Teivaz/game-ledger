from game_ledger.token_controller import TokenController
from game_ledger.config import cfg
from psycopg2 import connect
import http.client, json, urllib.parse
from werkzeug.exceptions import InternalServerError

class Context:
    def __init__(self):
        self.conn = connect(
            host=cfg["postgres_host"],
            port=int(cfg["postgres_port"]),
            dbname=cfg["postgres_db"],
            user=cfg["postgres_user"],
            password=cfg["postgres_password"],
        )
        self.token_controller = TokenController()

        self._start_db()

    def _start_db(self):
        # First check if tables exist and create if not
        pass

    def send_mail(self, to_email: str, from_email: str, from_name: str, subject: str, body_text: str, body_html: str):
        conn = http.client.HTTPSConnection("api.elasticemail.com")
        payload = {
            "apikey": cfg["elasticemail_api_key"],
            "subject": subject,
            "from": from_email,
            "fromName": from_name,
            "to": to_email,
            "bodyHtml": body_html,
            "bodyText": body_text,
            "isTransactional": True
        }
        conn.request("POST", "/v2/email/send/?" + urllib.parse.urlencode(payload))
        res = conn.getresponse()
        data = res.read()
        response_obj = json.loads(data.decode("utf-8"))
        if not response_obj["success"]:
            raise InternalServerError()

