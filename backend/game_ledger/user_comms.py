URL = "gameledger.app"


class UserComms:
    def send_auth_email(self, email: str, token: str):
        topic = "GameLedger Sign In Request"
        text = f'To sign in into the GameLedger please follow the link <a href="{URL}/api/user/auth?token={token}">Sign In</a>'
        print(f"email to: {email}\n Topic: {topic}\n {text}")
        # TODO: email text and topic to the provided address

    def send_register_email(self, email: str, token: str):
        topic = "GameLedger Register Request"
        text = f'To proceed registering in GameLedger please follow the link <a href="{URL}/api/user/auth?register&token={token}">Sign In</a>'
        print(f"email to: {email}\n Topic: {topic}\n {text}")
        # TODO: email text and topic to the provided address
