import colorama as cr
from frunner.common import State

def print_task(name, state):
    if state == State.PENDING:
        bg = cr.Back.LIGHTBLACK_EX 
        fg = cr.Fore.RED
    elif state == State.READY:
        bg = cr.Back.LIGHTBLACK_EX 
        fg = cr.Fore.GREEN
    elif state == State.WAITING:
        bg = cr.Back.LIGHTBLACK_EX 
        fg = cr.Fore.WHITE
    elif state == State.RUNNING:
        bg = cr.Back.LIGHTBLUE_EX
        fg = cr.Fore.BLUE
    elif state == State.COMPLETED:
        bg = cr.Back.RESET
        fg = cr.Fore.YELLOW
    else:
        raise ValueError('wtf')
    reset = cr.Style.RESET_ALL
    name = "{0:<15}".format(name[0:15])
    print(f"{fg}┃{bg}{name}{reset}{fg}┃──○──◉{reset}")

#print_task("TASK 0", State.COMPLETED)
#print_task("TASK 1", State.RUNNING)
#print_task("Task AAA", State.READY)
#print_task("Task BBBBBBZZZZZ", State.WAITING)
#print_task("More Waiting", State.WAITING)

print("┃Task A ┃──◆")
print("┃Task Z ┃─────◆")
print("┃Task B ┃─────◉──◇")
print("┃Task C ┃────────○──◇")
print("┃Task E ┃────────○──◇")
print("┃Task D ┃─────◉─────◇")

            
