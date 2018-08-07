# ![BigBrotherBot](http://i.imgur.com/7sljo4G.png) b3-plugin-discord
Sends report messages to Discord using Discord webhooks. 

Images available for Call of Duty: Modern Warfare 3, Call of Duty: Black Ops 2, Call of Duty 4: Modern Warfare.
![Report Example](https://i.gyazo.com/6d689a99e99aafe84d592afa3ab35fde.png)
![Report Example](https://i.gyazo.com/20fc9da7f1e6f07ce3f217b69f5489c6.png)
![Report Example](https://i.gyazo.com/3110854464e4a86be286202ddd345fd6.png)
![Report Example](https://i.gyazo.com/97f545fcba56f20e0520aeef459f9a54.png)

If ingame images haven't been added, it will show default pictures.
![Report Example](https://i.gyazo.com/2ffd11b9c6dd931107dcdce98c232ad9.png)


See it in action: https://discord.gg/x499c9k

---------
### Requirements
- If you have B3 1.10 or higher, it should work out of the box.

- For B3 1.9.2 Python version **(not windows-standalone)**
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


