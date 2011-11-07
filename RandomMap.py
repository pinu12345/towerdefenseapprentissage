from numpy import *
from numpy.random import *
from Global import *
import copy

class RandomMap:
	
	def __init__(self, idim = 0, jdim = 0, comp = -1, len = 0, empl = 0, prox = 0):
		#  idim*jdim  dimensions            min 3*3, max 24*16
		#  len        longueur du chemin    min 2, max variable
		#  comp       complexite du chemin  min 0, max 1, mieux bas
		#  empl       emplacements de to.   min 1, max variable
		#  prox       proximite au chemin   min 1, max a determiner
		
		# Verification des parametres d'entree
		idim_min = 3
		idim_max = 16
		idim_rec = idim_max
		jdim_min = 3
		jdim_max = 24
		jdim_rec = jdim_max
		if idim < idim_min or idim > idim_max:
			idim = idim_rec
		if jdim < jdim_min or jdim > jdim_max:
			jdim = jdim_rec
		
		comp_min = 0
		comp_max = 1
		comp_rec = .2
		if comp < comp_min or comp > comp_max:
			comp = comp_rec
			
		len_min = 2
		len_max = max(2, (idim-1) * (jdim-1) / 3)
		len_rec = len_max / (1 + 2*rand()) / (1 + comp)
		if len < len_min or len > len_max:
			len = len_rec
		
		empl_min = 1
		empl_max = idim*jdim - len - 1
		empl_rec = int(min(empl_max*.8, empl_max**(rand()*rand()) \
			+ 20*rand() + 20*rand()))
		if empl < empl_min or empl > empl_max:
			empl = empl_rec
		
		prox_min = 1
		prox_max = 5 # a determiner
		prox_rec = 1 + randint(prox_max)
		if prox < prox_min or prox > prox_max:
			prox = prox_rec
		
		print "\n empl:", empl, "\n prox:", prox
		
		# Caracteres de la carte
		empty, path, turret, base = \
			car_empty, car_path, car_turret, car_base
		
		# Points cardinaux
		N, S, W, E = cardN, cardS, cardW, cardE
		
		# Production en serie de cartes
		unsatisfying_map = 1
		
		while unsatisfying_map:
		
			# initialise la carte avec '-' partout
			self.M = [[empty] * jdim for i in range(idim)]
			M = self.M
			
			# initialise une tuile
			c = map_current_tile(0, 0)
			
			# trouve un endroit en bordure au hasard
			# c.i et c.j notent les coordonnees
			# dir note vers ou on etend le chemin
			# le chemin des ennemis est note 'X' (car_path)
			if randint(2): # au nord ou au sud
				c.j = randint(1, jdim-1)
				if randint(2): # nord
					c.i = 0
					dir = S
				else: # sud
					c.i = idim-1
					dir = N
			else:
				c.i = randint(1, idim-1)
				if randint(2): # ouest
					c.j = 0
					dir = E
				else: # est
					c.j = jdim-1
					dir = W
			
			# commence le chemin
			M[c.i][c.j] = path
			
			# compte la longueur du chemin actuel
			len_cur = 1
			
			keep_pathing = 1
			while keep_pathing:
				
				## on ajoute une case au chemin
				c.incr(dir)
				M[c.i][c.j] = path
				len_cur += 1
				if len_cur > len:
					break
				
				## on trouve quelles directions sont valides
				dir_valid = zeros(4)
				for dir_next in range(4): # chaque direction possible
					c_next = copy.deepcopy(c) # prochaine case potentielle
					c_next.incr(dir_next)
					if not_opposite_dir(dir, dir_next) \
						and c_next.not_at_border(idim, jdim): # ni oppose, ni au bord
						dir_valid[dir_next] = 1
						for dir_next2 in range(4): # autour de case potentielle
							c_next2 = copy.deepcopy(c_next)
							c_next2.incr(dir_next2)
							if not_opposite_dir(dir_next, dir_next2): # pas oppose
								if M[c_next2.i][c_next2.j] == path: # chemin
									dir_valid[dir_next] = 0
				
				## si au moins une direction est valide,
				## on en choisit une au hasard (biaise par les parametres)
				sum_dir = sum(dir_valid)
				if sum_dir:
					if sum_dir == 1: # juste une direction possible
						dir = argmax(dir_valid)
					elif dir_valid[dir]: # on peut continuer tout droit
						if rand() > comp:
							pass # on garde la meme direction
						else:
							dir_valid[dir] = 0
							if sum(dir_valid) == 1: # une seule autre option
								dir = argmax(dir_valid)
							else:						
								looking_for_dir = 1
								while looking_for_dir:
									dir = randint(4)
									if dir_valid[dir]:
										looking_for_dir = 0
					else: # on choisit entre gauche et droite
						looking_for_dir = 1
						while looking_for_dir:
							dir = randint(4)
							if dir_valid[dir]:
								looking_for_dir = 0
				else:
					keep_pathing = 0
				
				#dir_prob = array([icur, idim, idim+jcur, idim+jdim])
				
			M[c.i][c.j] = base
			
			# si la carte est satisfaisante, on arrete
			if len_cur > len:
				unsatisfying_map = 0
		
		
		# On assigne les emplacements de tourelles
		# empl: emplacements totaux
		# prox: distance minimale du chemin
		cur_empl = 0
		fail_empl = 0
		
		while cur_empl < empl and fail_empl < 100*idim*jdim:
			iemp, jemp = randint(idim), randint(jdim)
			if M[iemp][jemp] == empty:
				# on verifie la distance au chemin
				close_enough = 0
				for i in range(max(0, iemp-prox), min(idim, iemp+prox+1)):
					for j in range(max(0, jemp-prox), min(jdim, jemp+prox+1)):
						if M[i][j] == path and dist_pyth(i, j, iemp, jemp) <= prox:
							close_enough = 1
							break
					if close_enough:
						break
				if close_enough:
					M[iemp][jemp] = turret
					cur_empl += 1
				else:
					fail_empl += 1
			else:
				fail_empl += 1
		
	
	def print_in_console(self):
		# pour voir la carte
		print
		for i in range(len(self.M)):
			print " ",
			for j in range(len(self.M[i])):
				print self.M[i][j],
			print
			
def not_opposite_dir(dir1, dir2):
	sum_dir = dir1 + dir2
	if sum_dir == 1 or sum_dir == 5:
		return 0
	else:
		return 1
		
def dist_pyth(x1, y1, x2, y2):
	return sqrt((x2-x1)**2 + (y2-y1)**2)
    
class map_current_tile:
	
	# Points cardinaux
	N, S, W, E = 0, 1, 2, 3
		
	def __init__(self, i, j):
		self.i, self.j = i, j
		
	def incr(self, dir):
		if dir == self.N:
			self.i -= 1
		elif dir == self.S:
			self.i += 1
		elif dir == self.W:
			self.j -= 1
		elif dir == self.E:
			self.j += 1
			
	def copy(self):
		return map_current_tile(self.i, self.j)
		
	def not_at_border(self, idim, jdim):
		if self.i == 0 \
			or self.i == idim-1 \
			or self.j == 0 \
			or self.j == jdim-1:
			return 0
		else:
			return 1