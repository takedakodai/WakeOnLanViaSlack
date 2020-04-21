from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply
from wakeonlan import send_magic_packet
import requests
import json
import re

def getArgs(self):
    text = self.body['text']   
    args = text.split()
    n = len(args)
    return args, n

def getUID(self):
    uName = self.user['id']
    return uName 

def getMAC_DB():
    with open('data/MAC_table.json') as f:
        try:
            df = json.load(f)
        except ValueError:
            df = {}   
    return df

def acquireInfo(self):
    UID = getUID(self)
    df = getMAC_DB()   
    MAC_List = df.get(UID)
    return UID, df, MAC_List

def saveMAC_DB(self):
    with open('data/MAC_table.json', 'w') as f:
        json.dump(self, f, indent=4)
    print('Update DB')

def checkMacForm(self):
    match_obj = re.match(r'^[0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}$',self)
    if (match_obj == None):
        return False
    else: 
        return True

def checkIndexForm(self):
    match_obj = re.match(r'^\d+$',self)
    if (match_obj == None):
        return False
    else: 
        return True

@respond_to(r'^wol')
def DoWakeOnLan(message):
    args, n = getArgs(message)

    if (n == 1):
        message.reply('At least, one index is required.')
        return
    
    UID, df, MAC_List = acquireInfo(message)
    print('wol command by '+ UID)

    if (df == {}):
        message.reply('No MAC address is registered.')
        return    

    for Index in args[1:n]:
        
        if (checkIndexForm(Index) == False):
            message.reply('This index (' + Index + ') is skipped because it is not number. Index should be number.')
            continue
        targetAddr = MAC_List.get(str(Index))
        if (MAC_List != None and targetAddr != None):
            message.reply('Sending a magic packet to ' + targetAddr['MAC'])
            macAddr = targetAddr['MAC'].replace('-', ':')
            send_magic_packet(str(macAddr))
            print('Sending a magic packet to ' + macAddr + ' by ' + UID)
        else:
            message.reply('MAC address corresponding to the index (' + Index + ') you rquested does not exist.')
    
# MAC address management
@respond_to(r'^register')
def registerMAC(message):
    args, n = getArgs(message)

    if (n == 1):
        message.reply('MAC address is required')
        return
    if (n >= 4):
        message.reply('Too many arguments')
        return
    if (n >= 2):
        if (checkMacForm(args[1]) == False):
            message.reply('Invalid MAC address')
            return
        macAddr = args[1]
        labelName = ''
    if (n == 3):
        labelName = re.match(r'[0-9a-zA-Z_\-]+',args[2]).group()
    
    UID, df, MAC_List = acquireInfo(message)
    print('register command by '+ UID)

    if (MAC_List == None):
        df[UID] = {}
        df[UID][0] = {'MAC':macAddr, 'Label':labelName}
    else:
        MaxContents = len(MAC_List)
        for i in range(MaxContents+1):
            if (MAC_List.get(str(i)) == None):
                df[UID][str(i)]= {'MAC':macAddr, 'Label':labelName}
    
    message.reply('Your MAC address has been registered.')

    saveMAC_DB(df)
        
@respond_to(r'^rename')
def renameLabel(message):
    args, n = getArgs(message)

    if (n == 1):
        message.reply('Index and label name are required')
        return
    if (n == 2):
        message.reply('Label name is required')
        return
    if (n >= 4):
        message.reply('Too many arguments')
        return

    UID, df, MAC_List = acquireInfo(message)
    print('rename command by '+UID)
    
    if (df == {}):
        message.reply('No MAC address is registered.')
        return    
    
    if (checkIndexForm(args[1]) == False):
        message.reply('Index should be number')
        return

    Index = args[1]
    labelName = re.match(r'[0-9a-zA-Z_\-]+',args[2]).group()

    targetAddr = MAC_List.get(str(Index))

    if (MAC_List != None and targetAddr != None):
        targetAddr['Label'] = labelName
        MAC_List[str(Index)] = targetAddr
        df[UID] = MAC_List
        message.reply('New label is registered')
    else:
        message.reply('MAC address corresponding to the index (' + Index + ') you rquested does not exist.')

    saveMAC_DB(df)
    
@respond_to(r'^unregister')
def unregisterMAC(message):
    args, n = getArgs(message)

    if (n == 1):
        message.reply('Index is required')
        return

    UID, df, MAC_List = acquireInfo(message)
    print('unregister command by '+UID)

    if (args[1] == 'all'):
        message.reply('Your MAC address list is...\n' + json.dumps(MAC_List,indent=4)+'\n All addresses are being deleted.')
        df[UID] = {}
    else:
        for Index in args[1:n]:
            if (checkIndexForm(Index) == False):
                message.reply('This index (' + Index + ') is skipped because it is not number. Index should be number.')
                continue

            if (MAC_List == None):
                message.reply('Your MAC address is not registered yet.')
            else:
                if (MAC_List.get(str(Index)) != None):
                    df[UID].pop(str(Index))
                    message.reply('Your MAC address has been deleted.')
                else:
                    message.reply('MAC address correponding to the index (' + Index + ') was not found.')
        
    saveMAC_DB(df)

@respond_to(r'^getList')
def getList(message):
    args, n = getArgs(message)

    if (n >= 2):
        message.reply('Too many arguments')
        return

    UID, df, MAC_List = acquireInfo(message)
    print('get list by '+ UID)

    if (MAC_List == None or MAC_List == {}):
        message.reply('Your MAC address is not registered yet.')
    else:
        message.reply('Your MAC address list is...\n'+json.dumps(MAC_List,indent=4))

@respond_to('help')
def howToUse(message):
    message.reply('Command list\n getList -- return your list of MAC address linked to your user ID.\n register [MAC address] [Label] -- register MAC address of your PC you want to wake on lan. Label is optional.\n rename [Index] [New lable] -- change label name of registered MAC address list. Characters available for label name are [0-9a-zA-Z]. Other characters will be ignored.\n unregister [Index] -- Remove your registered MAC address. If you put all in [Index], all addresses you registered will be deleted.\n wol [Index]+ -- Send WOL packet to PC you choose and try to turn it on. To send WOL packets to more than one at one time, you can set multiple Index with a space.')