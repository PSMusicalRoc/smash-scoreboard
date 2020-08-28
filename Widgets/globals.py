#
# Important variables, in this case, will be references to the main
# window, the GUI variable, the GUI Batch() object (in case that
# turns out to be useful), and the dialog that shows up for switching
# widgets.
#
# Now also contains the grid of 9 that the main screen holds.
#
_important_vars = {}
dialog = None

# Here lies code for a new feature, size changes (in this
# case, resolution modes). The idea is that the user can choose
# how large the program is from a list and save that to an options
# file.
#
# Potential values for this variable can be:
# - "1920x1080"
# - "1280x720"
SIZE_MODE = "1280x720"