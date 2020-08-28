import glooey, pyglet
import Widgets.globals as Globals

class ButtonBaseBackground(glooey.Background):
  custom_center = pyglet.resource.texture('Widgets/Textures/BaseButton/ButtonCenter.png')
  custom_top = pyglet.resource.texture('Widgets/Textures/BaseButton/ButtonBorder.png')
  custom_bottom = pyglet.resource.texture('Widgets/Textures/BaseButton/ButtonBorder.png')
  custom_left = pyglet.resource.texture('Widgets/Textures/BaseButton/ButtonBorder.png')
  custom_right = pyglet.resource.texture('Widgets/Textures/BaseButton/ButtonBorder.png')
  custom_top_left = pyglet.resource.texture('Widgets/Textures/BaseButton/ButtonBorder.png')
  custom_top_right = pyglet.resource.texture('Widgets/Textures/BaseButton/ButtonBorder.png')
  custom_bottom_left = pyglet.resource.texture('Widgets/Textures/BaseButton/ButtonBorder.png')
  custom_bottom_right = pyglet.resource.texture('Widgets/Textures/BaseButton/ButtonBorder.png')

class BaseButton(glooey.Button):
  def __init__(self, *args, **kwargs):
    super().__init__(args, kwargs)
  
  class Background(ButtonBaseBackground):
    custom_center = pyglet.resource.texture('Widgets/Textures/CharacterSelectButton/ButtonBackground.png')

  class Over(ButtonBaseBackground):
    custom_center = pyglet.resource.texture('Widgets/Textures/CharacterSelectButton/ButtonBackgroundHover.png')

  class Down(ButtonBaseBackground):
    custom_center = pyglet.resource.texture('Widgets/Textures/CharacterSelectButton/ButtonBackgroundPress.png')

class CharacterSelectButton(BaseButton):
  def __init__(self, filename, image):
    super().__init__()
    self.image_filename = filename
    
    self._foreground.set_image(image)

  class Foreground(glooey.Image):
    pass
  
  class Off(ButtonBaseBackground):
    custom_center = pyglet.resource.texture("Widgets/Textures/CharacterSelectButton/ButtonBackgroundSelected.png")
  
  def on_click(self, w):
    #Goes into the grid, then the mover, then the scrollpane, another grid, then the scrollbox,
    #the HBox, then finally into the base widget
    base_widget = self.parent.parent.parent.parent.parent.parent.parent
    parent_grid = self.parent

    for button in parent_grid._Widget__yield_all_children():
      if isinstance(button, glooey.Button):
        button.enable()
    base_widget.output_filename = self.image_filename
    self.disable()

class Grid(glooey.Grid):
  custom_cell_padding = 5
  custom_padding = 5

class IntEditableLabel(glooey.Form):
  class Label(glooey.EditableLabel):
    custom_font_name = "Segoe UI"
    custom_font_size = 10
    custom_color = "#000000"
    custom_selection_color = "#ffffff"
    custom_selection_background_color = "#3390ff"
    custom_padding = 2
    if Globals.SIZE_MODE == "1920x1080":
      custom_size_hint = (160, 20)
    else:
      custom_size_hint = (80, 20)
    custom_text_alignment = 'center'

    def on_insert_text(self, start, text):
      no_int_text = ""
      for letter in text:
        if letter in "1234567890":
          no_int_text += letter
      
      self._text += no_int_text
      if self._text == "":
        pass
      else:
        if int(self._text) > 999:
          self._text = "999"
      self._layout.document.text = self._text
      self.dispatch_event('on_edit_text', self)

  class Base(glooey.Background):
    custom_center = pyglet.resource.texture('Widgets/Textures/TextInput/TextInputCenter.png')
    custom_top = pyglet.resource.texture('Widgets/Textures/TextInput/TextInputTop.png')
    custom_bottom = pyglet.resource.texture('Widgets/Textures/TextInput/TextInputBottom.png')
    custom_left = pyglet.resource.texture('Widgets/Textures/TextInput/TextInputLeft.png')
    custom_right = pyglet.resource.texture('Widgets/Textures/TextInput/TextInputRight.png')
    custom_top_left = pyglet.resource.texture('Widgets/Textures/TextInput/TextInputTopLeft.png')
    custom_top_right = pyglet.resource.texture('Widgets/Textures/TextInput/TextInputTopRight.png')
    custom_bottom_left = pyglet.resource.texture('Widgets/Textures/TextInput/TextInputBottomLeft.png')
    custom_bottom_right = pyglet.resource.texture('Widgets/Textures/TextInput/TextInputBottomRight.png')
  
  def do_regroup_children(self):
    self._label._regroup(pyglet.graphics.OrderedGroup(2, self.group))
    self._bg._regroup(pyglet.graphics.OrderedGroup(1, self.group))

class IntBox(glooey.HBox):
  def __init__(self):
    super().__init__()

    self.int_input = IntEditableLabel()

    self.pack(self.SubButton(self.int_input))
    self.add(self.int_input)
    self.pack(self.AddButton(self.int_input))
  
  class AddButton(BaseButton):
    def __init__(self, int_input):
      super().__init__()
      self.int_input = int_input

    class Background(ButtonBaseBackground):
      custom_center = pyglet.resource.texture("Widgets/Textures/IntBox/Add.png")
    
    class Over(ButtonBaseBackground):
      custom_center = pyglet.resource.texture("Widgets/Textures/IntBox/AddHover.png")
    
    class Down(ButtonBaseBackground):
      custom_center = pyglet.resource.texture("Widgets/Textures/IntBox/AddPress.png")

    def on_click(self, w):
      try:
        current_num = int(self.int_input._label._text)
      except ValueError:
        current_num = 0
      current_num += 1
      if current_num > 999:
        current_num = 999
      self.int_input._label._text = str(current_num)
      self.int_input._label._layout.document.text = str(current_num)
      self.int_input._label.dispatch_event('on_edit_text', self.int_input)
    
  class SubButton(BaseButton):
    def __init__(self, int_input):
      super().__init__()
      self.int_input = int_input

    class Background(ButtonBaseBackground):
      custom_center = pyglet.resource.texture("Widgets/Textures/IntBox/Sub.png")
    
    class Over(ButtonBaseBackground):
      custom_center = pyglet.resource.texture("Widgets/Textures/IntBox/SubHover.png")
    
    class Down(ButtonBaseBackground):
      custom_center = pyglet.resource.texture("Widgets/Textures/IntBox/SubPress.png")

    def on_click(self, w):
      try:
        current_num = int(self.int_input._label._text)
      except ValueError:
        current_num = 0
      current_num -= 1
      if current_num < 0:
        current_num = 0
      self.int_input._label._text = str(current_num)
      self.int_input._label._layout.document.text = str(current_num)
      self.int_input._label.dispatch_event('on_edit_text', self.int_input)

class ScrollBox(glooey.ScrollBox):
  custom_alignment = 'center'

  class VBar(glooey.VScrollBar):
    custom_scale_grip = True

    class Decoration(glooey.Background):
      custom_top = pyglet.resource.image('Widgets/Textures/ScrollBox/Bar_Ends.png')
      custom_center = pyglet.resource.texture('Widgets/Textures/ScrollBox/Bar_Vert.png')
      custom_bottom = pyglet.resource.image('Widgets/Textures/ScrollBox/Bar_Ends.png')
      custom_vert_padding = 21

    class Forward(glooey.Button):
      custom_base_image = pyglet.resource.image('Widgets/Textures/ScrollBox/Down_Base.png')
      custom_over_image = pyglet.resource.image('Widgets/Textures/ScrollBox/Down_Hover.png')
      custom_down_image = pyglet.resource.image('Widgets/Textures/ScrollBox/Down_Press.png')

    class Backward(glooey.Button):
      custom_base_image = pyglet.resource.image('Widgets/Textures/ScrollBox/Up_Base.png')
      custom_over_image = pyglet.resource.image('Widgets/Textures/ScrollBox/Up_Hover.png')
      custom_down_image = pyglet.resource.image('Widgets/Textures/ScrollBox/Up_Press.png')

    class Grip(glooey.Button):
      custom_height_hint = 20
      custom_alignment = 'fill'

      custom_base_top = pyglet.resource.image('Widgets/Textures/ScrollBox/Grip_Ends_Base.png')
      custom_base_center = pyglet.resource.texture('Widgets/Textures/ScrollBox/Grip_Vert_Base.png')
      custom_base_bottom = pyglet.resource.image('Widgets/Textures/ScrollBox/Grip_Ends_Base.png')

      custom_over_top = pyglet.resource.image('Widgets/Textures/ScrollBox/Grip_Ends_Hover.png')
      custom_over_center = pyglet.resource.texture('Widgets/Textures/ScrollBox/Grip_Vert_Hover.png')
      custom_over_bottom = pyglet.resource.image('Widgets/Textures/ScrollBox/Grip_Ends_Hover.png')

      custom_down_top = pyglet.resource.image('Widgets/Textures/ScrollBox/Grip_Ends_Hover.png')
      custom_down_center = pyglet.resource.texture('Widgets/Textures/ScrollBox/Grip_Vert_Hover.png')
      custom_down_bottom = pyglet.resource.image('Widgets/Textures/ScrollBox/Grip_Ends_Hover.png')

class Slot(glooey.Background):
  custom_center = pyglet.resource.texture('Widgets/Textures/BaseWidget/DefaultBackgroundColor.png')
  custom_top = pyglet.resource.texture('Widgets/Textures/BaseWidget/WidgetTop.png')
  custom_bottom = pyglet.resource.texture('Widgets/Textures/BaseWidget/WidgetBottom.png')
  custom_left = pyglet.resource.texture('Widgets/Textures/BaseWidget/WidgetLeft.png')
  custom_right = pyglet.resource.texture('Widgets/Textures/BaseWidget/WidgetRight.png')
  custom_top_left = pyglet.resource.texture('Widgets/Textures/BaseWidget/WidgetTopLeft.png')
  custom_top_right = pyglet.resource.texture('Widgets/Textures/BaseWidget/WidgetTopRight.png')
  custom_bottom_left = pyglet.resource.texture('Widgets/Textures/BaseWidget/WidgetBottomLeft.png')
  custom_bottom_right = pyglet.resource.texture('Widgets/Textures/BaseWidget/WidgetBottomRight.png')

class Text(glooey.Label):
  custom_font_name = "Segoe UI"
  custom_font_size = 10
  custom_color = "#000000"

class TextInput(glooey.Form):
  class Label(glooey.EditableLabel):
    custom_font_name = "Segoe UI"
    custom_font_size = 10
    custom_color = "#000000"
    custom_selection_color = "#ffffff"
    custom_selection_background_color = "#3390ff"
    custom_padding = 2
    custom_size_hint = (200, 20)

  class Base(glooey.Background):
    custom_center = pyglet.resource.texture('Widgets/Textures/TextInput/TextInputCenter.png')
    custom_top = pyglet.resource.texture('Widgets/Textures/TextInput/TextInputTop.png')
    custom_bottom = pyglet.resource.texture('Widgets/Textures/TextInput/TextInputBottom.png')
    custom_left = pyglet.resource.texture('Widgets/Textures/TextInput/TextInputLeft.png')
    custom_right = pyglet.resource.texture('Widgets/Textures/TextInput/TextInputRight.png')
    custom_top_left = pyglet.resource.texture('Widgets/Textures/TextInput/TextInputTopLeft.png')
    custom_top_right = pyglet.resource.texture('Widgets/Textures/TextInput/TextInputTopRight.png')
    custom_bottom_left = pyglet.resource.texture('Widgets/Textures/TextInput/TextInputBottomLeft.png')
    custom_bottom_right = pyglet.resource.texture('Widgets/Textures/TextInput/TextInputBottomRight.png')
  
  def do_regroup_children(self):
    self._label._regroup(pyglet.graphics.OrderedGroup(2, self.group))
    self._bg._regroup(pyglet.graphics.OrderedGroup(1, self.group))

class WindowBackground(glooey.Background):
  custom_center = pyglet.resource.texture('Widgets/Textures/BaseWidget/DefaultBackgroundColor.png')