from collections import deque
from time import monotonic
from types import FunctionType
from math import inf
from .errors import QueueEmpty, QueueFull, StackEmpty, StackFull
from heapq import heappush, heappop
from .objects import TTLItem


class TTLQueue:

    """A queue (FIFO) with per-item time to live (TTL)

       When a TTL expires, its associated element will be deleted, but please
       note that TTL expiration (and therefore, items deletion) is performed
       only when doing mutating operations (e.g. put and get)
       on the queue itself and when performing operations using the 'in' operator

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

        self.qsize = qsize if qsize else inf  # Infinite size
        self.ttl = ttl
        if self.ttl < 0:
            raise ValueError("ttl can't be negative!")
        if self.qsize < 0:
            raise ValueError("qsize can't be negative!")
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
        while i < n:   # Not the nicest-looking way of doing it, but surely works and is efficient
            item = self._queue[i]
            if item.date <= when:
                self._queue.remove(item)
                n = len(self._queue)
                i -= 1
            i += 1

    def put(self, element, ttl: int = 0):
        """Puts an item onto the queue

           :param element: The element to put in the queue
           :type element: object
           :param ttl: If you want to override the default ttl
            of the class for a specific element, you can specify
            that, defaults to 0 (use self.ttl)
           :param ttl: int, optional
           :raises QueueFull: If the queue is full
        """

        self.expire(self.timer())
        ttl = ttl if ttl else self.ttl
        ttl += self.timer()
        if len(self._queue) < self.qsize:
            self._queue.append(TTLItem(element, ttl))
        else:
            raise QueueFull("The queue is full!")

    def get(self):
        """Gets an item from the queue, raising QueueEmpty if the
           queue is empty
        """

        self.expire(self.timer())
        if not self._queue:
            raise QueueEmpty("The queue is empty!")
        return self._queue.popleft().obj

    def __repr__(self):
        """Implements repr(self)"""

        string = "TTLQueue({list}, qsize={qsize}, ttl={ttl}, timer={timer})"
        values = [t.obj for t in self._queue]
        return string.format(list=values, qsize=self.qsize, ttl=self.ttl, timer=self.timer)

    def __iter__(self):
        """Implements iter(self)"""

        for item in self._queue:
            yield item.obj

    def __contains__(self, item):
        """Implements item in self"""

        self.expire(self.timer())
        return self._queue.__contains__(TTLItem(item, None))

    def __bool__(self):
        """Implement bool(self)"""

        return bool(self._queue)

    def __eq__(self, other: object):
        """Implements self == other"""

        queue = [item.obj for item in self._queue]
        return queue == other


class TTLStack:
    """A stack (LIFO) with per-item time to live (TTL)

       All items inside the stack will be associated to a TTL (time to live).
       When a TTL expires, its associated element will be deleted, but please
       note that TTL expiration (and therefore, items deletion) is performed
       only when doing mutating operations on the stack itself (e.g. push/pop)
       and when performing operations using the 'in' operator

       It is also possible to set a different TTL for every item and to
       define the maximum stack size

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
        self.size = size if size else inf
        if self.ttl < 0:
            raise ValueError("ttl can't be negative!")
        if self.size < 0:
            raise ValueError("size can't be negative!")
        self._stack = deque()

    def push(self, element, ttl: int = 0):
        """Pushes an item onto the stack

           :param element: The element to push
           :type element: object
           :param ttl: If you want to override the default ttl
            of the class for a specific element, you can specify
            that, defaults to 0 (use self.ttl)
           :param ttl: int, optional
           :raises StackFull: If the stack is full
        """

        self.expire(self.timer())
        ttl = ttl if ttl else self.ttl
        ttl += self.timer()
        if len(self._stack) < self.size:
            self._stack.appendleft(TTLItem(element, ttl))
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
        return self._stack.popleft().obj

    def __repr__(self):
        """Implements repr(self)"""

        string = "TTLStack({list}, size={qsize}, ttl={ttl}, timer={timer})"
        values = [t.obj for t in self._stack]
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
            item = self._stack[i]
            if item.date <= when:
                self._stack.remove(item)
                n = len(self._stack)
                i -= 1
            i += 1

    def __contains__(self, item):
        """Implements item in self"""

        self.expire(self.timer())
        return self._stack.__contains__(TTLItem(item, None))

    def __bool__(self):
        """Implement bool(self)"""

        return bool(self._stack)

    def __eq__(self, other: object):
        """Implements self == other"""

        stack = [item.obj for item in self._stack]
        return stack == other


class TTLHeap(TTLQueue):
    """A heap queue with per-item time to live (TTL)

       All items inside the queue will be associated to a TTL (time to live).
       When a TTL expires, its associated element will be deleted, but please
       note that TTL expiration (and therefore, items deletion) is performed
       only when doing mutating operations (put/get) on the queue itself and
       when performing operations using the 'in' operator.

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

        super().__init__(qsize, ttl, timer)
        self._queue = []

    def __iter__(self):
        """Implements iter(self)"""

        super().__iter__()

    def __repr__(self):
        """Implements repr(self)"""

        string = "TTLHeap({list}, qsize={qsize}, ttl={ttl}, timer={timer})"
        values = [t.obj for t in self._queue]
        return string.format(list=values, qsize=self.qsize, ttl=self.ttl, timer=self.timer)

    def __contains__(self, item):
        """Implements item in self"""

        super().__contains__(item)

    def put(self, element, ttl: int = 0):
        """Puts an item onto the queue

           :param element: The element to put in the queue
           :type element: object
           :param ttl: If you want to override the default ttl
            of the class for a specific element, you can specify
            that, defaults to 0 (use self.ttl)
           :param ttl: int, optional
           :raises QueueFull: If the queue is full
        """

        self.expire(self.timer())
        ttl = ttl if ttl else self.ttl
        ttl += self.timer()
        if len(self._queue) < self.qsize:
            heappush(self._queue, TTLItem(element, ttl))
        else:
            raise QueueFull("The queue is full!")

    def get(self):
        """Gets an item from the queue, raising QueueEmpty if the
           queue is empty
        """

        self.expire(self.timer())
        if not self._queue:
            raise QueueEmpty("The queue is empty!")
        return heappop(self._queue).obj


    def expire(self, when: int):
        """Pops expired element out of the queue if their TTL has
           expired by when units of time (usually seconds)

           :param when: The expiry date to check items against. Items' whose
            insertion date, according to self.timer, is less or equal
            than this number will be automatically deleted
           :type when: int
        """

        super().expire(when)

    def __bool__(self):
        """Implement bool(self)"""

        return super().__bool__()

    def __eq__(self, other: object):
        """Implements self == other"""

        return super().__eq__(other)
