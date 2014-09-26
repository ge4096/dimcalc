#!/usr/bin/python

import data

# Todo:
# -(3m)
# 19V(3m)
# proper error handling
# Add >
# More non-SI units
# Derived units (e.g N*m)
# calculation tools
# arrow keys in input
# use prefixes in output
# equation solving

global fail

class Measure:
	def __init__(self, value = 0, units = [0, 0, 0, 0, 0, 0, 0]):
		try:
			self.value = float(value)
		except ValueError:
			self.value = 0
			print('Measure value could not be converted to float')
		if len(units) == 7:
			try:
				self.units = [0, 0, 0, 0, 0, 0, 0]
				c = 0
				for x in units:
					self.units[c] = int(x)
					c += 1
			except ValueError:
				self.units = [0, 0, 0, 0, 0, 0, 0]
				print('Measure unit values could not be converted to int')
		else:
			self.units = [0, 0, 0, 0, 0, 0, 0]
			print('Measure unit array of invalid length')
	def format(self):
		try:
			x = str(self.value) + data.vdic[str(self.units)]
		except KeyError:
			if self.value == round(self.value):
				x = str(int(self.value))
			else:
				x = str(self.value)
			ustr = ['m', 'kg', 's', 'A', 'K', 'mol', 'cd']
			for c in range(0, 6):
				if self.units[c] == 0:
					pass
				elif self.units[c] == 1:
					x += '*' + ustr[c]
				else:
					if self.units[c] == int(self.units[c]):
						x += '*' + ustr[c] + '^' + str(int(self.units[c]))
					else:
						x += '*' + ustr[c] + '^' + str(self.units[c])
		return x

def add(x, y):
	z = Measure()
	try:
		if x.units == y.units:
			z.value = x.value + y.value
			z.units = x.units
		else:
			failed()
			print('Dimension mismatch')
	except AttributeError:
		print('Inputs are not valid Measure objects')
	return z

def subt(x, y):
	z = Measure()
	try:
		if x.units == y.units:
			z.value = x.value - y.value
			z.units = x.units
		else:
			failed()
			print('Dimension mismatch')
	except AttributeError:
		print('Inputs are not valid Measure objects')
	return z

def mult(x, y):
	z = Measure()
	try:
		z.value = x.value * y.value
		for c in range(0, 6):
			z.units[c] = x.units[c] + y.units[c]
	except AttributeError:
		print('Inputs are not valid Measure objects')
	return z

def div(x, y):
	z = Measure()
	try:
		z.value = x.value / y.value
		for c in range(0, 6):
			z.units[c] = x.units[c] - y.units[c]
	except AttributeError:
		print('Inputs are not valid Measure objects')
	return z

def pow(x, y):
	z = Measure()
	try:
		z.value = x.value ** y
		for c in range(0, 6):
			z.units[c] = x.units[c] * y
	except AttributeError:
		print('Inputs are not valid Measure objects')
	return z

def failed():
	global fail
	fail = True

def unfail():
	global fail
	fail = False

def parse(x):
	if isinstance(x, Measure):
		return x
	elif isinstance(x, str):
		dec = False
		neg = False
		r = Measure()
		us = ''
		for c in range(0, len(x)):
			if x[c].isdigit():
				pass
			elif x[c] == '.' and not dec:
				dec = True
			elif x[c] == '-' and not neg and (c == 0 or x[c - 1] == 'e'):
				neg = True
			elif x[c].isalpha():
				if x[c] == 'e' and (x[c + 1].isdigit() or x[c + 1] == '-'):
					dec = True
					neg = False
				else:
					if c == 0:
						r.value = 1
						us = x
					else:
						r.value = float(x[:c])
						us = x[c:]
					break
			else:
				print('Illegal character parsed, will ignore')
		if us == '':
			r.value = float(x)
		else:
			try:
				pref = data.predic[us[0]]
				if us[:2] == 'da':
					pref = -1
					us1 = us[2:]
				else:
					us1 = us[1:]
				try:
					r.units = data.udic[us1][:7]
					r.value *= data.udic[us1][7] * (10 ** pref)
				except KeyError:
					pref = 0
					try:
						r.units = data.udic[us][:7]
						r.value *= data.udic[us][7]
					except KeyError:
						print('Units not found, assumed dimensionless')
			except KeyError:
				try:
					r.units = data.udic[us][:7]
					r.value *= data.udic[us][7]
				except KeyError:
					print('Units not found, assumed dimensionless')
		return r

def opsplit(x):
	argar = []
	tstr = ''
	for n in range(0, len(x)):
		if x[n] in '*+-/^()>':
			if tstr != '':
				argar += [tstr]
				tstr = ''
			argar += x[n]
		elif x[n] == ' ':
			pass
		else:
			tstr += x[n]
	if tstr != '':
		argar += [tstr]
	print(argar)
	if '-' in argar:
		if argar[0] == '-':
			argar = ['-' + argar[1]] + argar[2:]
		print(argar)
		for n in range(1, len(argar) - 1):
			if argar[n] == '-':
				if argar[n - 1] in '+-*/(^>':
					argar = argar[:n] + ['-' + argar[n + 1]] + argar[n + 2:]
					print('Shit')
	print(argar)
	return argar

def calc(argar):
	if len(argar) == 1:
		if isinstance(argar[0], Measure):
			return argar[0]
		else:
			try:
				return parse(argar[0])
			except ValueError:
				return Measure()
	else:
		if '(' in argar:
			for n in range(0, len(argar)):
				rn = False
				if argar[n] == ')':
					rn = True
					for n1 in range(n - 1, -1, -1):
						if rn:
							if argar[n1] == '(':
								rn = False
								return calc(argar[:n1] + [calc(argar[n1 + 1:n])] + argar[n + 1:])
					if rn:
						print('Parentheses are unbalanced')
						return Measure()
					break
		elif '^' in argar:
			powin = argar.index('^')
			if isinstance(argar[powin - 1], Measure):
				return calc(argar[:powin - 1] + [pow(argar[powin - 1], argar[powin + 1])] + argar[powin + 2:])
			else:
				powv = Measure()
				ar = parse(argar[powin - 1])
				if ar.units == [0, 0, 0, 0, 0, 0, 0]:
					powv.value = ar.value ** float(argar[powin + 1])
				else:
					powv.value = ar.value
					for c in range(0, 6):
						powv.units[c] = ar.units[c] * float(argar[powin + 1])
				return calc(argar[:powin - 1] + [powv] + argar[powin + 2:])
		elif '*' in argar or '/' in argar:
			if '*' in argar:
				multin = argar.index('*')
			else:
				multin = len(argar) + 1
			if '/' in argar:
				divin = argar.index('/')
			else:
				divin = len(argar) + 1
			if multin < divin:
				return calc(argar[:multin - 1] + [mult(parse(argar[multin - 1]), parse(argar[multin + 1]))] + argar[multin + 2:])
			elif multin > divin:
				return calc(argar[:divin - 1] + [div(parse(argar[divin - 1]), parse(argar[divin + 1]))] + argar[divin + 2:])
		elif '+' in argar or '-' in argar:
			if '+' in argar:
				addin = argar.index('+')
			else:
				addin = len(argar) + 1
			if '-' in argar:
				subin = argar.index('-')
			else:
				subin = len(argar) + 1
			if addin < subin:
				return calc(argar[:addin - 1] + [add(parse(argar[addin - 1]), parse(argar[addin + 1]))] + argar[addin + 2:])
			elif addin > subin:
				return calc(argar[:subin - 1] + [subt(parse(argar[subin - 1]), parse(argar[subin + 1]))] + argar[subin + 2:])
		elif '>' in argar:
			conin = argar.find('>')
			if isinstance(argar[conin - 1], str):
				argar[conin - 1] = parse(argar[conin - 1])
			if isinstance(argar[conin + 1], str):
				argar[conin + 1] = parse(argar[conin + 1])
			if argar[conin - 1].units == argar[conin + 1].units:
				pass

running = True
print('DimCalc v0.0.1')
while running:
	unfail()
	arg = input('> ')
	if arg == 'exit' or arg == 'quit' or arg == 'stop' or arg == 'end':
		running = False
	else:
		#try:
		v = calc(opsplit(arg)).format()
		if not fail:
			print(v)
		#except:
			#print('An error occurred')
