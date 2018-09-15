from blessed import Terminal
from contextlib import contextmanager
import time
import asyncio
import functools
from datetime import datetime
from .common import State

styles = {State.PENDING: ('○', lambda t, s: t.yellow(s)),
         State.READY: ('◉', lambda t, s: t.white(s)),
         State.COMPLETED: ('✓', lambda t, s: t.cyan(s)),
         State.RUNNING: ('►', lambda t, s: t.white_on_blue(s)),
         State.FAILED: ('✕', lambda t, s: t.white_on_red(s))}

echo = functools.partial(print, end='', flush=True)
class TaskTUI():
    def __init__(self, term, pipeline):
        self.term = term
        self.pipeline = pipeline


    def echo_yx(self, y, x, text):
        echo(self.term.move(y, x))
        echo(text)

    def vline(self, x, c='│', y_start=0):
        h = self.term.height
        for y in range(y_start, h):
            self.echo_yx(y, x, c)

    def redraw(self):
        self.task_list = sorted(self.pipeline.tasks, key=lambda x: x.get_distance())
        term = self.term
        echo(term.clear())
        h, w = term.height, term.width
        now_str = datetime.now().strftime("%Y-%M-%d %H:%M:%S")
        bg = term.yellow_reverse
        if self.pipeline.success == False:
            bg = term.red_reverse
        if self.pipeline.success:
            bg = term.cyan_reverse
        self.echo_yx(0,0, bg(' '.ljust(w)))
        self.echo_yx(0,0, bg(now_str))

        lwidth = 15 
        y, x = 2, 2
        for task in self.task_list:
            label = task.name[0:lwidth].ljust(lwidth)
            s, fun, *__ = styles[task.state] #str(task.state)[0]
            label = f"┃{s} {label}"
            if fun is not None:
                label = fun(term, label)
            self.echo_yx(y, x, label)
            y += 1
            if y > h-2:
                y = 2
                x += lwidth+5
         
        y, x = 2, x + (lwidth+7)#int(w*0.5)
        #self.vline(x, term.blue_reverse(' '))
        nn = h - y - 2
        for line in list(self.pipeline.log)[-nn:]:
            self.echo_yx(y, x+2, term.cyan(line))
            y += 1
        #self.echo_yx(h-1, w-20, 'Hello World: ' + str(self.pipeline.n))

    async def start_async(self):
        term = self.term
        while True:
            inkey = term.inkey(0.04)
            if inkey == 'q':
                break
            self.redraw()
            await asyncio.sleep(0.5)
        return self
      
@contextmanager
def start_tui(pipeline):
    term = Terminal()
    with term.hidden_cursor(), \
            term.raw(), \
            term.location(), \
            term.fullscreen(), \
            term.keypad():
        tui = TaskTUI(term, pipeline)
        yield tui

