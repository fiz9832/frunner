import urwid
import threading

def wait_screen(fun):
    txt = urwid.Text("Waiting...")
    fill = urwid.Filler(txt, 'middle')
    args = (txt, )
    t = threading.Thread(target=fun, args=args)
    t.start()
    loop = urwid.MainLoop(fill)
    loop.run()

def start_counter(txt):
    import time
    n = 0
    while True:
        txt.set_text(f'Hello {n}')
        time.sleep(1)
        n += 1

if __name__ == '__main__':
    wait_screen(start_counter)
