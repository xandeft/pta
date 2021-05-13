from socket import *
from os import walk
from os import path

def validateUser(userName):
    users = open("users.txt", "r")
    if (userName in users.read()):
        return True
    else:
        return False

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
userisValid = False

while(True):
    try:
        if (userisValid == False):
            connectionSocket, addr = serverSocket.accept()
        msg = connectionSocket.recv(1024).decode()

        try:
            seq_num, command= msg.split(' ')[0], msg.split(' ')[1]
            if (command == "CUMP"):
                user = msg.split(' ')[2]
                userisValid = validateUser(user)
                if (userisValid == True):
                    returnMsg = seq_num + " OK"
                    connectionSocket.send(returnMsg.encode('ascii'))
                else:
                    returnMsg = seq_num + " NOK"
                    connectionSocket.send(returnMsg.encode('ascii'))
                    connectionSocket.close()
            elif (command == "LIST"):
                if (userisValid == True):
                    files = []
                    sendFiles = ""
                    mypath = "./files"
                    for (dirpath, dirnames, filenames) in walk(mypath):
                        files.extend(filenames)
                        break
                    returnMsg = seq_num + " ARQS " + str(len(files)) + " "
                    connectionSocket.send(returnMsg.encode('ascii'))
                    for i in files:
                        if (i == files[len(files)-1]):
                            sendFiles += i
                        else:
                            sendFiles += i + ","
                    connectionSocket.send(sendFiles.encode('ascii'))

                else:
                    returnMsg = seq_num + " NOK"
                    connectionSocket.send(returnMsg.encode('ascii'))
                    connectionSocket.close()
            elif (command == "PEGA"):
                if (userisValid == True):
                    arq = msg.split(" ")[2]
                    pathArq = "./files/" + arq
                    if (arq in files):
                        sizeArq = path.getsize(pathArq)
                        textPlan = open(pathArq, "r")
                        text = textPlan.read()
                        #newPath = "../" + arq
                        #shutil.move(oldPath, newPath)
                        returnMsg = seq_num + " ARQ " + str(sizeArq) + " " + text
                        connectionSocket.send(returnMsg.encode('ascii'))
                    else:
                        returnMsg = seq_num + " NOK"
                        connectionSocket.send(returnMsg.encode('ascii'))
                else:
                    returnMsg = seq_num + " NOK"
                    connectionSocket.send(returnMsg.encode('ascii'))
                    connectionSocket.close()
            elif (command == "TERM"):
                if (userisValid == True):
                    returnMsg = seq_num + " OK"
                    connectionSocket.send(returnMsg.encode('ascii'))
                    break
                else:
                    returnMsg = seq_num + " NOK"
                    connectionSocket.send(returnMsg.encode('ascii'))
                    connectionSocket.close()
            
            else:
                returnMsg = seq_num + " NOK"
                connectionSocket.send(returnMsg.encode('ascii'))
                connectionSocket.close()

        except (IndexError, ValueError):
            returnMsg = "ERR1"
            connectionSocket.send(returnMsg.encode('ascii'))
            connectionSocket.close()
        
        except (KeyError):
            returnMsg = "ERR2"
            connectionSocket.send(returnMsg.encode('ascii'))
            connectionSocket.close()
        
    except (KeyboardInterrupt, SystemExit):
        break