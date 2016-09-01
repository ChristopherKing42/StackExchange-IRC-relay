import socket
import sys

import chatexchange.client
import chatexchange.events

server = "irc.freenode.org"       #settings
channel = raw_input("IRC channel: ")
botnick = raw_input("IRC bot nick: ")

room_id = raw_input("Stack Exchange room id: ")
email = raw_input("Stack Exchange bot email: ")
password = raw_input("Stack Exchange bot password: ")

#Based on code from http://stackoverflow.com/a/12219119/1172541

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
print "connecting to:"+server
irc.connect((server, 6667))                                                         #connects to the server
irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :This is a fun bot!\n") #user authentication
irc.send("NICK "+ botnick +"\n")                            #sets nick
# irc.send("PRIVMSG nickserv :iNOOPE\r\n")    #auth
irc.send("JOIN "+ channel +"\n")        #join the chan

#Based on sample from https://github.com/Manishearth/ChatExchange/blob/master/examples/chat.py

def on_message(message, client):
    if not isinstance(message, chatexchange.events.MessagePosted):
        # Ignore non-message_posted events.
        return
    if message.user == client.get_me():
        # Ignore messages from self
        return
    irc.send("PRIVMSG " + channel + ' :<' + message.user.name + '> ' + message.content + '\r\n')

host_id = 'stackexchange.com'
print "connecting to:"+host_id
client = chatexchange.client.Client(host_id)
client.login(email, password)

room = client.get_room(room_id)
room.join()
room.watch(on_message)

def parseIRC(text):
    components = text.split(':',2)
    name = components[1].split('!')[0]
    if "JOIN" in components[1]:
        return name + " joined."
    message = components[2]
    return "<"+name+"> "+message

# Also from http://stackoverflow.com/a/12219119/1172541

while True:    #puts it in a loop
    text=irc.recv(2040)  #receive the text

    if 'PING' in text:                          #check if 'PING' is found
        irc.send('PONG ' + text.split() [1] + '\r\n') #returnes 'PONG' back to the server (prevents pinging out!)

    try: room.send_message(parseIRC(text))
    except IndexError: pass
