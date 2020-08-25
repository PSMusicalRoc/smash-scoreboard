from Widgets import *
import pyglet, glooey, os, shutil

# output_info in all the instances it is used is defined as the following:
# - A tuple that contains:
#   - tuple[0]: A type identifier in the form of a string (like
#     'filename' or the like)
#   - tuple[1]: The name of the widget (user defined) that the tool
#     will use in the filename of the output
#   - tuple[2]: The data, whether it be text, a filename, or perhaps in the
#     future, raw image data.

class UpdateButton(BaseButton):  
  class Foreground(Text):
    custom_text = "Update!"
    custom_font_size = 20
    custom_bold = True
    custom_horz_padding = 30
  
  def on_click(self, w):
    grid = Globals._important_vars['grid']
    output_data = []

    for element in grid._Widget__yield_all_children():
      try:
        update_info = element.update()
        if isinstance(update_info, list):
          for data in update_info:
            output_data.append(data)
        else:
          output_data.append(update_info)
      except:
        pass
    
    for update_info in output_data:
      data_type = update_info[0]
      if data_type.lower() == "filename":
        self.handleFilename(update_info)
      elif data_type.lower() == "text":
        self.handleText(update_info)
      else:
        raise Exception("'update_info[0]' is not handled by the update function!")

  def handleFilename(self, update_info):
    assert(update_info[0])
    assert(update_info[1])
    assert(update_info[2])

    shutil.copyfile(update_info[2], DOCUMENTS_PATH + "Output\\" + update_info[1] + ".png")

  def handleText(self, update_info):
    assert(update_info[0])
    assert(update_info[1])
    assert(update_info[2])

    try:
      os.remove(DOCUMENTS_PATH + "Output\\" + update_info[1] + ".txt")
    except FileNotFoundError:
      pass
    file = open(DOCUMENTS_PATH + "Output\\" + update_info[1] + ".txt", "w", encoding="UTF-8")
    file.write(update_info[2])
    file.close()

class SaveLayoutButton(BaseButton):
  class Foreground(Text):
    custom_text = "Set as Default Layout"
    custom_font_size = 20
    custom_horz_padding = 30

  def on_click(self, w):
    writeJSONFile()