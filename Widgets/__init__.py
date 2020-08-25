import glooey, pyglet, os, json
from Widgets.WidgetPrimitives import *
import Widgets.globals as Globals
import PIL.Image as Image

DOCUMENTS_PATH = os.path.expandvars("C:\\Users\\%username%\\Documents\\Smash Scoreboard\\")

def dialogOnClose():
  Globals.dialog.has_exit = True
  Globals.dialog = None

def importCharacterButtonImages(character_name):
  size = 128, 128
  directory = "C:\\Users\\%username%\\Documents\\Smash Scoreboard\\ImgCache\\Ultimate Full Art\\" + character_name + "\\"
  expanded_path = os.path.expandvars(directory)
  
  i = 1
  fail = False
  list = []
  while not fail:
    try:
      if i < 10:
        image = Image.open(expanded_path + character_name + "_0" + str(i) + ".png")
        image.thumbnail(size)
        raw_image = image.tobytes()
        pyglet_image = pyglet.image.ImageData(image.width, image.height, 'RGBA', raw_image, pitch=-image.width * 4)
        character_button = CharacterSelectButton(expanded_path + character_name + "_0" + str(i) + ".png", pyglet_image)
        list.append(character_button)
      elif i >= 10:
        image = Image.open(expanded_path + character_name + "_" + str(i) + ".png")
      elif i < 99:
        raise FileNotFoundError("Too many images in " + character_name + " folder, stopping at 99")
    except FileNotFoundError:
      fail = True  
    i += 1
  
  return list

def getImgList(self, char, dir):
  fail = False
  i = 1
  list = []
  while not fail:
    try:
      if i < 10:
        open(dir+char+"_0"+str(i)+".png")
        list.append(dir+char+"_0"+str(i)+".png")
      elif i >= 10:
        open(dir+char+"_"+str(i)+".png")
        list.append(dir+char+"_"+str(i)+".png")
    except:
      fail=True
    i += 1
  return list
  
  ## Extract images from their files and make them 128x128 for the buttons

def checkNameAvailability(name):
  for element in Globals._important_vars['grid']._Widget__yield_all_children():
    try:
      if element.name == name:
        if name.endswith("_1"):
          suffix = int(name[-1])
          new_name = name[:-1]
          name = new_name + str(suffix + 1)
        else:
          name += "_1"
    except AttributeError:
      pass
  return name

def writeJSONFile():
  output = []
  grid = Globals._important_vars['grid']
  for child in grid._Widget__yield_all_children():
    if isinstance(child, glooey.Stack):
      try:
        child.x
        child.y
        if isinstance(child, CharacterSelect):
          child_type = "CharSelect"
        elif isinstance(child, PlayerNameInput):
          child_type = "PlayerName"
        elif isinstance(child, ScoreInputText):
          child_type = "StockText"
        else:
          child_type = "EmptySlot"

        try:
          output.append({
            'x': child.x,
            'y': child.y,
            'type': child_type,
            'name': child.name
          })
        except AttributeError:
          output.append({
            'x': child.x,
            'y': child.y,
            'type': child_type
          })
      except AttributeError:
        pass
  file = open(DOCUMENTS_PATH + "autoload.json", 'w')
  json.dump(output, file)

#####################################
# START EXPLICIT WIDGET DEFINITIONS #
#####################################

class AddButton(BaseButton):

  def __init__(self, cell):
    super().__init__()

    if isinstance(cell, tuple):
      self.x = cell[0]
      self.y = cell[1]
    else:
      self.x = 0
      self.y = 0

  class Background(ButtonBaseBackground):
    custom_center = pyglet.resource.texture('Widgets/Textures/AddButton/WidgetAdd.png')
  
  class Over(ButtonBaseBackground):
    custom_center = pyglet.resource.texture('Widgets/Textures/AddButton/WidgetAddHover.png')
  
  class Down(ButtonBaseBackground):
    custom_center = pyglet.resource.texture('Widgets/Textures/AddButton/WidgetAddPress.png')
  
  def on_click(self, w):
    if Globals.dialog != None:
      pass
    else:    
      Globals.dialog = pyglet.window.Window(height=300, width=300,
                                    caption="Select Widget for Cell " + str(self.x+1) +", " + str(self.y+1),
                                    style=pyglet.window.Window.WINDOW_STYLE_DIALOG)
      Globals.dialog.set_icon(pyglet.resource.image('icon16.png'), pyglet.resource.image('icon32.png'))
      dialog_gui_batch = pyglet.graphics.Batch()
      dialog_gui = glooey.Gui(Globals.dialog, batch=dialog_gui_batch)

      dialog_gui.add(SelectWidgetDialog((self.x, self.y)))

      @Globals.dialog.event
      def on_draw():
        Globals.dialog.clear()
        dialog_gui_batch.draw()
      
      @Globals.dialog.event
      def on_close():
        dialogOnClose()

class DelButton(AddButton):
  class Background(ButtonBaseBackground):
    custom_center = pyglet.resource.texture('Widgets/Textures/DelButton/WidgetDelete.png')
  
  class Over(ButtonBaseBackground):
    custom_center = pyglet.resource.texture('Widgets/Textures/DelButton/WidgetDeleteHover.png')
  
  class Down(ButtonBaseBackground):
    custom_center = pyglet.resource.texture('Widgets/Textures/DelButton/WidgetDeletePress.png')
  
  def on_click(self, w):
    grid = Globals._important_vars['grid']
    try:
      assert(grid != None)
    except AssertionError:
      raise RuntimeError("'grid' is unspecified: Is there a grid instantiated in the GUI?")

    for widget in grid._Widget__yield_all_children():
      try:
        if widget.x == self.x and widget.y == self.y:
          grid[self.y, self.x] = EmptySlot((self.x, self.y))
          break
      except:
        pass

class EmptySlot(glooey.Stack):

  def __init__(self, position):
    super().__init__()

    if isinstance(position, tuple):
      self.x = position[0]
      self.y = position[1]
    else:
      self.x = 0
      self.y = 0
    
    self.background = Slot()
    self.button = AddButton((self.x, self.y))
    self.board = glooey.Board()

    self.board.add(self.button, bottom=50, left_percent=.8)

    self.add_back(self.background)
    self.add_front(self.board)

class OptionsButton(BaseButton):
  def __init__(self, position):
    super().__init__()
    self.position = position

  class Foreground(glooey.Image):
    custom_image = pyglet.resource.image('Widgets/Textures/OptionsButton/Gear.png')

  def on_click(self, w):
    parent = self.parent.parent

    if Globals.dialog != None:
      pass
    else:
      Globals.dialog = pyglet.window.Window(height=300, width=300,
                                            caption="Options for " + parent.name,
                                            style=pyglet.window.Window.WINDOW_STYLE_DIALOG)
      Globals.dialog.set_icon(pyglet.resource.image('icon16.png'), pyglet.resource.image('icon32.png'))
      new_gui_batch = pyglet.graphics.Batch()
      new_gui = glooey.Gui(Globals.dialog, batch=new_gui_batch)

      try:
        new_gui.add(self.parent.parent.Options(self.position))
      except AttributeError:
        new_gui.add(BaseOptionsMenu(self.position))

      @Globals.dialog.event
      def on_draw():
        Globals.dialog.clear()
        new_gui_batch.draw()
      
      @Globals.dialog.event
      def on_close():
        dialogOnClose()

class BaseOptionsMenu(glooey.Stack):
  def __init__(self, position):
    super().__init__()

    self.position = position
    self.add_back(Slot())

    self.vbox = glooey.VBox()
    self.top = ScrollBox()
    self.bottom = glooey.HBox()
    self.bottom.set_padding(5)

    # Add widgets to Top
    grid = Grid()
    grid[0, 0] = Text("Widget Name:")
    grid[1, 0] = self.name_input = TextInput()
    self.top.add(grid)

    #Add widgets to Bottom
    self.bottom.add(self.CancelButton())
    self.bottom.add(self.ConfirmButton())

    self.vbox.add(self.top, 'expand')
    self.vbox.add(self.bottom, 30)

    self.add(self.vbox)

  class ConfirmButton(BaseButton):
    class Foreground(Text):
      custom_text = 'Confirm!'
      custom_bold = True
      custom_horz_padding = 15
      custom_vert_padding = 4

    def on_click(self, w):
      raise NotImplementedError()

  class CancelButton(BaseButton):
    class Foreground(Text):
      custom_text = 'Cancel'
      custom_horz_padding= 10
      custom_vert_padding = 4

      def on_click(self, w):
        raise NotImplementedError()

############### SELECTWIDGETDIALOG BUTTONS #################

class BaseSelectButton(BaseButton):

  def __init__(self, position):
    super().__init__()

    if isinstance(position, tuple):
      self.x = position[0]
      self.y = position[1]
    else:
      self.x = 0
      self.y = 0

    self.description = "No Description"

  class Background(ButtonBaseBackground):
    #custom_center = pyglet.resource.texture("Widgets/Textures/SelectWidgetDialog/TextInput.png")
    custom_center = pyglet.resource.texture("ICS_Test.png")
  
  class Over(ButtonBaseBackground):
    custom_center = pyglet.resource.texture("Widgets/Textures/SelectWidgetDialog/TextInputHover.png")
  
  class Down(ButtonBaseBackground):
    custom_center = pyglet.resource.texture("Widgets/Textures/SelectWidgetDialog/TextInputPress.png")
  
  def on_click(self, w):
    gui = Globals._important_vars['gui']
    grid = Globals._important_vars['grid']
    try:
      assert(grid)
    except AssertionError:
      raise RuntimeError("'grid' is unspecified: Is there a grid instantiated in the GUI?")

    for widget in gui._Widget__yield_all_children():
      if isinstance(widget, EmptySlot):
        if widget.x == self.x and widget.y == self.y:
          #grid[self.y, self.x] = Slot()
          grid[self.y, self.x] = CharacterSelect((self.x,self.y))
          Globals.dialog.close()
          Globals.dialog = None
          break

class CharacterSelectWidgetButton(BaseButton):
  def __init__(self, position):
    super().__init__()

    if isinstance(position, tuple):
      self.x = position[0]
      self.y = position[1]
    else:
      self.x = 0
      self.y = 0

    self.description = "Character Portrait Selection Widget"

  class Foreground(glooey.Image):
    custom_image = pyglet.resource.image("Widgets/Textures/SelectWidgetDialog/CharacterSelectButton.png")

  def on_click(self, w):
    gui = Globals._important_vars['gui']
    grid = Globals._important_vars['grid']
    try:
      assert(grid)
    except AssertionError:
      raise RuntimeError("'grid' is unspecified: Is there a grid instantiated in the GUI?")

    for widget in gui._Widget__yield_all_children():
      if isinstance(widget, EmptySlot):
        if widget.x == self.x and widget.y == self.y:
          #grid[self.y, self.x] = Slot()
          grid[self.y, self.x] = CharacterSelect((self.x,self.y))
          Globals.dialog.close()
          Globals.dialog = None
          break

class PlayerNameInputButton(BaseSelectButton):
  def __init__(self, position):
    super().__init__(position)
    self.description = "Widget for Player Tag input"
  
  class Background(ButtonBaseBackground):
    custom_center = pyglet.resource.texture("Widgets/Textures/SelectWidgetDialog/PlayerName.png")
  
  class Over(ButtonBaseBackground):
    custom_center = pyglet.resource.texture("Widgets/Textures/SelectWidgetDialog/PlayerNameHover.png")
  
  class Down(ButtonBaseBackground):
    custom_center = pyglet.resource.texture("Widgets/Textures/SelectWidgetDialog/PlayerNamePress.png")
  
  def on_click(self, w):
    gui = Globals._important_vars['gui']
    grid = Globals._important_vars['grid']
    try:
      assert(grid)
    except AssertionError:
      raise RuntimeError("'grid' is unspecified: Is there a grid instantiated in the GUI?")

    for widget in gui._Widget__yield_all_children():
      if isinstance(widget, EmptySlot):
        if widget.x == self.x and widget.y == self.y:
          grid[self.y, self.x] = PlayerNameInput((self.x, self.y))
          Globals.dialog.close()
          Globals.dialog = None
          break

class StockInputTextButton(BaseSelectButton):

  def __init__(self, position):
    super().__init__(position)
    self.description = "Input Stock Numbers via Textboxes"

  class Background(ButtonBaseBackground):
    custom_center = pyglet.resource.texture("Widgets/Textures/SelectWidgetDialog/StockInputText.png")
  
  class Over(ButtonBaseBackground):
    custom_center = pyglet.resource.texture("Widgets/Textures/SelectWidgetDialog/StockInputTextHover.png")
  
  class Down(ButtonBaseBackground):
    custom_center = pyglet.resource.texture("Widgets/Textures/SelectWidgetDialog/StockInputTextPress.png")

  def on_click(self, w):
    gui = Globals._important_vars['gui']
    grid = Globals._important_vars['grid']
    try:
      assert(grid)
    except AssertionError:
      raise RuntimeError("'grid' is unspecified: Is there a grid instantiated in the GUI?")

    for widget in gui._Widget__yield_all_children():
      if isinstance(widget, EmptySlot):
        if widget.x == self.x and widget.y == self.y:
          grid[self.y, self.x] = ScoreInputText((self.x, self.y))
          Globals.dialog.close()
          Globals.dialog = None
          break

###############  END SELECTWIDGET BUTTONS  #################

############### BEGIN SELECTWIDGET WIDGETS #################

class CharacterSelect(glooey.Stack):
  def __init__(self, position, name=None):
    super().__init__()

    self.x = position[0]
    self.y = position[1]
    self.output_filename = None
    if name != None:
      self.name = checkNameAvailability(name)
      self.name_label = Text(self.name)
    else:
      self.name = checkNameAvailability("CharacterInput")
      self.name_label = Text(self.name)

    self.add_back(Slot())

    self.hbox = self.HBox()
    self.board = glooey.Board()
    self.button = DelButton(position)
    self.options_button = OptionsButton(position)
    
    # Create Left Side of Character Select
    self.left = self.CharacterInput()

    # Create Right Side of the widget
    self.right = ScrollBox()
    self.right.set_height_hint(Globals._important_vars['window'].get_size()[0]/6)
    self.grid = Grid()

    self.changeCharacter("Kirby")

    self.right.add(self.grid)

    self.hbox.add(self.left)
    self.hbox.add(self.right, 'expand')

    self.board.add(self.button, bottom=50, left_percent=.4)
    self.board.add(self.options_button, bottom=50, left_percent=.3)
    self.board.add(self.name_label, bottom_percent=.90, center_x_percent=.25)

    self.add_front(self.hbox)
    self.add_front(self.board)
  
  def checkCharacterValid(self, character_name):
    try:
      path = "C:\\Users\\%username%\\Documents\\Smash Scoreboard\\ImgCache\\Ultimate Full Art\\" + character_name + "\\"
      expanded_path = os.path.expandvars(path)
      open(expanded_path + character_name + "_01.png")
      print("True")
      return True
    except FileNotFoundError:
      print("False")
      return False

  def changeCharacter(self, character_name):
    if self.checkCharacterValid(character_name):
      row = 0
      col = 0
      for image in importCharacterButtonImages(character_name):
        self.grid[row, col] = image
        col += 1
        if col >= 2:
          row += 1
          col = 0
      try:
        while True:
          self.grid[row, col]
          self.grid.remove(row, col)
          col += 1
          if col >= 2:
            row += 1
            col = 0
      except KeyError:
        pass
  
  def update(self):
    filename = self.output_filename
    return ("filename", self.name, filename)

  class HBox(glooey.HBox):
    custom_cell_padding = 5
  
  class CharacterInput(glooey.VBox):
    custom_vert_padding = 5
    custom_horz_padding = 10

    def __init__(self):
      super().__init__()

      self.character_list = []
      path = "C:\\Users\\%username%\\Documents\\Smash Scoreboard\\ImgCache\\Ultimate Full Art\\"
      expanded_path = os.path.expandvars(path)
      for folder in os.walk(expanded_path):
        name = folder[0].replace(expanded_path, '')
        if name != '' and name != "_ScoreNumbers" and name != "_Stocks":
          self.character_list.append(name)

      # Add space for the name label
      self.add(glooey.Spacer(), 35)

      self._text_input = self.TextInput()
      self.custom_cell_padding = 15

      @self._text_input.event
      def on_unfocus(self):
        # Goes to self.left, then self.hbox, then to root widget (self), finally to the method
        self.parent.parent.parent.changeCharacter(self._label._text)
      self.pack(self._text_input)

      self._buttons = []
      for i in range(5):
        self._buttons.append(self.CharacterNameButton(""))
        self.add(self._buttons[i], 30)

    class CharacterNameButton(BaseButton):
      def __init__(self, text=''):
        self.custom_text = text
        super().__init__()
        self.size_hint = (200, 20)
        self.hide()
      
      def on_click(self, w):
        # Here self.parent = self.left in the code
        self.parent.parent.parent.changeCharacter(self._foreground._text)
      
      class Foreground(Text):
        custom_alignment = 'center'

    class TextInput(TextInput):
      class Label(glooey.EditableLabel):
        custom_font_name = "Segoe UI"
        custom_font_size = 10
        custom_color = "#000000"
        custom_selection_color = "#ffffff"
        custom_selection_background_color = "#3390ff"
        custom_padding = 2
        custom_size_hint = (160, 20)

        def on_insert_text(self, start, text):
          self._text = self._layout.document.text
          buttons = self.parent.parent.parent._buttons
          if text != "":
            i = 0
            length = len(self.parent.parent.parent.character_list)
            character_list = self.parent.parent.parent.character_list
            for button in buttons:
              while True:
                if i >= length:
                  button.hide()
                  break
                character_name = character_list[i]
                if self._text.lower() in character_name.lower():
                  button._foreground.set_text(character_name)
                  button.unhide()
                  i += 1
                  break
                i += 1
          else:
            for button in buttons:
              button.hide()

          self.dispatch_event('on_edit_text', self)
        
        def on_delete_text(self, start, text):
          self.on_insert_text(start, text)

  class Options(BaseOptionsMenu):
    class ConfirmButton(BaseOptionsMenu.ConfirmButton):
      def on_click(self, w):
        position = self.parent.parent.parent.position
        grid = Globals._important_vars['grid']
        try:
          assert(grid)
        except AssertionError:
          raise RuntimeError("'grid' not specified, is there a grid instantiated?")
        
        for child in grid._Widget__yield_all_children():
          try:
            if isinstance(child, CharacterSelect):
              if child.x == position[0] and child.y == position[1]:
                options_menu = self.parent.parent.parent
                child.name = checkNameAvailability(options_menu.name_input._label._text)
                child.name_label.set_text(child.name)
          except AttributeError:
            pass
        
        Globals.dialog.close()
        Globals.dialog = None

class ScoreInputText(glooey.Stack):
  def __init__(self, position, name=None):
    super().__init__()

    self.x = position[0]
    self.y = position[1]
    if name != None:
      self.name = checkNameAvailability(name)
      self.name_label = Text(self.name)
    else:
      self.name = checkNameAvailability("Score")
      self.name_label = Text(self.name)

    self.add_back(Slot())

    self.grid = glooey.Grid(5, 5)
    self.grid.set_cell_alignment('center')
    self.board = glooey.Board()
    self.button = DelButton(position)
    self.options_button = OptionsButton(position)

    self.grid.set_row_height(1, 20)
    self.grid.set_row_height(2, 5)
    self.grid.set_row_height(1, 20)

    self.grid.set_col_width(1, 200)
    self.grid.set_col_width(3, 200)

    self.grid[1, 1] = self.p_one_score = IntBox()
    self.grid[1, 3] = self.p_two_score = IntBox()
    self.grid[3, 1] = Text("Player 1 Score")
    self.grid[3, 2] = glooey.Image(pyglet.resource.texture("Widgets/Textures/SelectWidgetDialog/StockInputText.png"))
    self.grid[3, 3] = Text("Player 2 Score")

    self.board.add(self.name_label, bottom_percent=.9, center_x_percent=.5)
    self.board.add(self.button, bottom=50, left_percent=.8)
    self.board.add(self.options_button, bottom=50, left_percent=.7)

    self.add_front(self.grid)
    self.add_front(self.board)

  def update(self):
    p_one_text = self.p_one_score.int_input.get_text()
    p_two_text = self.p_two_score.int_input.get_text()

    p_one_output = ("Text", self.name + "-Player 1", p_one_text)
    p_two_output = ("Text", self.name + "-Player 2", p_two_text)

    return [p_one_output, p_two_output]

  class Options(BaseOptionsMenu):
    class ConfirmButton(BaseOptionsMenu.ConfirmButton):
      def on_click(self, w):
        position = self.parent.parent.parent.position
        grid = Globals._important_vars['grid']
        try:
          assert(grid)
        except AssertionError:
          raise RuntimeError("'grid' not specified, is there a grid instantiated?")
        
        for child in grid._Widget__yield_all_children():
          try:
            if isinstance(child, ScoreInputText):
              if child.x == position[0] and child.y == position[1]:
                options_menu = self.parent.parent.parent
                child.name = checkNameAvailability(options_menu.name_input._label._text)
                child.name_label.set_text(child.name)
          except AttributeError:
            pass
        
        Globals.dialog.close()
        Globals.dialog = None

class PlayerNameInput(glooey.Stack):
  def __init__(self, position, name=None):
    super().__init__()

    self.x = position[0]
    self.y = position[1]
    if name != None:
      self.name = checkNameAvailability(name)
      self.name_label = Text(self.name)
    else:
      self.name = checkNameAvailability("Names")
      self.name_label = Text(self.name)

    self.add_back(Slot())

    self.grid = glooey.Grid(5, 5)
    self.grid.set_cell_alignment('center')
    self.board = glooey.Board()
    self.remove_button = DelButton(position)
    self.options_button = OptionsButton(position)

    self.grid.set_row_height(1, 20)
    self.grid.set_row_height(2, 5)
    self.grid.set_row_height(3, 20)

    self.grid.set_col_width(1, 200)
    self.grid.set_col_width(3, 200)

    self.grid[1, 1] = self.player_one_input = TextInput()
    self.grid[1, 3] = self.player_two_input = TextInput()
    self.grid[3, 1] = Text("Player 1 Name")
    self.grid[3, 2] = glooey.Image(pyglet.resource.texture("Widgets/Textures/SelectWidgetDialog/PlayerName.png"))
    self.grid[3, 3] = Text("Player 2 Name")

    self.board.add(self.remove_button, bottom=50, left_percent=.8)
    self.board.add(self.options_button, bottom=50, left_percent=.7)
    self.board.add(self.name_label, bottom_percent=.9, center_x_percent=.5)

    self.add_front(self.grid)
    self.add_front(self.board)
  
  def update(self):
    p_one_text = self.player_one_input.get_text()
    p_two_text = self.player_two_input.get_text()

    p_one_output = ("Text", self.name + "-Player 1", p_one_text)
    p_two_output = ("Text", self.name + "-Player 2", p_two_text)

    return [p_one_output, p_two_output]

  class Options(BaseOptionsMenu):
    class ConfirmButton(BaseOptionsMenu.ConfirmButton):
      def on_click(self, w):
        position = self.parent.parent.parent.position
        grid = Globals._important_vars['grid']
        try:
          assert(grid)
        except AssertionError:
          raise RuntimeError("'grid' not specified, is there a grid instantiated?")
        
        for child in grid._Widget__yield_all_children():
          try:
            if isinstance(child, PlayerNameInput):
              if child.x == position[0] and child.y == position[1]:
                options_menu = self.parent.parent.parent
                child.name = checkNameAvailability(options_menu.name_input._label._text)
                child.name_label.set_text(child.name)
          except AttributeError:
            pass
        
        Globals.dialog.close()
        Globals.dialog = None

###############  END SELECTWIDGET WIDGETS  #################

class ButtonScrollbox(ScrollBox):
  custom_height_hint = 300
  custom_width_hint = 300

  def __init__(self, position):
    super().__init__()

    self.position = position

    self.grid = Grid(num_cols=2)

    self.button_list = [PlayerNameInputButton(self.position),
                        StockInputTextButton(self.position),
                        CharacterSelectWidgetButton(self.position)]

    for i in range(len(self.button_list)):
      self.grid[i, 0] = self.button_list[i]
      self.grid[i, 1] = Text(self.button_list[i].description, line_wrap=100)
    
    self.add(self.grid)

class SelectWidgetDialog(glooey.Widget):

  def __init__(self, position):
    super().__init__()

    self.position = position

    self.stack = glooey.Stack()
    self.stack.add_back(WindowBackground())

    self.testscroll = ButtonScrollbox(self.position)
    self.stack.add_front(self.testscroll)

    self._attach_child(self.stack)

###################################
# END EXPLICIT WIDGET DEFINITIONS #
###################################