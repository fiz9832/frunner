from frunner import *
import asyncio

pipeline = pipeline()
t3 = pipeline.add_task("Task 3", 'python', 'test_task.py', '0')
t1 = pipeline.add_task("Task 1", 'sleep', '0.1')
t2 = pipeline.add_task("Task 2", 'sleep', '2')
t4 = pipeline.add_task("Task 4", 'sleep', '1')

for i in range(5, 35):
    tt = pipeline.add_task(f"Task {i}", 'sleep', '0.5')
    tt.requires(t2)

t0 = tt
for i in range(35, 55):
    tt = pipeline.add_task(f"Task {i}", 'sleep', '0.5')
    tt.requires(t2)
    t0 = tt

t3.requires(t2)
t4.requires(t3, tt)
t2.requires(t1)
# T1->T4,T2->T3
pipeline.run()
