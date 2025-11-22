import time

def test():
    for i in range(1000000):
        print(i**2)

c_time = time.monotonic()
test()
print(time.monotonic() - c_time)