# RattlePy

RattlePy is a simple asynchronous web server, that allows asynchronous processing
of incoming user requests, hence offers scalability in terms of memory and CPU time.

Long running synchronous tasks can be processed on threads and thus be connected to
the asynchronous loop using the Executor object.

Notification among coroutines can be obtained via publish-subscribe mechanism
in the Messenger object.

## Usage

	import rattlepy
	import aiohttp

	class MyServerApplication(rattlepy.RattlePyApplication):

		def prepare_routes(self):
			"""
			Register custom routes.
			:return:
			"""
			self.Routes.append(aiohttp.web.get("/v", self.version))

		async def version(self, request):
			"""
			A simple endpoint that returns JSON response.
			:param request: request
			:return: response
			"""
			return aiohttp.web.json_response({"v": 1})


	if __name__ == '__main__':
		app = MyServerApplication()
		app.serve()
