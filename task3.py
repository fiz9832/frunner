#!/usr/bin/env python
from blessed import Terminal
from time import time

def redraw(term, ctx):
    print(term.clear)
    w, h = term.width, term.height
    with term.location(0, h-1):
        print('Bottom Status Messages')

    with term.location(10, int(h/2)):
        print(ctx['a'])
    with term.location(10, int(h/2)+1):
        print("Press 'q' to quit")
    with term.location(0, 0):
        print(f"n = {ctx['b']}")

def main():
    t = Terminal()
    ctx = dict(a='hello world', b=0)
    with t.hidden_cursor(), \
            t.raw(), t.location(), t.fullscreen(), t.keypad():
        redraw(t, ctx)
        t0 = time()  
        while True:
            inkey = t.inkey(0.04)
            has_key = len(inkey) > 0 
            has_time = time() - t0 > 1.0                
            if has_key: 
                ctx['a'] = "Key Pressed: " + inkey
            if has_time:
                t0 = time()
                ctx['b'] += 1
            if has_key or has_time:
                redraw(t, ctx)
            if inkey == 'q':
                break
    print(t.clear())

if __name__ == '__main__':
    main()

