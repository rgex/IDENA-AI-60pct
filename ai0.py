import random
import numpy as np
import sys
import glob
import json

keywords = {}

# compares the extracted keywords from two images and calculates their similarity
def compareImageKeywords(keywords1, keywords2):
    score = 0
    for keyword1 in keywords1:
        for keyword2 in keywords2:
            if "description" in keyword1 and "description" in keyword2 and keyword1["description"] != None and keyword2["description"] != None:
                if keyword1["description"].lower() == keyword2["description"].lower():
                    if "score" in keyword1 and "score" in keyword2:
                        score += keyword1["score"] * keyword2["score"]
    return score

# calculates the score of a flip
def calculateScore(flipKeywords):
    return compareImageKeywords(flipKeywords[0], flipKeywords[1]) + compareImageKeywords(flipKeywords[1], flipKeywords[2]) + compareImageKeywords(flipKeywords[2], flipKeywords[3])

correct = 0
incorrect = 0
tie = 0

for filename in glob.glob('all-ai/*'):
    flipFile = open(filename)
    flip = json.load(flipFile)

    leftFlip = []
    for order in flip['content']['LeftOrder']:
        if "labelAnnotations" in flip['ai_description'][order][0]:
            leftFlip.append(flip['ai_description'][order][0]['labelAnnotations'])
    
    rightFlip = []
    for order in flip['content']['RightOrder']:
        if "labelAnnotations" in flip['ai_description'][order][0]:
            rightFlip.append(flip['ai_description'][order][0]['labelAnnotations'])
    
    if len(leftFlip) == 4 and len(rightFlip) == 4:
        scoreLeft = calculateScore(leftFlip)
        scoreRight = calculateScore(rightFlip)

        # the flip with the highest score is considered to be the correct one
        if scoreLeft > scoreRight and flip['answer'] == 'Left':
            correct += 1
        elif scoreLeft < scoreRight and flip['answer'] == 'Right':
            correct += 1
        elif scoreLeft > scoreRight and flip['answer'] == 'Right':
            incorrect += 1
        elif scoreLeft < scoreRight and flip['answer'] == 'Left':
            incorrect += 1
        else:
            tie += 1

print("correct: " + str(correct))
print("incorrect: " + str(incorrect))
print("tie: " + str(tie))
print("correct percentage:" + str(((correct + draw/2) / (correct + incorrect + draw)) * 100) + " %")
sys.exit()

