import pynput.keyboard as pk

clavier = pk.Controller()
clavier.press("a")
clavier.release("a")
