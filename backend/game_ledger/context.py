from game_ledger.token_controller import TokenController
from game_ledger.user_comms import UserComms
from psycopg2 import connection

class Context:
	def __init__(self):
		self.conn: connection
		self.token_controller = TokenController()
		self.user_comms = UserComms()
