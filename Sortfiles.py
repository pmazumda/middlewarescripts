import os,glob,shutil,sys,logging,datetime
from os import path
from pathlib import Path

#filename = glob.glob(src_dir, recursive = True)

    

PDF = ['.pdf']
WORD = ['.doc','.docx']
excel = ['.xls','.xlsx']
presentation = ['.ppt','.pptx']
text = ['.txt']
media = ['.jpeg','.jpg','.bmp','.png','.gif','.mp4','.mp3','.avi']
archive = ['.zip','.tar','.gz','.gzip','.7z','.war','.ear','.jar']
#Location to be moved

PDFLocation = "C:/Users/pinak.mazumdar/Downloads/NEW/PDF"
DOCLocation = "C:/Users/pinak.mazumdar/Downloads/NEW/DOC"
XLSLocation = "C:/Users/pinak.mazumdar/Downloads/NEW/EXCEL"
PPTLocation = "C:/Users/pinak.mazumdar/Downloads/NEW/POWERPOINT"
textLocation = "C:/Users/pinak.mazumdar/Downloads/NEW/TEXT"
mediaLocation = "C:/Users/pinak.mazumdar/Downloads/NEW/MEDIA"
archiveLocation = "C:/Users/pinak.mazumdar/Downloads/NEW/ARCHIVE"

    

#Indexfile = Path('PDFLocation' / 'index.txt')
#Indexfile.close()

print('Enter a directory to sort: ')           
src_dir = input()

#src_dir = 'D:\J2EE-PORTAL- can be deleted\JEECOE DOCS'
print (f'You have entered {src_dir} for sorting \n')
listoffiles = glob.glob(src_dir , recursive = False)
for file in listoffiles:
 print(file)
 if os.path.splitext(file)[1] in PDF:
           if(path.exists(PDFLocation)):
               try:
                   
                   Indexfile = open('index.txt','a+')
                   Indexfile.write(file + '\n')
                   shutil.move(file,PDFLocation)
                   
               except OSError:
                   shutil.copy(file,PDFLocation)
                   
                   print('Folder existed,moved files')
           else:
            os.mkdir(PDFLocation)
            Indexfile = open('index.txt','a+')
              
            Indexfile.write(file + '\n')
            shutil.move(file,PDFLocation)
            print('Folder created and moved files')
 if os.path.splitext(file)[1] in WORD:        
            if(path.exists(DOCLocation)):
             try:
                   Indexfile = open('index.txt','a+')
                   Indexfile.write(file + '\n')
                   shutil.move(file,DOCLocation)
                  
             except OSError:
                   shutil.copy(file,DOCLocation)
                   print('Folder existed,moved files')
            else:
             os.mkdir(DOCLocation)
             Indexfile = open('index.txt','a+')
               
             Indexfile.write(file + '\n')
             shutil.move(Path(src_dir,file),Path(DOCLocation,file))
             print('Folder created and moved files')
 if os.path.splitext(file)[1] in excel:           
            if(path.exists(XLSLocation)):
             try:
                   Indexfile = open('index.txt','a+')
                   Indexfile.write(file + '\n')
                   shutil.move(file,XLSLocation)
             except OSError:
                   shutil.copy(file,XLSLocation)
                   print('Folder existed,moved files')
            else:
             os.mkdir(XLSLocation)
             Indexfile = open('index.txt','a+')
               
             Indexfile.write(file + '\n')
             shutil.move(file,XLSLocation)
             print('Folder created and moved files')
 if os.path.splitext(file)[1] in presentation:
            if(path.exists(PPTLocation)):
             try:
                   Indexfile = open('index.txt','a+')
                   Indexfile.write(file + '\n')
                   shutil.move(file,PPTLocation)
             except OSError:
                   shutil.copy(file,PPTLocation)
                   print('Folder existed,moved files')
            else:
             os.mkdir(PPTLocation)
             Indexfile = open('index.txt','a+')
               
             Indexfile.write(file + '\n')
             shutil.move(file,PPTLocation)
             print('Folder created and moved files')
            
 if os.path.splitext(file)[1] in text:           
            if(path.exists(textLocation)):
             try:
                   Indexfile = open('index.txt','a+')
                   Indexfile.write(file + '\n')
                   shutil.move(file,textLocation)
             except OSError:
                   shutil.copy(file,textLocation)
                   print('Folder existed,moved files')
            else:
             os.mkdir(textLocation)
             Indexfile = open('index.txt','a+')
               
             Indexfile.write(file + '\n')
             shutil.move(file,textLocation)
             print('Folder created and moved files')
 if os.path.splitext(file)[1] in media:           
            if(path.exists(mediaLocation)):
             try:
                   Indexfile = open('index.txt','a+')
                   Indexfile.write(file + '\n')
                   shutil.move(file,mediaLocation)
             except OSError:
                   shutil.copy(file,mediaLocation)
                   print('Folder existed,moved files')
            else:
             os.mkdir(mediaLocation)
             shutil.move(file,mediaLocation)
             print('Folder created and moved files')
 if os.path.splitext(file)[1] in archive:           
            if(path.exists(archiveLocation)):
             try:
                   Indexfile = open('index.txt','a+')
                   Indexfile.write(file + '\n')
                   shutil.move(file,archiveLocation)
             except OSError:
                   print ('A file with the same name already exists in  the destination folder,select appropriate action.\n 1.Replace.\n 2.Rename and Copy. ')
                   choice = input()
                   if choice == '1':
                       shutil.copy(file,archiveLocation)
                       print('Files copied')
                   elif choice == '2':
                       print ('Renaming files with current date')
                       x = datetime.datetime.now()
                       #file= 'abc'
                       absWorkingDir = os.path.abspath(src_dir)
                       newfile = os.path.join(absWorkingDir, str(os.rename(file,os.path.splitext(file)[0]+x.strftime("%d%m%Y")+os.path.splitext(file)[1])))
                       print(newfile)
                       #renamedfile = os.rename(file,newfile)
                                        
                       #shutil.move(renamedfile,archiveLocation)
                       
                       shutil.move(newfile,archiveLocation)
            else:
             os.mkdir(archiveLocation)
             shutil.move(file,archiveLocation)
             print('Folder created and moved files')
