# ![BigBrotherBot](http://i.imgur.com/7sljo4G.png) b3-plugin-discord
Sends report messages to Discord using Discord webhooks. 

![Report Example](https://i.gyazo.com/453dcbf99baf2f92067919996666b9ad.png)
![Report Example](https://i.gyazo.com/20fc9da7f1e6f07ce3f217b69f5489c6.png)

---------
### Requirements

- B3 Python version (not windows-standalone)
- `requests` module
  - install with `pip install requests`
---------
### Installation

1. Create/Edit a Discord webhook in the desired channel.
2. Paste discord.xml in b3/extplugins/conf.
3. Paste discord.py in b3/extplugins.
4. Edit discord.xml, paste your webhook url and save the file.
5. Add the following line to your b3 configuration file (b3.xml):

`
<plugin name="discord" config="@b3/extplugins/conf/discord.xml"/>
`

6. Restart BigBrotherBot

***IMPORTANT: Restart map after plugin is loaded!***

---------  
### Usage

!report &lt;playername&gt;

---------
### Disclaimer

The author of this opensource plugin endorse NO responsibility whatsoever for any problem that might arise when using this tool.
Discord: WatchMiltan#7507


