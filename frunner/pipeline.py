
__all__ = ['pipeline']
import asyncio
from .task_tui import start_tui
import frunner as fr
from asyncio.subprocess import PIPE
from frunner import State
from collections import deque


def init_tasks(tasks):
    # build the importance graph
    def walk_task(task):
        task.importance += 1
        for tt in task.prereqs:
            walk_task(tt)
    for t in tasks:
        walk_task(t)

async def start_all(pipeline, tui):
    futures = [pipeline.start_async(), tui.start_async()]
    done, __ = await asyncio.wait(futures, return_when=asyncio.FIRST_COMPLETED)
    return done.pop().result()

class TaskResult:
    def __init__(self, task, stdout=None, stderr=None, retcode=None):
        self.task = task
        self.stdout = stdout
        self.stderr = stderr
        self.retcode = retcode
    
    def __str__(self):
        return (f"[{self.task.name}] retcode={self.retcode}")

async def run_task(task, pipeline):
    pipeline.info(f'[{task.name}] Executing...')
    task.state = State.RUNNING
    proc = await asyncio.create_subprocess_exec(*task.args,
            stdout=PIPE, stderr=PIPE, cwd=task.cwd)
    stdout, stderr = await asyncio.gather(
            read_stream(proc.stdout, print),
            read_stream(proc.stderr, print))
    retcode = await proc.wait()
    task.state = State.COMPLETED if retcode == 0 else State.FAILED
    task.result = TaskResult(task, stdout=stdout, stderr=stderr, retcode=retcode)
    pipeline.info(f'[{task.name}] Returned: {task.state}. stdout #={len(stdout)} retcode={retcode}')
    return task


async def read_stream(stream, display):
    output = []
    while True:
        line = await stream.readline()
        if not line:
            break
        output.append(line)
    return output

def get_ready_queue(tasks, info):
    ready_queue = []
    for task in tasks:
        if task.state in (State.COMPLETED, State.FAILED):
            continue
        if task.state  == State.PENDING:
            # check to see if we are okay to run
            if not task.prereqs:
                task.state = State.READY
            else:
                if all(t.state == State.COMPLETED for t in task.prereqs):
                    task.state = State.READY
                elif any(t.state == State.FAILED for t in task.prereqs):
                    task.state = State.FAILED
        if task.state == State.READY:
            ready_queue.append(task)
    # sort according to distance, reversed
    ready_queue = sorted(ready_queue, key=lambda x: x.get_distance())
    ready_queue = deque(ready_queue)
    return ready_queue

class Pipeline:
    def __init__(self):
        self.tasks = set()
        self.log = deque()
        self.success = None

    def add_task(self, name, *args):
        task = fr.TaskUnit(name, *args)
        if task in self.tasks:
            raise ValueError(f'"{name}" already exists.')
        self.tasks.add(task)
        return task
    
    def info(self, msg):
        self.log.append(msg)
        if len(self.log)>50:
            self.log.popleft()

    async def start_async(self, queue_len=3):
        init_tasks(self.tasks)
        ready_queue = get_ready_queue(self.tasks, self.info)
        nn = min(queue_len, len(ready_queue))
        futures = [run_task(ready_queue.popleft(),self) for i in range(nn)]

        while True:
            __, futures = await asyncio.wait(futures, return_when=asyncio.FIRST_COMPLETED)
            # since one is done, we can add one more the futures list if any is left
            ready_queue = get_ready_queue(self.tasks, self.info)
            if ready_queue:
                while ready_queue and len(futures) < queue_len:
                    futures.add(run_task(ready_queue.popleft(), self))
            if not ready_queue and not futures:
                break

    async def _start_async(self):
        self.n = 0
        while True:
            self.n += 1
            if self.n > 10:
                break
            await asyncio.sleep(0.5)
        return self

    def run(self):
        with start_tui(self) as tui:
            # complete both event loops
            result = asyncio.run(start_all(self, tui))
            z = [t for t in self.tasks if t.state != State.COMPLETED]
            self.success = not z
            if not self.success:
                self.info('Not all tasks completed: {len(z)}')
                for t in z:
                    self.info(f"{t.name}: {t.state}")
            self.info("Press q to exit...")
            result = asyncio.run(tui.start_async())
        # user canceled or pipeline finished?
        print(result)

def pipeline():
    return Pipeline()
