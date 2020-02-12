import asyncio

import aiohttp
import aiohttp.web


class RattlePyApplication(object):

	def __init__(self):
		# At the beginning, there is no async loop running
		self.Loop = None
		self.WebApplication = None
		self.Routes = []

	def serve(self):
		# Create new event loop
		self.Loop = asyncio.get_event_loop()
		if self.Loop.is_closed():
			self.Loop = asyncio.new_event_loop()
			asyncio.set_event_loop(self.Loop)

		# Prepare aiohttp application
		self.WebApplication = aiohttp.web.Application(loop=self.Loop)
		self.prepare_routes()
		self.WebApplication.add_routes(self.Routes)
		aiohttp.web.run_app(self.WebApplication)

	def prepare_routes(self):
		"""
		This method is meant to be overriden by your specific implementation.
		:return: None
		"""
		self.Routes.append(aiohttp.web.get("/hello-world/{name}", self.hello_world))

	async def hello_world(self, request):
		"""
		An example coroutine that handles the route "hello-world" registered
		in self.prepare_routes method.
		:param request: request
		:return: response
		"""
		return aiohttp.web.Response(
			text="Hello, {}!".format(request.match_info.get("name", "world"))
		)
