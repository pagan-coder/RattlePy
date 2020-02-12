#!/usr/bin/env python3
import rattlepy

import aiohttp

import logging

Log = logging.getLogger(__name__)


class MyServerApplication(rattlepy.RattlePyApplication):
	"""
	An example custom application with a simple routes added.
	"""

	def prepare_routes(self):
		"""
		Register custom routes.
		:return:
		"""
		self.Routes.append(aiohttp.web.get("/hello-world/{name}", self.hello_world))
		self.Messenger.subscribe("hello-world", self.endpoint_called)
		self.Routes.append(aiohttp.web.get("/v", self.version))

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

	async def version(self, request):
		"""
		A simple endpoint that returns JSON response.
		:param request: request
		:return: response
		"""
		return aiohttp.web.json_response({"v": 1})

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


if __name__ == '__main__':
	app = MyServerApplication()
	app.serve()
