import pyglet, glooey
import Widgets
from Widgets.WidgetPrimitives import *
from Widgets.globals import _important_vars
import Widgets.OutputHandler as Out

gui_batch = pyglet.graphics.Batch()

window = pyglet.window.Window(1920, 1080,
                              caption="Smash Scoreboard 4.0")
gui = glooey.Gui(window, batch=gui_batch)

grid = Grid(4, 3)
grid.set_row_height(3, 20)
for y in range(3):
  for x in range(3):
    grid[y, x] = Widgets.EmptySlot((x, y))
grid[3, 1] = Out.UpdateButton()

stack = glooey.Stack()
stack.add_back(WindowBackground())
stack.add_front(grid)

gui.add(stack)

@window.event
def on_draw():
  window.clear()
  gui_batch.draw()

_important_vars.update({
  "window": window,
  "gui": gui,
  "gui_batch": gui_batch,
  "grid": grid
})

pyglet.app.run()