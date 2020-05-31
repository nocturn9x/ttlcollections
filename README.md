# ttlcollections - Pure python collections with Time-to-live

`ttlcollections` is a pure Python implementation of a various data structures with built-in TTL (time to live) functionality, using nothing but the standard library.


## Installation

To install the library from source simply clone this repository and run the command `python3 setup.py install`

## Usage

As of now `ttlcollections` implements 2 data structures: a queue and a stack.

The difference between a stack and a queue is that the former follows the LIFO (Last-in First-out) scheme, while the latter follows the FIFO (First-in First out) scheme.

These 2 collections are implemented using `collections.deque` for fast `O(1)` complexity when accessing elements trough `pop`/`get` and `push`/`put`


### Example - TTLQueue

```python
from ttlcollections import TTLQueue
import time

q = TTLQueue(ttl=60)   # Elements that are older than 60 seconds will be deleted
q.put(1)
time.sleep(60)
q.get()   # Will raise ttlcollections.errors.QueueEmpty because the TTL for 1 has expired

```

#### Methods

This is the methods documentation for TTLQueue in Sphinx format

##### `TTLQueue` - `__init__()`

A FIFO data structure with per-item time to live (TTL)
       All items will have a default time to live, after that has
       expired (on the next mutating operation a.k.a put or get)
       expired elements will be popped out automatically.
       It is also possible to set a different TTL for every item and to
       define the maximum queue size.
       __Note__: This queue is __NOT__ thread safe and must be properly locked
       when used with multiple threads


```
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
```

##### `TTLQueue` - `put()`

Pops expired element out of the queue if their TTL has expired by when units of time (usually seconds)

```
           :param when: The expiry date to check items against. Items' whose
            insertion date, according to self.timer, is less or equal
            than this number will be automatically deleted
           :type when: int
```

##### `TTLQueue` - `get()`
Puts an item onto the queue

```
           :param element: The element to put in the queue
           :type element: object
           :param ttl: If you want to override the default ttl
            of the class for a specific element, you can specify
            that, defaults to 0 (use the default TTL)
           :param ttl: int, optional
           :raises QueueFull: If the queue is full
```

##### `TTLQueue` - `expire()`
Pops expired element out of the queue if their TTL has expired by `when` units of time (usually seconds)

```
           :param when: The expiry date to check items against. Items' whose
            insertion date, according to self.timer, is less or equal
            than this number will be automatically deleted
           :type when: int


```


### Example - TTLStack

```python
from ttlcollections import TTLStack
import time

q = TTLStack(ttl=60)   # Elements that are older than 60 seconds will be deleted
q.push(1)
time.sleep(60)
q.pop()   # Will raise ttlcollections.errors.StackEmpty because the TTL for 1 has expired

```

#### Methods

This is the methods documentation for TTLStack in Sphinx format

##### `TTLStack` - `__init__()`

A stack-like (LIFO) data structure with per-item time to live (TTL).

All items will have a default time to live, after that has
expired (on the next mutating operation a.k.a push or pop)
elements will be popped out automatically.
It is also possible to set a different TTL for every item and to define the maximum stack size
       
**Note**: This stack is __NOT__ thread safe and must be properly locked when used with multiple threads
 
```
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
```

##### `TTLStack` - `push()`

Pushes an item onto the stack

```
:param element: The element to push
:type element: object
:param ttl: If you want to override the default ttl
of the class for a specific element, you can specify
that, defaults to 0 (use the default TTL)
:param ttl: int, optional
:raises StackFull: If the stack is full
```

##### `TTLStack` - `pop()`

Pops an item from the stack, raising StackEmpty if the stack is empty

```

:raises StackEmpty: If the stack is empty
```

##### `TTLStack` - `expire()`

Pops expired element out of the stack if their TTL has expired by `when` units of time (usually seconds)
```
:param when: The expiry date to check items against. 
 Items' whose insertion date, according to self.timer, is less or equal than this number
 will be automatically deleted
:type when: int
```

#### Notes

Please consider that the TTL expiration check is done at every mutating operation (e.g. `put` or `pop`) and that already expired elements may take space in memory until one of these methods is called.

You can force the TTL expiration check by calling the `expire` method. This method takes a single parameter and will delete all items in the collection that have expired the by the current time (according to the timer function) plus the specified amount of time units (usually seconds). For the current time you can use the collection's internal timer function (e.g. `TTLQueue.timer()`)

## Credits

Nocturn9x - Main developer

### Contacts for Nocturn9x

[Telegram](https://telegram.me/processare)

[Email](mailto:nocturn9x@intellivoid.net)


