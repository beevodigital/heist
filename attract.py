import procgame.game

font_tiny7 = procgame.dmd.Font("./dmd/04B-03-7px.dmd")
font_jazz18 = procgame.dmd.Font("./dmd/Jazz18-18px.dmd")
font_14x10 = procgame.dmd.Font("./dmd/Font14x10.dmd")
font_18x12 = procgame.dmd.Font("./dmd/Font18x12.dmd")
font_07x4 = procgame.dmd.Font("./dmd/Font07x4.dmd")
font_07x5 = procgame.dmd.Font("./dmd/Font07x5.dmd")
font_09Bx7 = procgame.dmd.Font("./dmd/Font09Bx7.dmd")

class PrepareToStart(procgame.game.Mode):
	"""Manages waiting for the game to be ready to start."""
	def __init__(self, game):
		super(PrepareToStart, self).__init__(game=game, priority=9)
	
	def mode_started(self):
		self.game.trough.changed_handlers.append(self.trough_changed)
		self.pulse_and_delay()
	
	def mode_stopped(self):
		self.game.trough.changed_handlers.remove(self.trough_changed)
	
	def trough_changed(self):
		self.check_ready()
	
	def check_ready(self):
		"""Perform checks on the system state to see if we are ready to start the game."""
		print(self.game.trough.is_full())
		if self.game.trough.is_full():
			self.ready()
			return True
		
		return False
	
	def pulse_and_delay(self):
		ready = self.check_ready()
		if not ready:
			#self.game.coils.upperRightPopper.pulse()
			#self.game.coils.lowerRightPopper.pulse()
			self.delay(name='pulse_and_delay',
			           event_type=None,
			           delay=5.0,
			           handler=self.pulse_and_delay)
		
	def ready(self):
		"""Called to indicate that the game is ready to start."""
		# Remove attract mode from mode queue - Necessary?
		self.game.modes.remove(self)
		# Initialize game	
		self.game.start_game()
		# Add the first player
		self.game.add_player()
		# Start the ball.  This includes ejecting a ball from the trough.
		self.game.start_ball()



class Attract(procgame.game.Mode):
	"""A mode that runs whenever the game is in progress."""
	def __init__(self, game):
		super(Attract, self).__init__(game=game, priority=9)



		# TODO: Setup an attract mode layer
	
### TODO: commented out lamps for now BDE 2/24
	def mode_started(self):
		#self.pre_game_display()
		print('in mode started Attract')
		self.heistIntro = procgame.dmd.TextLayer(128/2, 7, font_jazz18, "center", opaque=True).set_text("THE HEIST")
		self.basicCreds = procgame.dmd.TextLayer(128/2, 12, font_09Bx7, "center", opaque=True).set_text("BY BRIAN")
		self.basicCredsSeconday = procgame.dmd.TextLayer(128/2, 12, font_09Bx7, "center", opaque=True).set_text("RYAN BRANDON")
		self.press_start = procgame.dmd.TextLayer(128/2, 12, font_09Bx7, "center", opaque=True).set_text("PRESS START")

		script = [{'seconds':3.0, 'layer':self.heistIntro},
			  {'seconds':2.0, 'layer':self.basicCreds},
			  {'seconds':2.0, 'layer':self.basicCredsSeconday},
			  {'seconds':3.0, 'layer':self.press_start}]

		self.layer = procgame.dmd.ScriptedLayer(width=128, height=32, script=script)
		#self.layer.on_complete = self.post_game_display

		#self.game.lamps.startButton.schedule(schedule=0xffff0000, cycle_seconds=0, now=False)
		#self.game.lamps.insertPlayfieldLower.enable()
		#self.game.lamps.insertPlayfieldMiddle.enable()
		#self.game.lamps.insertPlayfieldUpper.enable()
	
	#def mode_stopped(self):
		#self.game.lamps.startButton.disable()

	def sw_startButton_active(self, sw):
		self.game.modes.remove(self)
		# TODO: PrepareToStart should just be 'startup ball search.'
		#       We don't want to start the game immediately after we find the balls.
		self.game.modes.add(PrepareToStart(game=self.game))