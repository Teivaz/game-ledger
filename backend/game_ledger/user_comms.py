from game_ledger.config import cfg


class UserComms:
    def send_auth_email(self, ctx: "Context", email: str, token: str):
        base_url = cfg["base_url"]
        ctx.send_mail(
            to_email=email,
            from_email="Game Ledger System",
            subject="GameLedger Sign In Request",
            body=f'To sign in into the GameLedger please follow the link <a href="{base_url}/api/user/auth?token={token}">Sign In</a>',
        )

    def send_register_email(self, ctx: "Context", email: str, token: str):
        base_url = cfg["base_url"]
        ctx.send_mail(
            to_email=email,
            from_email="Game Ledger System",
            subject="GameLedger Sign Up Request",
            body=f'To proceed registering in GameLedger please follow the link <a href="{base_url}/api/user/auth?register&token={token}">Sign Up</a>'
        )
