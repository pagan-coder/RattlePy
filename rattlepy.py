import asyncio


class RattlePyApplication(object):

	def __init__(self):
		# At the beginning, there is no async loop running
		self.Loop = None

	def serve(self):
		# Create new event loop
		self.Loop = asyncio.get_event_loop()
		if self.Loop.is_closed():
			self.Loop = asyncio.new_event_loop()
			asyncio.set_event_loop(self.Loop)
