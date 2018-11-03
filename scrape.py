import csv
import os

SetNameArr = [ ] #Question Sets

def createCSV(name):
    with open(name+'.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = ["ID", "SET", "ROUND", "CAT", "KEY", "TYPE", "Q", "A"])
        '''
        ID :  unique ID # for each questions
        SET : Each question belongs to their respective set number. There are 9 sets in total.
        ROUND : Each SET has rounds. Questions belong to their respective ROUND #
        CAT : Questions belong to their corresponding category
        KEY : Toss-Up or BONUS question
        TYPE :  Short Answer or Multiple Choice
        Q : the question
        A : the answer
        '''
        writer.writeheader()

#createCSV('ScienceBOWL') file already exist. Uncomment to create CSV File


def readFile():
        #grab set
        for SetName in os.listdir('./HS-Sample-Questions'):
                if not SetName.startswith('.'):
                        SetNameArr.append(SetName)

        #print(SetNameArr)
        for item in SetNameArr:
                print('')
                print('In ' + item + ':')
                for PDF_FILE in os.listdir('./HS-Sample-Questions/' + item):
                        print(PDF_FILE)


readFile()