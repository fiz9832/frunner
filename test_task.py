import sys
print('hello world from test_task')
import time
time.sleep(2)
for i in range(100000):
    print(f'hello {i}')
print('Done sleeping from test_task')
sys.exit(int(sys.argv[1]))
