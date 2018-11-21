def decor_cond(condition_function):
	print('new decor')
	def decor(function):
		print('decor in decor')
		def wrapper(x):
			if condition_function():
				function(x)
			else:
				print("You can't")
		return lambda x: None
	return decor

class info:
	var = True 

@decor_cond(lambda: info.var)
def function(x):
	print(x)

x = 'q'

function(x)
info.var = False
function(x)
