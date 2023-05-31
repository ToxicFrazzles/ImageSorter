import asyncio

from .message_context import MessageContext


def receive_handler(op_code):
    class Dec:
        def __init__(self, fn):
            self.fn = fn
            self.owner = None

        def __call__(self, fn):
            def wrapper(instance: 'Module', ctx: MessageContext):
                return fn(instance, ctx)
            return wrapper

        def __set_name__(self, owner: 'Module', name):
            def wrapper(instance: 'Module', ctx: MessageContext):
                return self.fn(instance, ctx)
            if "_handlers" not in owner.__dict__:
                owner._handlers = {}
            if op_code not in owner._handlers:
                owner._handlers[op_code] = []
            owner._handlers[op_code].append(wrapper)
            # print(owner)
            setattr(owner, name, wrapper)
    return Dec


class Module:
    _handlers = {}

    async def dispatch(self, msg: MessageContext):
        if msg.op_code not in self._handlers or len(self._handlers[msg.op_code]) == 0:
            return False
        for handler in self._handlers[msg.op_code]:
            asyncio.create_task(handler(self, msg))
        return True
