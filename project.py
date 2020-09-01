import math
import random
import copy
import time

class City:
	def __init__(self, name, x, y):
		self.name = name
		self.x = x
		self.y = y
	
	def equal(self, city):
		return (self.name == city.name and self.x == city.x and self.y == city.y)

	def printInfo(self):
		print(self.name, self.x, self.y)

class Route:
	def __init__(self, cityList):
		self.cityList = copy.deepcopy(cityList)
		self.travelDistance = self.fitnessFunction()
		self.chosenProbability = 0

	# The lower the better
	def fitnessFunction(self):
		travelDistance = 0
		for i in range(1, len(self.cityList)):
			travelDistance += distance(self.cityList[i-1], self.cityList[i])
		travelDistance += distance(self.cityList[len(self.cityList)-1], self.cityList[0])
		return travelDistance

	def shuffleCityList(self):
		random.shuffle(self.cityList)
		self.travelDistance = self.fitnessFunction()

	def mutate(self, mutateProbability):
		probability = random.random()
		if (probability > (1-mutateProbability)):
			randomNumber1 = random.randint(0, len(self.cityList)-1)
			randomNumber2 = randomNumber1
			while (True):
				randomNumber2 = random.randint(0, len(self.cityList)-1)
				if (randomNumber2 != randomNumber1):
					break
			temp = copy.deepcopy(self.cityList[randomNumber1])
			self.cityList[randomNumber1] = copy.deepcopy(self.cityList[randomNumber2])
			self.cityList[randomNumber2] = temp
			self.travelDistance = self.fitnessFunction()

	def printInfo(self):
		for i in range(len(self.cityList)):
			print(self.cityList[i].name, self.cityList[i].x, self.cityList[i].y)
		print(self.travelDistance)
		print(self.chosenProbability)
		print()

class Generation:
	def __init__(self, routeList):
		self.routeList = copy.deepcopy(routeList)
		self.sumTravelDistance, self.bestRoute = self.sumTravelDistanceAndBestRoute()
		self.assignChosenProbbility()
	
	def sumTravelDistanceAndBestRoute(self):
		sum = 0
		bestRoute = copy.deepcopy(self.routeList[0])
		for i in range(len(self.routeList)):
			sum += self.routeList[i].travelDistance
			if (self.routeList[i].travelDistance < bestRoute.travelDistance):
				bestRoute = copy.deepcopy(self.routeList[i])
		return sum, bestRoute
	
	def assignChosenProbbility(self):
		for i in range(len(self.routeList)):
			self.routeList[i].chosenProbability = 1 - (self.routeList[i].travelDistance/self.sumTravelDistance)

def distance(city1, city2):
	return math.sqrt((city1.x-city2.x)**2 + (city1.y-city2.y)**2)

# Population size > 1
def generateFirstGeneration(populationSize, originalRoute):
	routeList = []
	routeList.append(copy.deepcopy(originalRoute))
	for i in range(1, populationSize):
		newRoute = copy.deepcopy(originalRoute)
		newRoute.shuffleCityList()
		routeList.append(newRoute)
	return Generation(routeList)

def randomSelection(generation):
	randomNumber1 = 0
	randomNumber2 = 0
	while (True):
		found = False
		accecptedProbability = random.random()
		for i in range(len(generation.routeList)):
			randomNumber1 = random.randint(0, len(generation.routeList)-1)
			if (generation.routeList[randomNumber1].chosenProbability > accecptedProbability):
				found = True
				break
		if (found is True):
			break

	while (True):
		found = False
		accecptedProbability = random.random()
		for i in range(len(generation.routeList)):
			randomNumber2 = random.randint(0, len(generation.routeList)-1)
			if (generation.routeList[randomNumber2].chosenProbability > accecptedProbability and randomNumber2 != randomNumber1):
				found = True
				break
		if (found is True):
			break

	return copy.deepcopy(generation.routeList[randomNumber1]), copy.deepcopy(generation.routeList[randomNumber2])
	
def pmx(route1, route2):
	cutPoint = random.randint(1, len(route1.cityList)-1)

	cityList1 = copy.deepcopy(route1.cityList)
	i = 0
	while (i < cutPoint):
		for j in range(len(cityList1)):
			if (cityList1[j].equal(route2.cityList[i])):
				cityList1[j] = cityList1[i]
				cityList1[i] = route2.cityList[i]
				break
		i += 1

	cityList2 = copy.deepcopy(route2.cityList)
	i = 0
	while (i < cutPoint):
		for j in range(len(cityList2)):
			if (cityList2[j].equal(route1.cityList[i])):
				cityList2[j] = cityList2[i]
				cityList2[i] = route1.cityList[i]
				break
		i += 1
	
	return Route(cityList1), Route(cityList2)

def reproduce(route1, route2):
	cityList = []
	selectedParent = copy.deepcopy(route1)
	otherParent = copy.deepcopy(route2)

	if (random.random() > 0.5):
		selectedParent = copy.deepcopy(route2)
		otherParent = copy.deepcopy(route1)
	
	cutNumber = int((len(selectedParent.cityList))/2)
	selectedCutPlace = random.randint(0, len(selectedParent.cityList)-cutNumber)

	for i in range(cutNumber):
		cityList.append(copy.deepcopy(selectedParent.cityList[selectedCutPlace+i]))
	
	for i in range(len(otherParent.cityList)):
		contain = False
		for j in range(len(cityList)):
			if (otherParent.cityList[i].equal(cityList[j])):
				contain = True
		if (contain is False):
			cityList.append(copy.deepcopy(otherParent.cityList[i]))

	return Route(cityList)

def findAppendElement(middleCut1, middleCut2, city):
	mappedPosition = 0
	for i in range(len(middleCut1)):
		if (middleCut1[i].equal(city)):
			mappedPosition = i
			break
	mappedCity = copy.deepcopy(middleCut2[mappedPosition])
	contain = False
	for i in range(len(middleCut1)):
		if (middleCut1[i].equal(mappedCity)):
			contain = True
			return findAppendElement(middleCut1, middleCut2, mappedCity)
	if (contain is False):
		return mappedCity
	
def pmx1(route1, route2):
	cutPosition1 = random.randint(0, len(route1.cityList)-3)
	cutPosition2 = random.randint(cutPosition1+1, len(route1.cityList)-2)

	middleCut1 = []
	middleCut2 = []
	for i in range(cutPosition1+1, cutPosition2+1):
		middleCut1.append(copy.deepcopy(route1.cityList[i]))
		middleCut2.append(copy.deepcopy(route2.cityList[i]))

	offspring1 = []
	offspring2 = []
	for i in range(len(route1.cityList)):
		if (i >= cutPosition1+1 and i <= cutPosition2):
			offspring1.append(copy.deepcopy(middleCut2[i-(cutPosition1+1)]))
			offspring2.append(copy.deepcopy(middleCut1[i-(cutPosition2+1)]))
		else:
			contain1 = False
			contain2 = False
			for j in range(len(middleCut1)):
				if (route1.cityList[i].equal(middleCut2[j])):
					contain1 = True

				if (route2.cityList[i].equal(middleCut1[j])):
					contain2 = True

			if (contain1 is False):
				offspring1.append(copy.deepcopy(route1.cityList[i]))
			else:
				appendCity = findAppendElement(middleCut2, middleCut1, route1.cityList[i])
				offspring1.append(appendCity)

			if (contain2 is False):
				offspring2.append(copy.deepcopy(route2.cityList[i]))
			else:
				appendCity = findAppendElement(middleCut1, middleCut2, route2.cityList[i])
				offspring2.append(appendCity)
	return Route(offspring1), Route(offspring2)

def geneticSearchPmxMutate(fileName, populationSize, mutateProbability, allowedTime):
	startTime = time.time()
	originalRoute = Route(fetchData(fileName))
	currentGeneration = generateFirstGeneration(populationSize, originalRoute)
	bestRoute = currentGeneration.bestRoute
	generationCounter = 0
	print("\n------------------------------------------------------------------------------------")
	print("Running Genetic Search Using PMX And Mutation...")
	print("Generation", generationCounter)
	print("Shortest route found is:", bestRoute.travelDistance)
	elapsedTime = time.time() - startTime
	print("Runtime:", elapsedTime)
	
	while (True):
		generationCounter += 1
		print("\n------------------------------------------------------------------------------------")
		print("Running Genetic Search Using PMX And Mutation...")
		print("Generation", generationCounter)
		routeList = []
		for i in range(int(populationSize/2)):
			route1, route2 = randomSelection(currentGeneration)
			newRoute1, newRoute2 = pmx(route1, route2)
			newRoute1.mutate(mutateProbability)
			newRoute2.mutate(mutateProbability)
			routeList.append(newRoute1)
			routeList.append(newRoute2)
		currentGeneration = Generation(routeList)
		if (currentGeneration.bestRoute.travelDistance < bestRoute.travelDistance):
			bestRoute = copy.deepcopy(currentGeneration.bestRoute)
		elapsedTime = time.time() - startTime
		print("Shortest route found is:", bestRoute.travelDistance)
		print("Runtime:", elapsedTime)
		if (elapsedTime > allowedTime):
			print("\n------------------------------------------------------------------------------------")
			print("Timeout!")
			print("Population Size:", populationSize)
			print("Mutate Probability", mutateProbability)
			print("Estimated Allowed Time:", allowedTime)
			print("Shortest route found is:", bestRoute.travelDistance)
			return bestRoute

def geneticSearchReproduceMutate(fileName, populationSize, mutateProbability, allowedTime):
	startTime = time.time()
	originalRoute = Route(fetchData(fileName))
	currentGeneration = generateFirstGeneration(populationSize, originalRoute)
	bestRoute = currentGeneration.bestRoute
	generationCounter = 0
	print("\n------------------------------------------------------------------------------------")
	print("Running Genetic Search Using Reproduce And Mutation...")
	print("Generation", generationCounter)
	print("Shortest route found is:", bestRoute.travelDistance)
	elapsedTime = time.time() - startTime
	print("Runtime:", elapsedTime)

	while (True):
		generationCounter += 1
		print("\n------------------------------------------------------------------------------------")
		print("Running Genetic Search Using Reproduce And Mutation...")
		print("Generation", generationCounter)
		routeList = []
		for i in range(int(populationSize)):
			route1, route2 = randomSelection(currentGeneration)
			newRoute = reproduce(route1, route2)
			if (newRoute.travelDistance < bestRoute.travelDistance):
				routeList.append(newRoute)
			else:
				newRoute.mutate(mutateProbability)
				routeList.append(newRoute)
		currentGeneration = Generation(routeList)
		if (currentGeneration.bestRoute.travelDistance < bestRoute.travelDistance):
			bestRoute = copy.deepcopy(currentGeneration.bestRoute)
		elapsedTime = time.time() - startTime
		print("Shortest route found is:", bestRoute.travelDistance)
		print("Runtime:", elapsedTime)
		if (elapsedTime > allowedTime):
			print("\n------------------------------------------------------------------------------------")
			print("Timeout!")
			print("Population Size:", populationSize)
			print("Mutate Probability", mutateProbability)
			print("Estimated Allowed Time:", allowedTime)
			print("Shortest route found is:", bestRoute.travelDistance)
			return bestRoute

def geneticSearchPmx1Mutate(fileName, populationSize, mutateProbability, allowedTime):
	startTime = time.time()
	originalRoute = Route(fetchData(fileName))
	currentGeneration = generateFirstGeneration(populationSize, originalRoute)
	bestRoute = currentGeneration.bestRoute
	generationCounter = 0
	print("\n------------------------------------------------------------------------------------")
	print("Running Genetic Search Using PMX1 And Mutation...")
	print("Generation", generationCounter)
	print("Shortest route found is:", bestRoute.travelDistance)
	elapsedTime = time.time() - startTime
	print("Runtime:", elapsedTime)
	
	while (True):
		generationCounter += 1
		print("\n------------------------------------------------------------------------------------")
		print("Running Genetic Search Using PMX1 And Mutation...")
		print("Generation", generationCounter)
		routeList = []
		for i in range(int(populationSize/2)):
			route1, route2 = randomSelection(currentGeneration)
			newRoute1, newRoute2 = pmx1(route1, route2)
			newRoute1.mutate(mutateProbability)
			newRoute2.mutate(mutateProbability)
			routeList.append(newRoute1)
			routeList.append(newRoute2)
		currentGeneration = Generation(routeList)
		if (currentGeneration.bestRoute.travelDistance < bestRoute.travelDistance):
			bestRoute = copy.deepcopy(currentGeneration.bestRoute)
		elapsedTime = time.time() - startTime
		print("Shortest route found is:", bestRoute.travelDistance)
		print("Runtime:", elapsedTime)
		if (elapsedTime > allowedTime):
			print("\n------------------------------------------------------------------------------------")
			print("Timeout!")
			print("Population Size:", populationSize)
			print("Mutate Probability", mutateProbability)
			print("Estimated Allowed Time:", allowedTime)
			print("Shortest route found is:", bestRoute.travelDistance)
			return bestRoute

def geneticMutateSearch(fileName, populationSize, mutateProbability, allowedTime):
	startTime = time.time()
	originalRoute = Route(fetchData(fileName))
	currentGeneration = generateFirstGeneration(populationSize, originalRoute)
	bestRoute = currentGeneration.bestRoute
	generationCounter = 0
	print("\n------------------------------------------------------------------------------------")
	print("Running Genetic Search Using Mutate Search...")
	print("Generation", generationCounter)
	print("Shortest route found is:", bestRoute.travelDistance)
	elapsedTime = time.time() - startTime
	print("Runtime:", elapsedTime)
	
	while (True):
		generationCounter += 1
		print("\n------------------------------------------------------------------------------------")
		print("Running Genetic Search Using Mutate Search...")
		print("Generation", generationCounter)
		routeList = []
		for i in range(int(populationSize)):
			newRoute = copy.deepcopy(currentGeneration.bestRoute)
			newRoute.mutate(mutateProbability)
			routeList.append(newRoute)
		currentGeneration = Generation(routeList)
		if (currentGeneration.bestRoute.travelDistance < bestRoute.travelDistance):
			bestRoute = copy.deepcopy(currentGeneration.bestRoute)
		elapsedTime = time.time() - startTime
		print("Shortest route found is:", bestRoute.travelDistance)
		print("Runtime:", elapsedTime)
		if (elapsedTime > allowedTime):
			print("\n------------------------------------------------------------------------------------")
			print("Timeout!")
			print("Population Size:", populationSize)
			print("Mutate Probability", mutateProbability)
			print("Estimated Allowed Time:", allowedTime)
			print("Shortest route found is:", bestRoute.travelDistance)
			return bestRoute

def fetchData(inputFile):
	cityList = []
	file = open(inputFile, 'r')
	for line in file:
		if (str(line).strip()):
			tokens = line.split()
			cityList.append(City(tokens[0], float(tokens[1]), float(tokens[2])))
	return cityList

def writeToFile(bestRoute, filename):
	file = open(filename, "w")
	for i in range(len(bestRoute.cityList)):
		cityInfo = bestRoute.cityList[i].name + " "
		file.write(cityInfo)
	file.close()

def checkGoodPerm(fileName):
	file = open(fileName, 'r')
	line = file.readline()
	tokens = line.split()
	arr = []
	for i in range(len(tokens)):
		arr.append(tokens[i])
	arr.sort()
	res = all(i < j for i, j in zip(arr, arr[1:]))
	print("Good permutaion?: " + str(res) + str("\n"))

def test():
	print("\n------------------------------------------------------------------------------------")
	file = "citiesTest.txt"
	mutateProbability = 0.5
	cityList = fetchData(file)
	route = Route(cityList)
	route.printInfo()

	print("\n------------------------------------------------------------------------------------")
	route.mutate(mutateProbability)
	route.printInfo()

	print("\n------------------------------------------------------------------------------------")
	route.shuffleCityList()
	route.printInfo()

	print("\n------------------------------------------------------------------------------------")
	route = Route(cityList)
	generation0 = generateFirstGeneration(5, route)
	for i in range(len(generation0.routeList)):
		generation0.routeList[i].printInfo()
	print(generation0.sumTravelDistance)
	print()

	print("\n------------------------------------------------------------------------------------")
	route1, route2 = randomSelection(generation0)
	route1.printInfo()
	route2.printInfo()

	print("\n------------------------------------------------------------------------------------")
	first, second = pmx(route1, route2)
	first.printInfo()
	second.printInfo()

	print("\n------------------------------------------------------------------------------------")
	offspring1, offspring2 = pmx1(route1, route2)
	offspring1.printInfo()
	offspring2.printInfo()

def run():
	file = "cities1000.txt"
	populationSize = 100
	mutateProbability = 0.8
	estimatedAllowedTime = 3600

	bestRoute1 = geneticSearchPmxMutate(file, populationSize, mutateProbability, estimatedAllowedTime)
	writeToFile(bestRoute1, "pmxMutate.txt")
	checkGoodPerm("pmxMutate.txt")
	# bestRoute2 = geneticSearchReproduceMutate(file, populationSize, mutateProbability, estimatedAllowedTime)
	# writeToFile(bestRoute2, "reproduceMutate.txt")
	# checkGoodPerm( "reproduceMutate.txt")
	# bestRoute3 = geneticSearchPmx1Mutate(file, populationSize, mutateProbability, estimatedAllowedTime)
	# writeToFile(bestRoute3, "pmx1Mutate.txt")
	# checkGoodPerm("pmx1Mutate.txt")
	# bestRoute4 = geneticMutateSearch(file, populationSize, mutateProbability, estimatedAllowedTime)
	# writeToFile(bestRoute4, "mutateSearch.txt")
	# checkGoodPerm("mutateSearch.txt")

# test()
run()