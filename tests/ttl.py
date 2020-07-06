import time
from ttlcollections import TTLQueue, TTLHeap, TTLStack
from termcolor import cprint


def test_queue(queue: TTLQueue) -> bool:
    """Tests the TTLQueue class"""

    for x in range(queue.qsize - 1):
        queue.put(x)
    time.sleep(queue.ttl)
    1 in queue
    if queue:
        cprint("Error: Queue not empty after sleep", "red")
        return False
    queue.put(1, ttl=5)
    time.sleep(5)
    1 in queue   # This triggers the expire function
    if queue:
        cprint("Error: Queue not empty after custom TTL sleep", "red")
        return False
    cprint("Queue test passed", "green")
    return True


def test_heap(heap: TTLHeap) -> bool:
    """Tests the TTLHeap class"""

    for x in range(heap.qsize - 1):
        heap.put(x)
    time.sleep(heap.ttl)
    1 in heap
    if heap:
        cprint("Error: Heap not empty after sleep", "red")
        return False
    heap.put(1, ttl=5)
    time.sleep(5)
    1 in heap   # This triggers the expire function
    if heap:
        cprint("Error: Heap not empty after custom TTL sleep", "red")
        return False
    cprint("Heap test passed", "green")
    return True


def test_stack(stack: TTLStack) -> bool:
    """Tests the TTLStack class"""

    for x in range(stack.size - 1):
        stack.push(x)
    time.sleep(stack.ttl)
    1 in stack
    if stack:
        cprint("Error: Stack not empty after sleep", "red")
        return False
    stack.push(1, ttl=5)
    time.sleep(5)
    1 in stack   # This triggers the expire function
    if stack:
        cprint("Error: Stack not empty after custom TTL sleep", "red")
        return False
    cprint("Stack test passed", "green")
    return True


def main():
    """Test entry point"""

    start = time.monotonic()
    results = {}
    results["stack"] = test_stack(TTLStack(10, 10))
    results["queue"] = test_queue(TTLQueue(10, 10))
    results["heap"] = test_heap(TTLHeap(10, 10))
    end = time.monotonic()
    values = results.values()
    took = round(end - start, 2)
    if not all(values):
        failed = list(values).count(False)
        cprint(f"{failed} tests failed, {len(values) - failed} passed in {took} seconds", "red")
    else:
        cprint(f"0 tests failed, {len(values)} passed in {took} seconds", "green")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("Operation cancelled by user", "red")
