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

                                #try regex2
                                if (result == None):
                                        #print(PDFtxt)
                                        newProg = re.compile(regex2)
                                        newResult = newProg.search(PDFtxt)

                                        #try regex3
                                        if (newResult == None):
                                                newnewProg = re.compile(regex3)
                                                newnewResult = newnewProg.search(PDFtxt)
                                                #try regex4
                                                if (newnewResult == None):
                                                        newnewnewProg = re.compile(regex4)
                                                        newnewnewResult = newnewnewProg.search(PDFtxt)
                                                        if (newnewnewResult == None):
                                                                print('could not match {} {} {}'.format(item, PDF_FILE, i))
                                                                regex5Prog = re.compile(regex5)
                                                                regex5Result = regex5Prog.search(PDFtxt)
                                                                if (regex5Result == None):
                                                                       print('could not match {} {} {}'.format(item, PDF_FILE, i))
                                                                else:
                                                                        print(regex5Result.group(2)) 
                                                        else:
                                                               print(newnewnewResult.group(2))
                                                else:
                                                        print(newnewResult.group(2))
                                        else:
                                                print(newResult.group(2))
                                else:
                                       print(result.group(2)) #regex result
                                
                pdfFileObj.close() 

readFile()



'''f= open("test.txt","w+")

pdfFileObj = open('./HS-Sample-Questions/SS6/Sample6_ROUND15.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
pageObj = pdfReader.getPage(4)
f.write(pageObj.extractText())
f.close()'''