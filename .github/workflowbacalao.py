from scene import *
import sound
import random
import math
import ui
A = Action

class ButtonNode (SpriteNode):
	def __init__(self, title, *args, **kwargs):
		SpriteNode.__init__(self, 'pzl:Button1', *args, **kwargs)
		button_font = ('Chalkboard SE', 20)
		self.title_label = LabelNode(title, font=button_font, color='#000000', position=(0, 1), parent=self)
		self.title = title

class MenuScene (Scene):
	
	def highscore(self):
 		if (highscore < self.score):
 			highscore = self.score
	
	def __init__(self, title, subtitle, button_titles):
		Scene.__init__(self)
		self.title = title
		self.subtitle = subtitle
		self.button_titles = button_titles
		
	def setup(self):
		button_font = ('Chalkboard SE', 20)
		title_font = ('Chalkboard SE', 36)
		num_buttons = len(self.button_titles)
		self.bg = SpriteNode(color='#5e81d9', parent=self)
		bg_shape = ui.Path.rounded_rect(0, 0, 240, num_buttons * 64 + 140, 8)
		bg_shape.line_width = 4
		shadow = ((0, 0, 0, 0.35), 0, 0, 24)
		self.menu_bg = ShapeNode(bg_shape, (1,1,1,0.9), '#15a4ff', shadow=shadow, parent=self)
		self.title_label = LabelNode(self.title, font=title_font, color='black', position=(0, self.menu_bg.size.h/2 - 40), parent=self.menu_bg)
		self.title_label.anchor_point = (0.5, 1)
		self.subtitle_label = LabelNode(self.subtitle, font=button_font, position=(0, self.menu_bg.size.h/2 - 100), color='#000000', parent=self.menu_bg)
		self.subtitle_label.anchor_point = (0.5, 1)
		self.buttons = []
		for i, title in enumerate(reversed(self.button_titles)):
			btn = ButtonNode(title, parent=self.menu_bg)
			btn.position = 0, i * 64 - (num_buttons-1) * 32 - 50
			self.buttons.append(btn)
		self.did_change_size()
		self.menu_bg.scale = 0
		self.bg.alpha = 0
		self.bg.run_action(A.fade_to(0.4))
		self.menu_bg.run_action(A.scale_to(1, 0.3, TIMING_EASE_OUT_2))
		self.background_color = '#718fd9'
		
	def did_change_size(self):
		self.bg.size = self.size + (2, 2)
		self.bg.position = self.size/2
		self.menu_bg.position = self.size/2
	
	def touch_began(self, touch):
		touch_loc = self.menu_bg.point_from_scene(touch.location)
		for btn in self.buttons:
			if touch_loc in btn.frame:
				sound.play_effect('8ve:8ve-beep-attention')
				btn.texture = Texture('pzl:Button2')
				if __name__ == '__main__':
					run(Bacalao(), show_fps=True)
					
	def touch_ended(self, touch):
		touch_loc = self.menu_bg.point_from_scene(touch.location)
		for btn in self.buttons:
			btn.texture = Texture('pzl:Button1')
			if self.presenting_scene and touch_loc in btn.frame:
				new_title = self.presenting_scene.menu_button_selected(btn.title)
				if new_title:
					btn.title = new_title
					btn.title_label.text = new_title

if __name__ == '__main__':
	run(MenuScene('Bacalao', "high score: ", ['play Bacalao']))
	
	
	
	
	
	
	
	
	
	
	
	
def cmp(a, b):
	return ((a > b) - (a < b))
	
standing_texture = Texture('IMG_3729.PNG')
walk_textures = [Texture('IMG_3729.PNG'), Texture('IMG_3729.PNG')]
hit_texture = Texture('IMG_3737.PNG')
class Coin (SpriteNode):
	def __init__(self, **kwargs):
		SpriteNode.__init__(self, 'IMG_3730.PNG', **kwargs)

class Meteor (SpriteNode):
	def __init__(self, **kwargs):
		img = random.choice(['IMG_3733.PNG', 'IMG_3734.PNG'])
		SpriteNode.__init__(self, img, **kwargs)

class Bacalao (Scene):
	def setup(self):
		
		self.background_color = '#5e81d9'
		ground = Node(parent=self)
		x = 0
		while x <= self.size.w + 64:
			tile = SpriteNode('plf:Tile_Water', position=(x, 32))
			ground.add_child(tile)
			x += 64
			tile = SpriteNode('plf:Tile_Water', position=(x -50, 96))
			ground.add_child(tile)
			tile = SpriteNode('plf:Tile_Water', position=(x -50, 160))
			ground.add_child(tile)
			top_tile = SpriteNode('plf:Tile_WaterTop_high', position=(x -50, 224))
			ground.add_child(top_tile)
			
		self.player = SpriteNode('IMG_3729.PNG')
		self.player.anchor_point = (0.5, 0.5)
		self.player.position = (self.size.w/2, 110)
		self.player.size = (200, 76)
		self.player.rotation = (-1.57)
		self.add_child(self.player)
		
		score_font = ('Chalkboard SE', 50)
		self.score_label = LabelNode('0', score_font, parent=self)
		self.score_label.position = (self.size.w/11, self.size.h - 30)
		self.score_label.z_position = 1
		self.score = 0
		self.walk_step = -1
		self.items = []
		self.player.size = (200, 76)
		self.new_game()
		
	def new_game(self):
		for item in self.items:
			item.remove_from_parent()
		self.items = []
		self.score = 0
		self.score_label.text = '0'
		self.walk_step = -1
		sound.set_volume(1)
		sound.play_effect('voice:male_go')
		self.player.texture = standing_texture
		self.player.position = (self.size.w/2, 110)
		self.player.size = (200, 76)
		self.speed = 1.0
		self.game_over = False
		
	def update(self):
		if self.game_over:
			return 
			self.player.size = (200, 76)
		self.update_player()
		self.check_item_collisions()
		if random.random() < 0.03 * self.speed:
			self.spawn_item()
			
		if (self.score > 99):
			self.score_label.position = (self.size.w/8.5, self.size.h - 30)
		if (self.score > 999):
			self.score_label.position = (self.size.w/6.5, self.size.h - 30)
		if (self.score > 9999):
			self.score_label.position = (self.size.w/5, self.size.h - 30)
		
	def update_player(self):
		g = gravity()
		if abs(g.x) > 0.02:
			self.player.y_scale = cmp(-g.x, 0)
			x = self.player.position.x
			max_speed = 58
			x = max(0, min(self.size.w, x + g.x * max_speed))
			self.player.position = (x, 110)
			
			step = int(self.player.position.x / 100) % 2
			if step != self.walk_step:
				self.player.texture = walk_textures[step]
				sound.play_effect('game:Woosh_1', 0.05, 1.0 + 0.5 * step)
				self.walk_step = step
		else:
			self.player.texture = standing_texture
			self.walk_step = -1
			
	def check_item_collisions(self):
		player_hitbox = Rect(self.player.position.x - 20, 125, 38, 75)
		for item in list(self.items):
			if item.frame.intersects(player_hitbox):
				if isinstance(item, Coin):
					sound.set_volume(.5)
					self.collect_item(item)
				elif isinstance(item, Meteor):
					sound.set_volume(1)
					self.player_hit()
				elif not item.parent:
					self.items.remove(item)
				
	def player_hit(self):
		self.game_over = True
		sound.play_effect('rpg:KnifeSlice2')
		sound.play_effect('voice:male_game_over')
		self.player.texture = hit_texture
		self.player.size = (80, 230)
		self.speed = 1
		self.player.run_action(A.move_by(0, 610, 1.3))
		self.run_action(A.sequence(A.wait(2*self.speed), A.call(self.new_game)))
		
	def spawn_item(self):
		if random.random() < 0.3:
			meteor = Meteor(parent=self)
			meteor.size = (50, 90)
			meteor.position = (random.uniform(50, self.size.w-70), self.size.h + 70)
			d = random.uniform(2.0, 4.0)
			actions = [A.move_to(random.uniform(0, self.size.w), -100, d), A.remove()]
			meteor.run_action(A.sequence(actions))
			self.items.append(meteor)
		else:
			coin = Coin(parent=self)
			coin.size = (50, 50)
			coin.position = (random.uniform(50, self.size.w-50), self.size.h + 50)
			d = random.uniform(1.50, 4.0)
			actions = [A.move_by(0, -(self.size.h + 60), d), A.remove()]
			coin.run_action(A.sequence(actions))
			self.items.append(coin)
		self.speed = min(3, self.speed + 0.02)
		
	def collect_item(self, item, value = 5):
		sound.play_effect('voice:male_congratulations',)
		item.remove_from_parent()
		self.items.remove(item)
		self.score += value
		self.score_label.text = str(self.score)
			
	
