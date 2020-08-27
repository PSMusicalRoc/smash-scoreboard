import pyglet, glooey, json, time
import Widgets
from Widgets.WidgetPrimitives import *
from Widgets.globals import _important_vars
import Widgets.OutputHandler as Out

#Define Globals for later
grid = None
gui = None
gui_batch = None
window = None

# Define functions for later

def parseAutoloadJSON():
  file = open(Widgets.DOCUMENTS_PATH + "autoload.json", 'r')
  jsonDump = json.load(file)

  global grid
  for object in jsonDump:
    position = (object['x'], object['y'])
    object_type = object['type']
    if object_type == 'CharSelect':
      grid[position[1], position[0]] = Widgets.CharacterSelect(position, name=object['name'])
    elif object_type == 'PlayerName':
      grid[position[1], position[0]] = Widgets.PlayerNameInput(position, name=object['name'])
    elif object_type == 'StockText':
      grid[position[1], position[0]] = Widgets.ScoreInputText(position, name=object['name'])
    else:
      grid[position[1], position[0]] = Widgets.EmptySlot(position)
      
def createMainWindow(dt):
  global gui_batch
  gui_batch = pyglet.graphics.Batch()

  global window
  window = pyglet.window.Window(1920, 1080,
                                caption="Smash Scoreboard 4.0")
  window.set_icon(pyglet.resource.image('icon16.png'), pyglet.resource.image('icon32.png'))
  
  global gui
  gui = glooey.Gui(window, batch=gui_batch)

  global grid
  grid = Grid(4, 3)
  grid.set_row_height(3, 20)

  _important_vars.update({
    "window": window,
    "gui": gui,
    "gui_batch": gui_batch,
    'grid': grid
  })

  try:
    parseAutoloadJSON()
  except FileNotFoundError:
    for y in range(3):
      for x in range(3):
        grid[y, x] = Widgets.EmptySlot((x, y))
  grid[3, 1] = Out.UpdateButton()
  grid[3, 0] = Out.SaveLayoutButton()

  stack = glooey.Stack()
  stack.add_back(WindowBackground())
  stack.add_front(grid)

  gui.add(stack)

  @window.event
  def on_draw():
    window.clear()
    gui_batch.draw()
  
  global fader
  fader.close()

# Main code

display = pyglet.canvas.get_display()
screens = display.get_screens()

width, height = screens[0].width, screens[0].height
window_width, window_height = 1000, 600
position_x = int((width/2) - (window_width/2))
position_y = int((height/2) - (window_height/2))

fader = pyglet.window.Window(window_width, window_height,
                            style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
fader.set_location(position_x, position_y)

fader_batch = pyglet.graphics.Batch()
image = pyglet.image.load('Fader.png')

@fader.event
def on_draw():
  fader.clear()
  image.blit(0, 0)

pyglet.clock.schedule_once(createMainWindow, 3)

pyglet.app.run()