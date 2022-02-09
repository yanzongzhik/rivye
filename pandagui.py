import xbmc, xbmcgui

KEY_BUTTON_BACK = 275
KEY_KEYBOARD_ESC = 61467

ACTION_PARENT_DIR = 9
ACTION_PREVIOUS_MENU = 10
ACTION_NEXT_ITEM = 14
ACTION_NAV_BACK = 92

BTN_THUMB_DN = 330
BTN_THUMB_UP = 331
BTN_PLAY_PAUSE = 332
BTN_SKIP = 333
BTN_INFO = 334
BTN_HIDE = 335

BTN_TIRED = 336
BTN_THUMBED_DN = 337
BTN_THUMBED_UP = 338

STATION_LIST_ID = 200

class PandaGUI(xbmcgui.WindowXMLDialog):

	def setPanda( self, panda ):
		self.panda = panda

	def onInit(self):
		print "PANDORA: Window Initalized!!!"
		play_station_n = -1
		last_station_id = self.panda.settings.getSetting('last_station_id')
		auto_start = self.panda.settings.getSetting('auto_start')
		self.list = self.getControl( STATION_LIST_ID )
		dlg = xbmcgui.DialogProgress()
		dlg.create( "PANDORA", "Fetching Stations" )
		dlg.update( 0 )
		stations = {}
		station_names = []
		for s in self.panda.getStations():
			#print "station[%s] = %s, %s" % (s.name.encode('utf-8'), s.id.encode('utf-8'), s.isQuickMix)
			if s.isQuickMix:
				s.name = "* [ "+s.name+" ]"
			tmp = xbmcgui.ListItem(s.name)
			tmp.setProperty( "stationId", s.id )
			stations[s.name] = tmp
			station_names.append( s.name )
		if self.panda.settings.getSetting( "sort_stations" ) == "true":
			station_names = sorted( station_names )
		station_list = []
		for name in station_names:
			station_list.append( stations[name] )
			if stations[name].getProperty('stationId') == last_station_id:
				play_station_n = len(station_list) - 1
			print "station_list[%s]{name, id} = {%s, %s}" % ( len(station_list)-1, station_list[len(station_list)-1].getLabel(), station_list[len(station_list)-1].getProperty('stationId'))
		self.list.addItems( station_list )
		dlg.close()
		self.getControl(BTN_THUMBED_DN).setVisible(False)
		self.getControl(BTN_THUMBED_UP).setVisible(False)

		logo = self.getControl(100)
		if self.panda.settings.getSetting( "logo" ) == "false":
			logo.setPosition(-100, -100)

		if ( auto_start == "true" ) & ( play_station_n >= 0 ):
			dlg.create( "PANDORA", "Now starting station: "+station_list[play_station_n].getLabel().encode('utf-8') )
			dlg.update( 0 )
			self.list.selectItem( play_station_n )
			self.setFocusId( STATION_LIST_ID )
			##print "START: station_list[%s]{name, id} = {%s, %s}" % ( play_station_n, station_list[play_station_n].getLabel(), station_list[play_station_n].getProperty('stationId'))
			##print "START: station_list[%s]{name, id} = {%s, %s}" % ( play_station_n, self.list.getSelectedItem().getLabel(), self.list.getSelectedItem().getProperty('stationId'))
			print "START: station_id = %s" % last_station_id
			self.panda.playStation( last_station_id )
			dlg.close


	def onAction(self, action):
		buttonCode =  action.getButtonCode()
		actionID   =  action.getId()
		if ( actionID in ( ACTION_PREVIOUS_MENU, ACTION_NAV_BACK, \
                           ACTION_PARENT_DIR ) ):
			if xbmc.getCondVisibility( 'Skin.HasSetting(PandoraVis)' ):
				xbmc.executebuiltin( 'Skin.Reset(PandoraVis)' )
				#xbmc.executebuiltin( "SetProperty(HidePlayer,False)" )
			else:
				self.panda.quit()


		elif (actionID == ACTION_NEXT_ITEM ):
			self.panda.skipSong()

	def onClick(self, controlID):
		if (controlID == STATION_LIST_ID): # station list control
			selItem = self.list.getSelectedItem()
			self.panda.playStation( selItem.getProperty("stationId") )
		elif self.panda.playing:
			if controlID == BTN_THUMB_DN:
				self.getControl(BTN_THUMB_DN).setVisible(False)
				self.getControl(BTN_THUMBED_DN).setVisible(True)
				self.getControl(BTN_THUMB_UP).setVisible(True)
				self.getControl(BTN_THUMBED_UP).setVisible(False)
				self.panda.addFeedback( 'ban' )
				self.panda.playNextSong()
			elif controlID == BTN_THUMB_UP:
				self.getControl(BTN_THUMB_DN).setVisible(True)
				self.getControl(BTN_THUMBED_DN).setVisible(False)
				self.getControl(BTN_THUMB_UP).setVisible(False)
				self.getControl(BTN_THUMBED_UP).setVisible(True)
				self.panda.addFeedback( 'love' )
			elif controlID == BTN_PLAY_PAUSE:
				pass #Handled by skin currently, further functionality TBD
			elif controlID == BTN_SKIP:
				self.panda.playNextSong()
			elif controlID == BTN_INFO:
				pass #TODO
			elif controlID == BTN_TIRED:
				#obj = self.getControl(BTN_TIRED)
				#for attr in dir(obj):
				#	print ">>> obj.%s = %s" % (attr, getattr(obj, attr))
				self.panda.addTiredSong()
				self.panda.playNextSong()
			elif controlID == BTN_HIDE:
				pass #Handled by skin

	def onFocus(self, controlID):
		pass
