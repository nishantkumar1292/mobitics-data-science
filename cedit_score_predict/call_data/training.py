import csv
import random
import math
import json

def loadCsv(filename):
	lines = csv.reader(open(filename, "rb"))
	dataset = list(lines)
	dataset.pop(0)
	transformed_dataset = convert_string_to_int(dataset)
	for i in range(len(transformed_dataset)):
		transformed_dataset[i].pop(-2) #removing remark column
		transformed_dataset[i].pop(0) #removing cust_id
		transformed_dataset[i] = [float(x) for x in transformed_dataset[i]]
	return transformed_dataset

def splitDataset(dataset, splitRatio):
	trainSize = int(len(dataset) * splitRatio)
	trainSet = []
	copy = list(dataset)
	while len(trainSet)<trainSize:
		index = random.randrange(len(copy))
		trainSet.append(copy.pop(index))
	return [trainSet, copy]

def seperateByClass(dataset):
	seperated = {}
	for i in range(len(dataset)):
		vector = dataset[i]
		if vector[-1] not in seperated:
			seperated[vector[-1]] = []
		seperated[vector[-1]].append(vector)
	return seperated

def mean(numbers):
	return sum(numbers)/float(len(numbers))

def stdev(numbers):
	avg = mean(numbers)
	variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
	return math.sqrt(variance)

def summarize(dataset):
	summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataset)]
	del summaries[-1]
	return summaries

def summarizeByClass(dataset):
	separated = seperateByClass(dataset)
	summaries = {}
	for classValue, instances in separated.iteritems():
		summaries[classValue] = summarize(instances)
	return summaries

def calculateProbablity(x, mean, stdev):
	exponent = math.exp(-(math.pow(x-mean,2))/(2*math.pow(stdev,2)))
	return (1/(math.sqrt(2*math.pi)*stdev))*exponent

def calculateClassProbablities(summaries, inputVector):
	probablities = {}
	for classValue, classSummaries in summaries.iteritems():
		probablities[classValue] = 1
		for i in range(len(classSummaries)):
			mean, stdev = classSummaries[i]
			x = inputVector[i]
			probablities[classValue] *= calculateProbablity(x, mean, stdev)
	return probablities

def predict(summaries, inputVector):
	probablities = calculateClassProbablities(summaries, inputVector)
	bestLabel, bestProb = None, -1
	for classValue, probablity in probablities.iteritems():
		if bestLabel is None or probablity > bestProb:
			bestProb = probablity
			bestLabel = classValue
	return bestLabel

def getPredictions(summaries, testSet):
	predictions = []
	for i in range(len(testSet)):
		result = predict(summaries, testSet[i])
        print "result"
        print result
        predictions.append(result)
	return predictions

def getAccuracy(testSet, predictions):
	correct = 0
	for i in range(len(testSet)):
		if testSet[i][-1] == predictions[i]:
			correct += 1
	return (correct/float(len(testSet)))*100

def convert_string_to_int(dataset):
	for row in dataset:
		row.append(1) if row[-1]=='GOOD' else row.append(0)
	return dataset

def save_model(summaries):
    filename = 'data/output.json'
    with open(filename, "w") as out:
        json.dump(summaries, out)


def main():
	filename = 'data/call_distribution.csv'
	splitRatio = 0.8
	dataset = loadCsv(filename)
	trainingSet, testSet = splitDataset(dataset, splitRatio)
	print('Split {0} rows into train={1} and test={2} rows').format(len(dataset), len(trainingSet), len(testSet))
	# #prepare model
	summaries = summarizeByClass(trainingSet)
	save_model(summaries)
    print('output saved to data/output')
    predictions = getPredictions(summaries, testSet)
    # #print predictions
    # accuracy = getAccuracy(testSet, predictions)
    # print('Accuracy: {0}%').format(accuracy)
main()
