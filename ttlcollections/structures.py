from collections import deque
from time import monotonic
from types import FunctionType
import math
from .errors import QueueEmpty, QueueFull, StackEmpty, StackFull


class TTLQueue:

    """A FIFO data structure with per-item time to live (TTL)
       All items will have a default time to live, after that has
       expired (on the next mutating operation a.k.a put or get)
       expired elements will be popped out automatically.
       It is also possible to set a different TTL for every item and to
       define the maximum queue size

       Note: This queue is NOT thread safe and must be properly locked
       when used with multiple threads

       :param qsize: The max size of the queue, defaults to 0 (no limit)
       :type qsize: int, optional
       :param ttl: The TTL for every item in the queue, defaults to 0 (no TTL)
       :type ttl: int, optional
       :param timer: The timer function that the queue will use to
        keep track of elapsed time. Defaults to time.monotonic(), but can
        be customized. Any function that yields an incremental value
        on each subsequent call is acceptable, but its return values
        should not be repeated during runtime to avoid nonsense results
       :type timer: class: FunctionType, optional
    """

    def __init__(self, qsize: int = 0, ttl: int = 0, timer: FunctionType = monotonic):
        """Object constructor"""

        self.qsize = qsize if qsize else math.inf  # Infinite size
        self.ttl = ttl
        self.timer = timer
        self._queue = deque()

    def expire(self, when: int):
        """Pops expired element out of the queue if their TTL has
           expired by when units of time (usually seconds)

           :param when: The expiry date to check items against. Items' whose
            insertion date, according to self.timer, is less or equal
            than this number will be automatically deleted
           :type when: int
        """

        i = 0
        n = len(self._queue)
        while i < n:
            try:
                date, element = self._queue[i]
            except IndexError:
                break
            if date <= when:
                del self._queue[i]
            i += 1

    def put(self, element, ttl: int = 0):
        """Puts an item onto the queue

           :param element: The element to put in the queue
           :type element: object
           :param ttl: If you want to override the default ttl
            of the class for a specific element, you can specify
            that, defaults to 0 (use the default TTL)
           :param ttl: int, optional
           :raises QueueFull: If the queue is full
        """

        ttl = ttl if ttl else self.ttl
        self.expire(self.timer())
        if len(self._queue) < self.qsize:
            self._queue.append((self.timer() + ttl, element))
        else:
            raise QueueFull("The queue is full!")

    def get(self):
        """Gets an item from the queue, raising QueueEmpty if the
           queue is empty
        """

        self.expire(self.timer())
        if not self._queue:
            raise QueueEmpty("The queue is empty!")
        return self._queue.popleft()[1]

    def __repr__(self):
        """Implements repr(self)"""

        string = "TTLQueue({list}, qsize={qsize}, ttl={ttl}, timer={timer})"
        values = [t[1] for t in self._queue]
        return string.format(list=values, qsize=self.qsize, ttl=self.ttl, timer=self.timer)

    def __iter__(self):
        """Implements iter(self)"""

        for _, element in self._queue:
            yield element


class TTLStack:
    """A stack-like (LIFO) data structure with per-item time to live (TTL)
       All items will have a default time to live, after that has
       expired (on the next mutating operation a.k.a push or pop)
       expired elements will be popped out automatically.
       It is also possible to set a different TTL for every item and to
       define the maximum stack

       Note: This stack is NOT thread safe and must be properly locked
       when used with multiple threads

       :param size: The max size of the stack, defaults to 0 (no limit)
       :type size: int, optional
       :param ttl: The TTL for every item in the stack, defaults to 0 (no TTL)
       :type ttl: int, optional
       :param timer: The timer function that the stack will use to
        keep track of elapsed time. Defaults to time.monotonic(), but can
        be customized. Any function that yields an incremental value
        on each subsequent call is acceptable, but its return values
        should not be repeated during runtime to avoid nonsense results
       :type timer: class: FunctionType, optional
    """

    def __init__(self, size: int = 0, ttl: int = 0, timer: FunctionType = monotonic):
        """Object constructor"""

        self.timer = timer
        self.ttl = ttl
        self.size = size
        self._stack = deque()

    def push(self, element, ttl: int = 0):
        """Pushes an item onto the stack

           :param element: The element to push
           :type element: object
           :param ttl: If you want to override the default ttl
            of the class for a specific element, you can specify
            that, defaults to 0 (use the default TTL)
           :param ttl: int, optional
           :raises StackFull: If the stack is full
        """

        ttl = ttl if ttl else self.ttl
        self.expire(self.timer())
        if len(self._stack) < self.size:
            self._stack.appendleft((self.timer() + ttl, element))
        else:
            raise StackFull("The stack is full!")

    def pop(self):
        """Pops an item from the stack, raising StackEmpty if the
           stack is empty

           :raises StackEmpty: If the stack is empty
        """

        self.expire(self.timer())
        if not self._stack:
            raise StackEmpty("The stack is empty!")
        return self._stack.popleft()[1]

    def __repr__(self):
        """Implements repr(self)"""

        string = "TTLStack({list}, size={qsize}, ttl={ttl}, timer={timer})"
        values = [t[1] for t in self._stack]
        return string.format(list=values, qsize=self.size, ttl=self.ttl, timer=self.timer)

    def expire(self, when: int):
        """Pops expired element out of the stack if their TTL has
           expired by when units of time (usually seconds)

           :param when: The expiry date to check items against. Items' whose
            insertion date, according to self.timer, is less or equal
            than this number will be automatically deleted
           :type when: int
        """

        i = 0
        n = len(self._stack)
        while i < n:
            try:
                date, element = self._stack[i]
            except IndexError:
                break
            if date <= when:
                del self._stack[i]
            i += 1
