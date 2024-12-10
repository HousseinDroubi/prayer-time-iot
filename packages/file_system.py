import os

INFO_FILE_PATH = "info.txt"

# clear file contents
def clearFile(path):
	with open(path,'w') as file:
		print(f"clearing file {path}")
		pass

# create file
def createFile(path):
	print(f"Creating file {path}")
	clearFile(path)
		
def saveIntoFfile(path,contents):
	with open(path,'w') as file:
		file.write(contents)
		
# check if file existed
def isFileExisted(path):
	print(f"Checking if {path} existed")
	return os.path.exists(path)
