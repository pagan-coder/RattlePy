import abc
import asyncio

import aiohttp
import aiohttp.web

from .messenger import Messenger
from .executor import Executor


class RattlePyApplication(object):
	"""
	The main application object that prepares the server application
	together with an asynchronous loop. It utilizes Messenger and Executor.
	"""

	def __init__(self):
		# At the beginning, there is no async loop running
		self.Loop = None
		self.WebApplication = None
		self.Routes = []

		# Publish-subscribe mechanism
		self.Messenger = Messenger()

		# Executor to perform long synchronous tasks on threads
		self.Executor = None

	def serve(self):
		# Create new event loop
		self.Loop = asyncio.get_event_loop()
		if self.Loop.is_closed():
			self.Loop = asyncio.new_event_loop()
			asyncio.set_event_loop(self.Loop)

		# Prepare the executor
		self.Executor = Executor(loop=self.Loop)

		# Prepare aiohttp application
		self.WebApplication = aiohttp.web.Application(loop=self.Loop)
		self.prepare_routes()
		self.WebApplication.add_routes(self.Routes)
		aiohttp.web.run_app(self.WebApplication)

	@abc.abstractmethod
	def prepare_routes(self):
		"""
		This method is meant to be overriden by your specific implementation.
		Example of an added route:
		self.Routes.append(aiohttp.web.get("/hello-world/{name}", self.hello_world))
		:return:
		"""
		pass
