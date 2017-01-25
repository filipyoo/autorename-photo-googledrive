# Script to download the last updated pictures on Google Drive, 
# and rename them if Exif data is available, if not, keep their original name.

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import datetime, time

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.

drive = GoogleDrive(gauth)

newFileUploadedFolder     = "newFileUploaded\\"
newFileUploadNoExifFolder = "newFileUploadNoExif\\"

# In order not to be asked to accept the user request of google each time the program is executed, 
# several parameters are set in settings.yaml, which create the credentials.txt file to store informations. 



def downloadFile(destinationFolder, file):
    filePic = drive.CreateFile({'id':file['id']})
    filePic.GetContentFile(destinationFolder + file['title'])

def renameFileWithExif(file):
    pictureName = file['imageMediaMetadata']['date']
    pictureName = pictureName.replace(":", "").replace(" ", "_")
    file['title']  = pictureName+".jpg"
    file.Upload()

def getCreatedDateOfFile(file):
    fileCreatedDate = file['createdDate']
    fileCreatedDate, head, tail = fileCreatedDate.partition(".")
    fileCreatedDate = fileCreatedDate.replace(":", "").replace("-", "").replace("T","")
    return fileCreatedDate

# Recursion from the root (MyDrive main folder) through others folder by using their ID, 'root' is the main MyDrive folder.
def ListFolder(parent):
    file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % parent}).GetList()
    for f in file_list:
        if f['mimeType']=='image/jpeg':
            if int(getCreatedDateOfFile(f)) < int(lastUploadedTime):
                pass
            else:
                try:
                    renameFileWithExif(f)
                    downloadFile(newFileUploadedFolder, f)
                    print("Downloading new uploaded files with EXIF...")
                    print (f['title'])
                except Exception:
                    print("Downloading new uploaded files with NO EXIF...")
                    downloadFile(newFileUploadNoExifFolder, f)
                    print (f['title'])

        if f['mimeType']=='application/vnd.google-apps.folder':     #if folder
            ListFolder(f['id'])



lastUploadedTime = open("lastUploadedTime.txt", "r").read()
ListFolder('root')
lastUploadedTime = open("lastUploadedTime.txt", "w").write(time.strftime("%Y%m%d%H%M%S", time.gmtime()))
print("\n================ DONE ================\n")
print("New files downloaded, last update: " + open("lastUploadedTime.txt","r").read())

finish = input("Quit? y (yes)\n")
if finish == "y":
	pass