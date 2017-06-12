import sys
import re

def getLineData(line):
	line = line.split(';')[0]
	parts = line.split(' = ')
	return parts[0], parts[1].rstrip()

def getKinetics(line):
	name, expression = getLineData(line)
	return [name, "(" + expression + ")"]

def getAssignment(line):
	return list(getLineData(line))

def improveExpressionReadability(expression):
	expression = expression.split("+")
	expression = " + ".join(expression)

	expression = expression.split("-")
	expression = " + ".join(expression)
	return expression

def getEquation(line):
	name, expression = getLineData(line)
	return name[5:-1] + " = " + improveExpressionReadability(expression)

def replaceEquations(equation, kinetics):
	for kinet in kinetics:
		equation = equation.replace(kinet[0], kinet[1])
	return equation

def replaceODEs(equations, kinetics):
	return map(lambda equation: replaceEquations(equation, kinetics), equations)

"""
Print output
"""
def nicePrint(equations, assignments):
	print "Ordinary differential equations:" + "\n" + "_" * 80 + "\n"
	for ODE in equations:
		print ODE + "\n"
	print "\n" + "_" * 80
	print "Associated assignments:" + "\n"
	for assignment in assignments:
		print assignment[0] + " = " + assignment[1]

input_file = sys.argv[-1]
file = open(input_file, "r")

assignments, kinetics, equations = [], [], []

for line in file:
	if re.search("assignment", line):
		assignments.append(getAssignment(line.rstrip().replace("\"", "")))
	elif re.search("kinetic function", line):
		kinetics.append(getKinetics(line.rstrip().replace("\"", "")))
	elif re.search("d/dt", line):
		equations.append(getEquation(line.rstrip().replace("\"", "")))
		
equations = replaceODEs(equations, kinetics)
nicePrint(equations, assignments)