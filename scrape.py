import csv
import PyPDF2 
import os
import collections
import re
regex = r'(TOSS\n-UP)([\s\S]*)(ANSWER)([\s\S]*)(BONUS)([\s\S]*)(ANSWER)([\s\S]*)(TOSS\n-UP)([\s\S]*)(BONUS)([\s\S]*)(ANSWER)([\s\S]*)' #used for set 1
regex2 = r'(TOSS\n-UP)([\s\S]*)(ANSWER)([\s\S]*)(BONUS)([\s\S]*)(ANSWER)([\s\S]*)' #last page
regex3 = r'(TOSS-UP)([\s\S]*)(ANSWER)([\s\S]*)(TOSS-UP)([\s\S]*)(ANSWER)([\s\S]*)'  #used for set 2 and beyond
regex4 = r'(TOSS-UP)([\s\S]*)(ANSWER)([\s\S]*)(BONUS)([\s\S]*)(ANSWER)([\s\S]*)'
regex5 = r'(TOSS\n-UP)([\s\S]*)(ANSWE\nR)([\s\S]*)(BONUS)([\s\S]*)(ANSWER)([\s\S]*)' #SS1 Round17 pg12


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
def returnType(str):
        subjects = [
        'Short Answer',
        'Multiple Choice',
        ]

        for i in range(0, len(subjects)):
                if (subjects[i] in str):
                        return subjects[i]
                else:
                        continue

def returnCAT(str):
        subjects = [
        'CHEMISTRY',
        'BIOLOGY',
        'PHYSICS',
        'MATH',
        'ENERGY',
        'EARTH AND SPACE',
        'ASTRONOMY',
        'EARTH SCIENCE',
        'GENERAL SCIENCE'
        ]

        for i in range(0, len(subjects)):
                if (subjects[i].upper() in str.upper()):
                        return subjects[i]
                else:
                        continue

idNum = 0
def readFile():
        global idNum
        #grab set
        for SetName in os.listdir('./HS-Sample-Questions'):
                if not SetName.startswith('.'):
                        SetNameArr.append(SetName)

        #print(SetNameArr)
        with open('test.csv', 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames = ["ID", "SET", "ROUND", "CAT", "KEY", "TYPE", "Q", "A"])
                writer.writeheader()

                for item in SetNameArr:
                        print('')
                        print('In ' + item + ':')
                                
                        for PDF_FILE in os.listdir('./HS-Sample-Questions/' + item):
                                #print(PDF_FILE)

                                #create PDF File Object for each ROUND PDF
                                pdfFileObj = open('./HS-Sample-Questions/'+item+"/"+PDF_FILE, 'rb')
                                #Create Reader OBJ of PDF File Object
                                pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
                                c = collections.Counter(range(pdfReader.getNumPages()))
                                for i in c:
                                        pageObj = pdfReader.getPage(i)
                                #print(i)
                                        PDFtxt = pageObj.extractText() #grabs individual page 
                                        prog = re.compile(regex)
                                        result = prog.search(PDFtxt)

                                        #try regex2 last page
                                        if (result == None):
                                                #print(PDFtxt)
                                                newProg = re.compile(regex2)
                                                newResult = newProg.search(PDFtxt)

                                                #try regex3
                                                if (newResult == None):
                                                        newnewProg = re.compile(regex3)
                                                        newnewResult = newnewProg.search(PDFtxt)
                                                        #try regex4 <= set2 last page
                                                        if (newnewResult == None):
                                                                newnewnewProg = re.compile(regex4)
                                                                newnewnewResult = newnewnewProg.search(PDFtxt)


                                                                if (newnewnewResult == None):
                                                                        regex5Prog = re.compile(regex5)
                                                                        regex5Result = regex5Prog.search(PDFtxt)
                                                                        if (regex5Result == None):
                                                                                print('could not match {} {} {}'.format(item, PDF_FILE, i))
                                                                        
                                                                        else:
                                                                                print(regex5Result.group(1)) 
                                                                                writer.writerow({'ID': idNum, 'SET': item, 'ROUND': PDF_FILE, "CAT": returnCAT(regex5Result.group(2)), "KEY": regex5Result.group(1), "TYPE": returnType(regex5Result.group(2)), "Q": regex5Result.group(2), "A":regex5Result.group(4) })
                                                                                idNum+=1
                                                                                writer.writerow({'ID': idNum, 'SET': item, 'ROUND': PDF_FILE, "CAT": returnCAT(regex5Result.group(6)), "KEY": regex5Result.group(5), "TYPE": returnType(regex5Result.group(6)), "Q": regex5Result.group(6), "A":regex5Result.group(8) })
                                                                                idNum+=1

                                                                else:
                                                                        writer.writerow({'ID': idNum, 'SET': item, 'ROUND': PDF_FILE, "CAT": returnCAT(newnewnewResult.group(2)), "KEY": newnewnewResult.group(1), "TYPE": returnType(newnewnewResult.group(2)), "Q": newnewnewResult.group(2), "A":newnewnewResult.group(4) })
                                                                        idNum+=1
                                                                        writer.writerow({'ID': idNum, 'SET': item, 'ROUND': PDF_FILE, "CAT": returnCAT(newnewnewResult.group(6)), "KEY": newnewnewResult.group(5), "TYPE": returnType(newnewnewResult.group(6)), "Q": newnewnewResult.group(6), "A":newnewnewResult.group(6) })
                                                        else:
                                                                print(newnewResult.group(1))
                                                                writer.writerow({'ID': idNum, 'SET': item, 'ROUND': PDF_FILE, "CAT": returnCAT(newnewResult.group(2)), "KEY": newnewResult.group(1), "TYPE": returnType(newnewResult.group(2)), "Q": newnewResult.group(2), "A":newnewResult.group(4) })
                                                                idNum+=1
                                                                writer.writerow({'ID': idNum, 'SET': item, 'ROUND': PDF_FILE, "CAT": returnCAT(newnewResult.group(6)), "KEY": newnewResult.group(5), "TYPE": returnType(newnewResult.group(5)), "Q": newnewResult.group(6), "A":newnewResult.group(8) })
                                                                idNum+=1
                                                                
                                                else:
                                                        print(newResult.group(1))
                                                        writer.writerow({'ID': idNum, 'SET': item, 'ROUND': PDF_FILE, "CAT": returnCAT(newResult.group(2)), "KEY": newResult.group(1), "TYPE": returnType(newResult.group(2)), "Q": newResult.group(2), "A":newResult.group(4) })
                                                        idNum+=1
                                                        writer.writerow({'ID': idNum, 'SET': item, 'ROUND': PDF_FILE, "CAT": returnCAT(newResult.group(6)), "KEY": newResult.group(5), "TYPE": returnType(newResult.group(5)), "Q": newResult.group(6), "A":newResult.group(8) })
                                                        idNum+=1
                                        else:
                                                print(result.group(1)) #regex result
                                                
                                                writer.writerow({'ID': idNum, 'SET': item, 'ROUND': PDF_FILE, "CAT": returnCAT(result.group(2)), "KEY": result.group(1), "TYPE": returnType(result.group(2)), "Q": result.group(2), "A":result.group(4) })
                                                idNum+=1
                                                writer.writerow({'ID': idNum, 'SET': item, 'ROUND': PDF_FILE, "CAT": returnCAT(result.group(6)), "KEY": result.group(5), "TYPE": returnType(result.group(6)), "Q": result.group(6), "A":result.group(8) })
                                                idNum+=1
                                                writer.writerow({'ID': idNum, 'SET': item, 'ROUND': PDF_FILE, "CAT": returnCAT(result.group(10)), "KEY": result.group(9), "TYPE": returnType(result.group(10)), "Q": result.group(10), "A":result.group(10) })
                                                idNum+=1
                                                writer.writerow({'ID': idNum, 'SET': item, 'ROUND': PDF_FILE, "CAT": returnCAT(result.group(14)), "KEY": result.group(13), "TYPE": returnType(result.group(14)), "Q": result.group(14), "A":result.group(14) })
                                                idNum+=1
                        pdfFileObj.close() 

readFile()



'''f= open("test.txt","w+")

pdfFileObj = open('./HS-Sample-Questions/SS6/Sample6_ROUND15.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
pageObj = pdfReader.getPage(4)
f.write(pageObj.extractText())
f.close()'''