import os,shutil,glob

from os import path


#filename = glob.glob(src_dir, recursive = True)

              
PDF = ['.pdf']
WORD = ['.doc','.docx']
excel = ['.xls','.xlsx']
presentation = ['.ppt','.pptx']
text = ['.txt']

#Location to be moved

PDFLocation = "C:/Users/pinak.mazumdar/Downloads/PDF"
DOCLocation = "C:/Users/pinak.mazumdar/Downloads/DOC"
XLSLocation = "C:/Users/pinak.mazumdar/Downloads/EXCEL"
PPTLocation = "C:/Users/pinak.mazumdar/Downloads/POWERPOINT"
textLocation = "C:/Users/pinak.mazumdar/Downloads/TEXT"

print('Enter a directory to sort: ')           
src_dir = input()

print (f'You have entered {src_dir} for sorting')
filename=glob.glob(src_dir, recursive = True)
for file in filename:
     
 if os.path.splitext(file)[1] in PDF:
           if(path.exists(PDFLocation)):
            shutil.move(file,PDFLocation)
            print('Folder existed,moved files')
           else:
            os.mkdir(PDFLocation)
            shutil.move(file,PDFLocation)
            print('Folder created and moved files')
 if os.path.splitext(file)[1] in WORD:        
            if(path.exists(DOCLocation)):
             shutil.move(file,DOCLocation)
             print('Folder existed,moved files')
            else:
             os.mkdir(DOCLocation)
             shutil.move(file,DOCLocation)
            print('Folder created and moved files')
 if os.path.splitext(file)[1] in excel:           
            if(path.exists(XLSLocation)):
             shutil.move(file,XLSLocation)
             print('Folder existed,moved files')
            else:
             os.mkdir(XLSLocation)
             shutil.move(file,XLSLocation)
            print('Folder created and moved files')
 if os.path.splitext(file)[1] in presentation:
            if(path.exists(PPTLocation)):
             shutil.move(file,PPTLocation)
             print('Folder existed,moved files')
            else:
             os.mkdir(PPTLocation)
             shutil.move(file,PPTLocation)
             print('Folder created and moved files')
            
 if os.path.splitext(file)[1] in text:           
            if(path.exists(textLocation)):
             shutil.move(file,textLocation)
             print('Folder existed,moved files')
            else:
             os.mkdir(textLocation)
             shutil.move(file,textLocation)
             print('Folder created and moved files')
