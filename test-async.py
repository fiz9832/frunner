"""Parallel task dispatching service using asyncio.
"""
import asyncio
from asyncio.subprocess import PIPE
import sys
from collections import deque
import colorama as cr

class task:
    def __init__(self, name, *args):
        self.name = name
        self.args = args
        self.result = None



tasks = [task('T'+str(i), 'sleep',str(i)) for i in range(1, 4)]
tasks.append(task('AA', 'python', 'test_task.py'))
asyncio.run(run_tasks(tasks))

