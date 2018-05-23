
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,os,time

def check(url):

	REPO_FOLDER,INFO = url.split('|SPLIT|')
	
	if not os.path.exists(REPO_FOLDER):
		f = open(INFO,mode='r'); msg = f.read(); f.close()
		TextBoxes("%s" % msg)
		quit()
	else: return
	
def TextBoxes(announce):
	class TextBox():
		WINDOW=10147
		CONTROL_LABEL=1
		CONTROL_TEXTBOX=5
		def __init__(self,*args,**kwargs):
			xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
			self.win=xbmcgui.Window(self.WINDOW) # get window
			xbmc.sleep(500) # give window time to initialize
			self.setControls()
		def setControls(self):
			self.win.getControl(self.CONTROL_LABEL).setLabel('[COLOR snow]Sports[/COLOR]') # set heading
			try: f=open(announce); text=f.read()
			except: text=announce
			self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
			return
	TextBox()
	while xbmc.getCondVisibility('Window.IsVisible(10147)'):
		time.sleep(.5)

