from game_ledger.config import cfg
from game_ledger.context import Context


class UserComms:
    @staticmethod
    def send_auth_email(ctx: "Context", email: str, token: str):
        base_url = cfg["base_url"]
        ctx.send_mail(
            to_email=email,
            from_email=cfg["email"],
            from_name="Game Ledger System",
            subject="GameLedger Sign In Request",
            body_html=f'To sign in into the GameLedger please follow the link <a href="{base_url}/api/user/signin/?token={token}">Sign In</a>',
            body_text=f'To sign in into the GameLedger please enter the link in your browser\n{base_url}/api/user/signin/?token={token}\n',
        )

    @staticmethod
    def send_register_email(ctx: "Context", email: str, token: str):
        base_url = cfg["base_url"]
        ctx.send_mail(
            to_email=email,
            from_email=cfg["email"],
            from_name="Game Ledger System",
            subject="GameLedger Sign Up Request",
            body_html=f'To proceed registering in GameLedger please follow the link <a href="{base_url}/api/user/register/&token={token}">Sign Up</a>',
            body_text=f'To proceed registering in GameLedger please enter the link in your browser\n{base_url}/api/user/register/&token={token}\n',
        )
