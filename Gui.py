from Gui_Client import Gui_Client

# Main GUI controller object; directly referenced by the various Screen objects.
# Initialized by openmoo2.py main procedure.
GUI = Gui_Client()

# ------------------------------------------------------------------------------
if __name__ == '__init__':
    GUI.init('C:\\orion2cd')	
    GUI.run()
