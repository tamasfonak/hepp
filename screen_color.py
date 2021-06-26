from blessed import Terminal


term = Terminal()
height, width = term.height, term.width

def color(color):
	
	if color == "red":
		space = term.on_red(' ')
		print("Red")
	elif color == "green":
		space = term.on_green(' ')
		print("Green")
	"""for i in range(height-2):
		for j in range (width):
			with term.location(j, i):
				print(space)"""
