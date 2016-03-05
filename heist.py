import procgame.game
import pinproc
import trough
import attract

import locale

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

locale.setlocale(locale.LC_ALL, "") # Used to put commas in the score.


class BaseGameMode(procgame.game.Mode):
	"""A mode that runs whenever the game is in progress."""
	def __init__(self, game):
		super(BaseGameMode, self).__init__(game=game, priority=1)
		pass
	
	def mode_started(self):
		self.game.trough.changed_handlers.append(self.trough_changed)
	
	def mode_stopped(self): # naming is inconsistent with game_ended/ball_ended
		self.game.trough.changed_handlers.remove(self.trough_changed)

	def trough_changed(self):
		if self.game.trough.is_full():
			self.game.end_ball()
	
class HeistGame(procgame.game.BasicGame):
	
	trough = None
	base_game_mode = None
	
	def __init__(self):
		super(HeistGame, self).__init__(pinproc.MachineTypePDB)
		self.load_config('heist.yaml')
		self.trough = trough.Trough(game=self)
		self.base_game_mode = BaseGameMode(game=self)
		self.attract_mode = attract.Attract(game=self)
		self.reset()
	
	# GameController Methods
	
	def reset(self):
		super(HeistGame,self).reset()
		
		self.modes.add(self.trough)
		self.modes.add(self.attract_mode)
	
	def start_ball(self):
		super(HeistGame, self).start_ball()
	
	def game_started(self):
		self.log("GAME STARTED")
		super(HeistGame, self).game_started()
		# Don't start_ball() here, since Attract does that after calling start_game().
	
	def ball_starting(self):
		self.log("BALL STARTING")
		super(HeistGame, self).ball_starting()
		
		# TODO: Check that there is not already a ball in the shooter lane.
		# TODO: Pulse the trough until we get a hit from the shooter lane switch.
		self.coils.trough.pulse() # eject a ball into the shooter lane
		
		self.enable_flippers(True)
		self.modes.add(self.base_game_mode)

	def ball_ended(self):
		"""Called by end_ball(), which is itself called by base_game_mode.trough_changed."""
		self.log("BALL ENDED")
		self.modes.remove(self.base_game_mode)
		self.enable_flippers(False)
		super(HeistGame, self).ball_ended()

	def game_ended(self):
		self.log("GAME ENDED")
		super(HeistGame, self).game_ended()
		self.modes.remove(self.base_game_mode)
		self.modes.add(self.attract_mode)

## main:

def main():
	game = None
	try:
	 	game = HeistGame()
	 	print('flippers enabled')
	 	game.enable_flippers(True)
		game.run_loop()
	finally:
		del game

if __name__ == '__main__':
	main()