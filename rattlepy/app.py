import logging
import asyncio

import aiohttp
import aiohttp.web

from .messenger import Messenger
from .executor import Executor


Log = logging.getLogger(__name__)


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

	def prepare_routes(self):
		"""
		This method is meant to be overriden by your specific implementation.
		:return:
		"""
		self.Routes.append(aiohttp.web.get("/hello-world/{name}", self.hello_world))
		self.Messenger.subscribe("hello-world", self.endpoint_called)

	async def hello_world(self, request):
		"""
		An example coroutine that handles the route "hello-world" registered
		in self.prepare_routes method.
		:param request: request
		:return: response
		"""
		# Obtain the parameter from the request
		name = request.match_info["name"]

		# Publish message notifying all relevant subscribers that the endpoint was called
		await self.Messenger.publish("hello-world", name)

		# Perform long running synchronous operations on threads and thus make them asynchronous
		processed_name = await self.Executor.execute(self.hello_world_synchronous, name)

		# Return text response
		return aiohttp.web.Response(
			text="Hello, {}!".format(processed_name)
		)

	def hello_world_synchronous(self, name):
		"""
		Long-running synchronous task that should be performed on thread,
		so the asynchronous server is not blocked.
		:param name: name obtained from the query
		:return: processed name
		"""
		processed_name = name.upper()
		processed_name = processed_name.replace("A", "AaA")
		processed_name = processed_name.replace("E", "EnE")
		processed_name = processed_name.replace("I", "IllI")
		processed_name = processed_name.replace("O", "OuO")
		processed_name = processed_name.replace("U", "UxxxU")
		return processed_name

	async def endpoint_called(self, message_name, message):
		"""
		An example of specific subsriber that logs every message it obtains.
		:param message_name: type of the message the subscriber is subscribed to
		:param message: the body of the message
		:return:
		"""
		Log.warning(
			"Endpoint '{}' was successfully called with obtained request data '{}'.".format(message_name, message)
		)
