# WOL via slack

## Wake up your PC anywhere!!

This is a tool for turning on your PC in a specific network through slack.
[Reference](https://qiita.com/sukesuke/items/1ac92251def87357fdf6)

### Install packages

 This program needs following packages. Install by pip as follows:

 ```python
 pip install slackbot
 ```  

 ```python
 pip install wakeonlan
 ```  

### Build a new app of slack and generate the slack api token

First you need to get the slack api token for your bot.  
You can creat a new app on [this integration page](https://api.slack.com/bot-users), and acquire Bot User OAuth Access Token to get authority for this program to work properly.  
The app is *bot* as OAuth scope.

* NOTICE * You have to make an classic app to use rtm.connect of slackbot. [More Detail]( https://api.slack.com/authentication/oauth-v2)

### Install your app to slack

 Choose and install the bot to your workspace.

### Clone this repository and edit configures

 Replace Token in slackbot_settings.py to Bot User OAuth Access Token you have acquired.  

### run main program

run.py should be kept running anytime.
Moreover, this program can start up PCs connected to the same network.

## Usage

 Post following commands to the bot.

### Register your MAC address with a label to a database of the bot. Label is optional. Characters available for label name are [0-9a-zA-Z_-]. Other characters will be ignored

 ```python
 register [MAC address] [Lable]
 ```

### Get your MAC address list with index key

 ```python
 getList
 ```

### Rename the label of your MAC address. Characters available for label name are [0-9a-zA-Z_]. Other characters will be ignored

```python
rename [Index] [Label]
```

### Remove your MAC address from the list. If you put all in [Index], all addresses you registered will be deleted

 ```python
 unregister [Index]+
 ```

### Send Wake on LAN pakcet to MAC address you choose. To send WOL packets to more than one at one time, you can set multiple Index with a space

 ```python
 wol [Index]+
 ```

## Appendix

* Users are identified by their unique IDs. Therefore, they can only access their own database and any username is not necessary.
* The registered data is saved in MAC_table.json.
 Please DO NOT delete this file.
* You also need to setup OS and BIOS. Please ask google wake on lan.
