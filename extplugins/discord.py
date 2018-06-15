#
# ################################################################### #
#                                                                     #
#  Discord Plugin for BigBrotherBot(B3) (www.bigbrotherbot.com)       #
#  Copyright (c) 2018 Miltan aka WatchMiltan                          #
#                                                                     #
#  This program is free software; you can redistribute it and/or      #
#  modify it under the terms of the GNU General Public License        #
#  as published by the Free Software Foundation; either version 2     #
#  of the License, or (at your option) any later version.             #
#                                                                     #
#  This program is distributed in the hope that it will be useful,    #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of     #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the       #
#  GNU General Public License for more details.                       #
#                                                                     #
#  You should have received a copy of the GNU General Public License  #
#  along with this program; if not, write to the Free Software        #
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA      #
#  02110-1301, USA.                                                   #
#                                                                     #
# ################################################################### #
#
#
#  CHANGELOG:
#  02.04.2018 - v1.0 - WatchMiltan
#  - first release.
#  23.04.2018 - v1.1 - WatchMiltan
#  - added thumbnails and icons for BO2
#  - using a configuration file to get webhook
#  29.04.2018 - v1.2 - WatchMiltan
#  - it actually works now
#  05.06.2018 - v1.3 - WatchMiltan
#  - partial rewrite, adjusted colors
#  - corrected json parsing
#  - added comments for easier comprehension
#


__version__ = '1.3gh'
__author__  = 'WatchMiltan'

#b3 libaries
import b3
import b3.events
import b3.plugin

#libaries for webhook and embed
import requests 
import json
import datetime
import time
import re
from collections import defaultdict


#discord embed formatting
class DiscordEmbed: 
    def __init__(self, url, **kwargs):
        self.url = url
        self.color = kwargs.get('color')
        self.gamename = kwargs.get('author')
        self.gamename_icon = kwargs.get('author_icon')
        self.fields = kwargs.get('fields', [])
        self.mapview = kwargs.get('thumbnail')
        self.footnote = kwargs.get('footer')

    def set_gamename(self, **kwargs):
        self.gamename = kwargs.get('name')
        self.gamename_icon = kwargs.get('icon')

    def set_mapview(self, url):
        self.mapview = url

    def textbox(self,**kwargs):
        name = kwargs.get('name')
        value = kwargs.get('value')
        inline = kwargs.get('inline', True)
        field = {'name' : name, 'value' : value, 'inline' : inline}
        self.fields.append(field)

    def set_footnote(self,**kwargs):
        self.footnote = kwargs.get('text')
        self.ts = str(datetime.datetime.utcfromtimestamp(time.time()))

    @property
    def push(self, *arg): #compiling push data to be sent to discord
        data = {}
        data["embeds"] = []
        embed = defaultdict(dict)

        if self.gamename: embed["author"]["name"] = self.gamename
        if self.gamename_icon: embed["author"]["icon_url"] = self.gamename_icon
        if self.color: embed["color"] = self.color
        if self.mapview: embed["thumbnail"]['url'] = self.mapview
        if self.footnote: embed["footer"]['text'] = self.footnote
        if self.ts: embed["timestamp"] = self.ts

        if self.fields:
            embed["fields"] = []
            for field in self.fields:
                f = {}
                f["name"] = field['name']
                f["value"] = field['value']
                f["inline"] = field['inline']
                embed["fields"].append(f)

        data["embeds"].append(dict(embed))
        empty = all(not d for d in data["embeds"])
        if empty: data['embeds'] = []
        return json.dumps(data)

    def post(self): #push data to webhook
        headers = {'Content-Type': 'application/json'}
        result = requests.post(self.url, data=self.push, headers=headers)
        

class DiscordPlugin(b3.plugin.Plugin):
    _adminPlugin = None

    def onLoadConfig(self):
        self.url = str(self.config.get('settings', 'webhook'))
        return

    def onStartup(self):
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            self.debug('Admin Plugin not found!')
            return False
        else:
            self.debug('Plugin successfully loaded')

        self._adminPlugin.registerCommand(self, 'report', 0, self.cmd_report)
        self.debug('Report Command registered in admin plugin')

    #remove colorcodes
    def stripColors(self, s):
        return re.sub('\^[0-9]{1}','',s)

    def cmd_report(self, data, client=None, cmd=None):
        if not data:
            client.message('^1Incorrect report syntax.')
            return False
        else:
            input = self._adminPlugin.parseUserCmd(data)

            if not self._adminPlugin.findClientPrompt(input[0], client):
                #player not amoung connected clients
                client.message('Player ^1not found.')
                return False

            cheater_id_b3 = str(self._adminPlugin.findClientPrompt(input[0], client))
            cheater = cheater_id_b3.split(':')[2]
            reporter = self.stripColors(client.exactName)

            dict = self.console.game.__dict__
            server = self.stripColors(str(dict['sv_hostname']))
            map = dict['_mapName']
            game = dict['gameName']

            #constructing embedded message to be sent on server
            if 'cod8' in game.lower():
                embed = DiscordEmbed(self.url, color=0x97C928)
                embed.set_gamename(name='Call of Duty: Modern Warfare 3', icon='https://orig00.deviantart.net/9af1/f/2011/310/2/1/modern_warfare_3_logo_by_wifsimster-d4f9ozd.png')

                #changing mapview according to mapname
                if 'dome' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/f/f1/Bare_Load_Screen_Dome_MW3.png')
                elif 'terminal' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/6/68/Terminal_Loading_Screen_MW3.png')
                elif 'alpha' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/a/a6/Lockdown_loading_screen_MW3.PNG')
                elif 'bootleg' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/0/08/Bare_Load_Screen_Bootleg_MW3.png')
                elif 'carbon' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/c/c8/Bare_Load_Screen_Carbon_MW3.png')
                elif 'exchange' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/b/bb/Loading_Screen_Flood_the_Market_MW3.png')
                elif 'harthat' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/5/5a/Bare_Load_Screen_Hardhat_MW3.png')
                elif 'interchange' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/4/4b/Bare_Load_Screen_Interchange_MW3.png')
                elif 'paris' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/a/a7/Iron_Lady_MW3.png')
                elif 'plaza2' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/6/6d/Mall_Interior_Arkaden_MW3.png')
                elif 'seatown' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/a/a7/Bare_Load_Screen_Seatown_MW3.png/revision/latest?cb=20120320235504')
                elif 'underground' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/0/09/Bare_Load_Screen_Underground_MW3.png')
                elif 'village' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/f/f4/Bare_Load_Screen_Village_MW3.png')
                else:
                    embed.set_mapview('https://cdn0.iconfinder.com/data/icons/flat-design-basic-set-1/24/error-exclamation-512.png')

            elif 't6' in game.lower():
                embed = DiscordEmbed(self.url, color=1)
                embed.set_gamename(name='Call of Duty: Black Ops 2', icon='https://i.pinimg.com/originals/5a/44/5c/5a445c5c733c698b32732550ec797e91.jpg')

                if 'mp_la' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/b/ba/Aftermath_loading_screen_BOII.png')
                elif 'carrier' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/8/88/Carrier_loadscreen_BOII.png')
                elif 'drone' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/5/5b/Drone_loadscreen_BOII.png')
                elif 'express' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/b/b1/Express_bullet_train_BOII.png/revision/latest?cb=20130224044951')
                elif 'hijacked' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/4/42/Hijacked..png/revision/latest?cb=20130407201845&path-prefix=de')
                elif 'meltdown' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/f/f2/Meltdown..png/revision/latest?cb=20130506221321&path-prefix=de')
                elif 'overflow' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/8/80/Overflow_Load_Screen_BOII.png')
                elif 'nightclub' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/7/74/Plaza_Load_Screen_BOII.png')
                elif 'raid' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/2/29/Raid_Load_Screen_BOII.png')
                elif 'slums' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/0/04/Slums_Load_Screen_BOII.png/revision/latest?cb=20121209080826')
                elif 'village' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/f/f7/Standoff..png/revision/latest?cb=20130429072412&path-prefix=de')
                elif 'turbine' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/5/50/Turbine_Load_Screen_BOII.png')
                elif 'socotra' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/6/6d/Yemen_Load_Screen_BOII.png')
                elif 'nuketown' in map.lower():
                    embed.set_mapview('https://vignette.wikia.nocookie.net/callofduty/images/5/52/Nuketown_2015..png/revision/latest?cb=20130210235047&path-prefix=de')
                else:
                    embed.set_mapview('https://cdn0.iconfinder.com/data/icons/flat-design-basic-set-1/24/error-exclamation-512.png')

            else:
                embed = DiscordEmbed(self.url, color=0xff0000)
                embed.set_gamename(name='Cheater Report: '+ game)
                embed.set_mapview('https://cdn0.iconfinder.com/data/icons/flat-design-basic-set-1/24/error-exclamation-512.png')

            embed.textbox(name='Reported Player', value=cheater[1:-1])
            embed.textbox(name='Server', value=server)
            embed.set_footnote(text='reported by '+ reporter)
            embed.post()
            self.debug('Report message sent to Discord.')
            client.message('^2Player has been reported on Discord!')
