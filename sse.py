import queue


class MQSSE:
    def __init__(self):
        self.sse_queue = []

    def listen(self, id):
        msg_queue = queue.Queue(maxsize=10)
        self.sse_queue.append({'queue': msg_queue, 'id': id})
        return msg_queue

    def deploy(self, msg, id):
        for i in reversed(range(len(self.sse_queue))):
            try:
                if self.sse_queue[i]['id'] == id:
                    self.sse_queue[i]['queue'].put_nowait(msg)
            except queue.Full:
                del self.sse_queue[i]
