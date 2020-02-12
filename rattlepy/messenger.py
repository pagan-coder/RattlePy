class Messenger(object):

	# Performance optimization
	EmptyList = []

	def __init__(self):
		self.Subscribers = {}

	def subscribe(self, message_name, subscriber):
		"""
		Adds a subscriber to process the given message.
		:param message_name: message the subscriber wants to subscribe to
		:param subscriber: callable subscriber
		:return:
		"""
		if message_name not in self.Subscribers:
			self.Subscribers[message_name] = set()
		self.Subscribers[message_name].add(subscriber)

	async def publish(self, message_name, message=None):
		"""
		Publish message to specific subscribers asynchronously.
		:param message_name: the name of the message the specific subscribers are subscribed to
		:param message: body of the message to be passed to the subscriber
		:return: number of notified subscribers
		"""

		subscribers = self.Subscribers.get(message_name, self.EmptyList)
		for subscriber in subscribers:
			await subscriber(message_name, message)

		return len(subscribers)
