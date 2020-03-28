# ![BigBrotherBot](http://i.imgur.com/7sljo4G.png) b3-plugin-discord
Sends report messages to Discord using Discord webhooks. 

- !report &lt;playername&gt; - Sends a report notification to discord.
- !clean &lt;playername&gt; - Admins can use this command to let the others know that he has been checked

Images available for Call of Duty: Modern Warfare 3, Call of Duty: Black Ops 2, Call of Duty 4: Modern Warfare and Call of Duty: Black Ops.

![Report Example](https://i.gyazo.com/6d689a99e99aafe84d592afa3ab35fde.png)
![Report Example](https://i.gyazo.com/20fc9da7f1e6f07ce3f217b69f5489c6.png)
![Report Example](https://i.gyazo.com/3110854464e4a86be286202ddd345fd6.png)
![Report Example](https://i.gyazo.com/97f545fcba56f20e0520aeef459f9a54.png)
![Report Example](https://i.gyazo.com/c7d6d0e4ba0f19c14a3ec8d12ed695cc.png)

If ingame images haven't been added, it will show default pictures.
![Report Example](https://i.gyazo.com/2ffd11b9c6dd931107dcdce98c232ad9.png)

Will also send notfications when a player **leaves**, gets **banned** or gets **kicked** on the server.

![Player left](https://i.gyazo.com/d5c3941a7869eb0992b6fb1e95ee424a.png)
![Tempbanned](https://i.gyazo.com/cfdab1887f807212bcc94ef49c6c93ff.png)
![Checked](https://i.gyazo.com/e18682edbfcb0c2463c541171a8b1d56.png)
![Banned](https://i.gyazo.com/9b4e4f975dc25f51f1867a3429ae5174.png)
![Kicked](https://i.gyazo.com/1e89a62267feeb61bcf130d9de16cabe.png)


See it in action: https://discord.gg/x499c9k

---------
### Requirements
- If you have B3 1.10 or higher, it should work out of the box.

- For B3 1.9.2 Python version **(not windows-standalone)** :
  - `requests` module required
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
### Disclaimer

The author of this opensource plugin endorse NO responsibility whatsoever for any problem that might arise when using this tool.


