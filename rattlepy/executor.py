import concurrent
import concurrent.futures


class Executor(object):
	"""
	Executes synchronous tasks on threads, that are connected
	to a provided asynchronous loop.
	"""

	def __init__(self, loop):
		self.Loop = loop
		self.ThreadExecutor = concurrent.futures.ThreadPoolExecutor(
			thread_name_prefix="RattlePyThread"
		)

	def execute(self, func, *args):
		return self.Loop.run_in_executor(
			self.ThreadExecutor,
			func,
			*args
		)
