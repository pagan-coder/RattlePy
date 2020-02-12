#!/usr/bin/env python3
import rattlepy

import aiohttp


class MyServerApplication(rattlepy.RattlePyApplication):
	"""
	An example custom application with a simple route added.
	"""

	def prepare_routes(self):
		# Include example routes from parent
		super().prepare_routes()
		# Add custom routes
		self.Routes.append(aiohttp.web.get("/v", self.version))

	async def version(self, request):
		return aiohttp.web.json_response({"v": 1})


if __name__ == '__main__':
	app = MyServerApplication()
	app.serve()
