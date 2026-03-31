import threading
import queue
import time


def worker(w, t):
    print(w)


WAIT = 1 / 1000 # iters per second


def main():
    ts = [threading.Thread(target=worker, args=(f"Thread {i}", i)) for i in range(0, 100)]

    while ts:
        for t in ts:
            if t.ident is None:
                t.start()

            if not t.is_alive():
                ts.remove(t)

        time.sleep(WAIT)


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(end - start)
