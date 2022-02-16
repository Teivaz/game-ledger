from game_ledger.config import cfg
import http.client, json, urllib.parse
from werkzeug.exceptions import InternalServerError


def elasticmail_send_mail(
    to_email: str,
    from_email: str,
    from_name: str,
    subject: str,
    body_text: str,
    body_html: str,
):
    conn = http.client.HTTPSConnection("api.elasticemail.com")
    payload = {
        "apikey": cfg["elasticemail_api_key"],
        "subject": subject,
        "from": from_email,
        "fromName": from_name,
        "to": to_email,
        "bodyHtml": body_html,
        "bodyText": body_text,
        "isTransactional": True,
    }
    conn.request("POST", "/v2/email/send/?" + urllib.parse.urlencode(payload))
    res = conn.getresponse()
    data = res.read()
    response_obj = json.loads(data.decode("utf-8"))
    if not response_obj["success"]:
        raise InternalServerError()


send_mail = elasticmail_send_mail
