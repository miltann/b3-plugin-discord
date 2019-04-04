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
#  - added thumbnails and icons for t6 (BO2)
#  - using a configuration file to get webhook
#  29.04.2018 - v1.2 - WatchMiltan
#  - it actually works now
#  05.06.2018 - v1.3 - WatchMiltan
#  - partial rewrite, adjusted colors
#  - corrected json parsing
#  - added comments for easier comprehension
#  16.06.2018 - v1.4 - WatchMiltan
#  - added thumbnails and icons for cod4
#  - added thumbnails and icons for cod6 (MW2)
#  19.11.2018 - v1.5 - WatchMiltan
#  - notifications sent if player gets banned/kicked
#  20.01.2019 - v1.6 - WatchMiltan
#  - notifications sent if player gets tempbanned
#  12.02.2019 - v1.7 - WatchMiltan
#  - notification sent if player leaves the game
#  14.02.2019 - v1.8 - WatchMiltan
#  - added clean command, sends notification if player has been checked
#  15.02.2019 - v1.9 - WatchMiltan
#  - improved code & cleanup
#  21.03.2019 - v2.0 - WatchMiltan
#  - code cleanup
#  - fixed event order
#  - added thumbnails and icons for cod7 (BO)
#

__version__ = '2.0gh'
__author__  = 'WatchMiltan'

import b3
import b3.events
import b3.plugin
from b3 import functions

import requests
import json
import datetime
import time
import re
from collections import defaultdict

class DiscordEmbed:
    def __init__(self, url, **kwargs):
        self.url = url
        self.color = kwargs.get('color')
        self.gamename = kwargs.get('author')
        self.gamename_icon = kwargs.get('author_icon')
        self.fields = kwargs.get('fields', [])
        self.mapview = kwargs.get('thumbnail')
        self.desc = kwargs.get('desc')
        self.footnote = kwargs.get('footer')

    def set_gamename(self, **kwargs):
        self.gamename = kwargs.get('name')
        self.gamename_icon = kwargs.get('icon')

    def set_mapview(self, url):
        self.mapview = url

    def set_desc(self, desc):
        self.desc = desc

    def textbox(self,**kwargs):
        field = {'name' : kwargs.get('name'),
                'value' : kwargs.get('value'), 
                'inline' : kwargs.get('inline', True)}
        self.fields.append(field)

    def set_footnote(self,**kwargs):
        self.footnote = kwargs.get('text')
        self.ts = str(datetime.datetime.utcfromtimestamp(time.time()))

    @property
    def push(self, *arg):
        data = {}
        data["embeds"] = []
        embed = defaultdict(dict)

        if self.gamename: embed["author"]["name"] = self.gamename
        if self.gamename_icon: embed["author"]["icon_url"] = self.gamename_icon
        if self.color: embed["color"] = self.color
        if self.mapview: embed["thumbnail"]['url'] = self.mapview
        if self.desc: embed["description"] = self.desc
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

    def post(self):
        headers = {'Content-Type': 'application/json'}
        result = requests.post(self.url, data=self.push, headers=headers)


class DiscordPlugin(b3.plugin.Plugin):
    _adminPlugin = None
    
    def onLoadConfig(self):
        self.url = str(self.config.get('settings', 'webhook'))
        return

    def onStartup(self):
        self.reportedplayers = []
        self.gamelist = {
        'cod8' : {
          'color': 0x97C928,
          'name': 'Call of Duty: Modern Warfare 3',
          'icon': 'https://orig00.deviantart.net/9af1/f/2011/310/2/1/modern_warfare_3_logo_by_wifsimster-d4f9ozd.png',
          'dome': 'https://vignette.wikia.nocookie.net/callofduty/images/f/f1/Bare_Load_Screen_Dome_MW3.png',
          'terminal':'https://vignette.wikia.nocookie.net/callofduty/images/6/68/Terminal_Loading_Screen_MW3.png',
          'alpha': 'https://vignette.wikia.nocookie.net/callofduty/images/a/a6/Lockdown_loading_screen_MW3.PNG',
          'bootleg': 'https://vignette.wikia.nocookie.net/callofduty/images/0/08/Bare_Load_Screen_Bootleg_MW3.png',
          'carbon': 'https://vignette.wikia.nocookie.net/callofduty/images/c/c8/Bare_Load_Screen_Carbon_MW3.png',
          'exchange': 'https://vignette.wikia.nocookie.net/callofduty/images/b/bb/Loading_Screen_Flood_the_Market_MW3.png',
          'harthat': 'https://vignette.wikia.nocookie.net/callofduty/images/c/c0/Hardhat_Load_Screen_CODO.png/revision/latest?cb=20171230164642',
          'interchange': 'https://vignette.wikia.nocookie.net/callofduty/images/4/4b/Bare_Load_Screen_Interchange_MW3.png',
          'paris': 'https://vignette.wikia.nocookie.net/callofduty/images/a/a7/Iron_Lady_MW3.png',
          'plaza2': 'https://vignette.wikia.nocookie.net/callofduty/images/6/6d/Mall_Interior_Arkaden_MW3.png',
          'seatown': 'https://vignette.wikia.nocookie.net/callofduty/images/a/a7/Bare_Load_Screen_Seatown_MW3.png/revision/latest?cb=20120320235504',
          'underground': 'https://vignette.wikia.nocookie.net/callofduty/images/0/09/Bare_Load_Screen_Underground_MW3.png',
          'village': 'https://vignette.wikia.nocookie.net/callofduty/images/f/f4/Bare_Load_Screen_Village_MW3.png'
        },

        't6' : {    
          'color': 1,
          'name': 'Call of Duty: Black Ops 2',
          'icon': 'https://i.pinimg.com/originals/5a/44/5c/5a445c5c733c698b32732550ec797e91.jpg', 
          'mp_la': 'https://vignette.wikia.nocookie.net/callofduty/images/b/ba/Aftermath_loading_screen_BOII.png',
          'carrier': 'https://vignette.wikia.nocookie.net/callofduty/images/8/88/Carrier_loadscreen_BOII.png',
          'drone': 'https://vignette.wikia.nocookie.net/callofduty/images/5/5b/Drone_loadscreen_BOII.png',
          'express': 'https://vignette.wikia.nocookie.net/callofduty/images/b/b1/Express_bullet_train_BOII.png/revision/latest?cb=20130224044951',
          'hijacked':'https://vignette.wikia.nocookie.net/callofduty/images/4/42/Hijacked..png/revision/latest?cb=20130407201845&path-prefix=de',
          'meltdown': 'https://vignette.wikia.nocookie.net/callofduty/images/f/f2/Meltdown..png/revision/latest?cb=20130506221321&path-prefix=de',
          'overflow':'https://vignette.wikia.nocookie.net/callofduty/images/8/80/Overflow_Load_Screen_BOII.png',
          'nightclub': 'https://vignette.wikia.nocookie.net/callofduty/images/7/74/Plaza_Load_Screen_BOII.png',
          'raid': 'https://vignette.wikia.nocookie.net/callofduty/images/2/29/Raid_Load_Screen_BOII.png',
          'slums': 'https://vignette.wikia.nocookie.net/callofduty/images/0/04/Slums_Load_Screen_BOII.png/revision/latest?cb=20121209080826',
          'village': 'https://vignette.wikia.nocookie.net/callofduty/images/5/50/Turbine_Load_Screen_BOII.png',
          'turbine': 'https://vignette.wikia.nocookie.net/callofduty/images/5/50/Turbine_Load_Screen_BOII.png',
          'socotra': 'https://vignette.wikia.nocookie.net/callofduty/images/6/6d/Yemen_Load_Screen_BOII.png',
          'nuketown': 'https://vignette.wikia.nocookie.net/callofduty/images/5/52/Nuketown_2015..png/revision/latest?cb=20130210235047&path-prefix=de'
        },
        
        'cod4' : {    
          'color': 0x296731,
          'name': 'Call of Duty 4: Modern Warfare',
          'icon': 'http://orig05.deviantart.net/8749/f/2008/055/0/c/call_of_duty_4__dock_icon_by_watts240.png',
          'backlot': 'https://vignette.wikia.nocookie.net/callofduty/images/0/0f/Backlot_loadscreen_CoD4.jpg',
          'bloc': 'https://vignette.wikia.nocookie.net/callofduty/images/9/9d/Bare_Load_Screen_Bloc_CoD4.jpg',
          'bog': 'https://vignette.wikia.nocookie.net/callofduty/images/2/29/Bog_Map_Image_CoD4.jpg/revision/latest?cb=20100723075648',
          'cargoship': 'https://vignette.wikia.nocookie.net/callofduty/images/e/e5/Cod4_map_wetwork.jpg',
          'citystreets': 'https://vignette.wikia.nocookie.net/callofduty/images/9/92/Cod4_map_district.jpg',
          'convoy': 'https://vignette.wikia.nocookie.net/callofduty/images/3/3c/Bare_Load_Screen_Ambush_CoD4.jpg/revision/latest?cb=20100723075603',
          'countdown': 'https://vignette.wikia.nocookie.net/callofduty/images/e/e9/Bare_Load_Screen_Countdown_CoD4.jpg/revision/latest?cb=20100723075829',
          'crash': 'https://vignette.wikia.nocookie.net/callofduty/images/9/90/Bare_Load_Screen_Crash_CoD4.jpg/revision/latest?cb=20110727174701',
          'crossfire': 'https://vignette.wikia.nocookie.net/callofduty/images/5/53/Cod4_map_crossfire.jpg/revision/latest?cb=20100723075954',
          'farm': 'https://vignette.wikia.nocookie.net/callofduty/images/8/82/Bare_Load_Screen_Downpur_CoD4.jpg/revision/latest?cb=20110727175118',
          'overgrown': 'https://vignette.wikia.nocookie.net/callofduty/images/7/7d/Bare_Load_Screen_Overgrown_CoD4.jpg/revision/latest?cb=20110727174104',
          'pipeline': 'https://vignette.wikia.nocookie.net/callofduty/images/2/29/Cod4_map_pipeline.jpg/revision/latest?cb=20100723080432',
          'shipment': 'https://vignette.wikia.nocookie.net/callofduty/images/9/9b/Shipment_Load.jpg/revision/latest?cb=20100723080524',
          'showdown': 'https://vignette.wikia.nocookie.net/callofduty/images/1/1f/Showdown_Overview_CoD4.jpg/revision/latest?cb=20120519205219',
          'strike': 'https://vignette.wikia.nocookie.net/callofduty/images/b/b0/Loadscreen_mp_strike.jpg/revision/latest?cb=20100712195725',
          'vacant': 'https://vignette.wikia.nocookie.net/callofduty/images/f/f6/Cod4_map_vacant.jpg/revision/latest?cb=20100723080839',
          'snow': 'https://vignette.wikia.nocookie.net/callofduty/images/f/f7/Bare_Load_Screen_Winter_Crash_CoD4.jpg/revision/latest?cb=20100723080720',
          'broadcast': 'https://vignette.wikia.nocookie.net/callofduty/images/e/ec/Broadcast_loading_screen_CoD4.jpg/revision/latest?cb=20100723080927',
          'carentan': 'https://vignette.wikia.nocookie.net/callofduty/images/9/95/Carentan_View_1_WWII.jpg/revision/latest?cb=20171223000154',
          'creek': 'https://vignette.wikia.nocookie.net/callofduty/images/e/e1/CreekCOD4.jpg/revision/latest?cb=20100723075941',
          'killhouse': 'https://vignette.wikia.nocookie.net/callofduty/images/4/48/Cod4-killhouse.jpg/revision/latest?cb=20100723081127'
        },
                
        'cod6' : {    
          'color': 0xC19640,
          'name': 'Call of Duty: Modern Warfare 2',
          'icon': 'https://i.gyazo.com/758b6933287392106bfdddc24b09d502.png',
          'mp_afghan': 'https://vignette.wikia.nocookie.net/callofduty/images/8/83/Afghan_loading_screen_MW2.png/revision/latest?cb=20130310131229',
          'mp_boneyard': 'https://vignette.wikia.nocookie.net/callofduty/images/e/ef/Scrapyard.jpg/revision/latest?cb=20100720174413',
          'mp_brecourt': 'https://vignette.wikia.nocookie.net/callofduty/images/c/cc/Wasteland.jpg/revision/latest?cb=20100720174520',
          'mp_checkpoint': 'https://vignette.wikia.nocookie.net/callofduty/images/9/9f/Karachi-prev.jpg/revision/latest?cb=20100720174412',
          'mp_derail': 'https://vignette.wikia.nocookie.net/callofduty/images/2/20/Derail.jpg/revision/latest?cb=20100720174408',
          'mp_estate': 'https://vignette.wikia.nocookie.net/callofduty/images/9/91/Estate.jpg/revision/latest?cb=20100720174409',
          'mp_favela': 'https://vignette.wikia.nocookie.net/callofduty/images/2/29/Favela_Map_MW2.jpg/revision/latest?cb=20100720174410',
          'mp_highrise': 'https://vignette.wikia.nocookie.net/callofduty/images/4/49/Highrise-promo.jpg/revision/latest?cb=20100720174411',
          'mp_invasion': 'https://vignette.wikia.nocookie.net/callofduty/images/9/95/Invasion_MW2.jpg/revision/latest?cb=20100720174410',
          'mp_nightshift': 'https://vignette.wikia.nocookie.net/callofduty/images/d/d2/Skidrow.jpg/revision/latest?cb=20100720174516',
          'mp_quarry': 'https://vignette.wikia.nocookie.net/callofduty/images/8/8a/Loadscreen_mp_quarry.jpg/revision/latest?cb=20091207173135',
          'mp_rundown': 'https://vignette.wikia.nocookie.net/callofduty/images/3/3a/Rundown-prev.jpg/revision/latest?cb=20100720174412',
          'mp_rust': 'https://vignette.wikia.nocookie.net/callofduty/images/3/33/Rust.jpg/revision/latest?cb=20100720174413',
          'mp_subbase': 'https://vignette.wikia.nocookie.net/callofduty/images/1/1e/Sub_Base.jpg/revision/latest?cb=20100720174517',
          'mp_terminal': 'https://vignette.wikia.nocookie.net/callofduty/images/1/14/Bare_Load_Screen_Terminal_MW2.jpg/revision/latest?cb=20100720174519',
          'mp_underpass': 'https://vignette.wikia.nocookie.net/callofduty/images/b/b5/Underpass.jpg/revision/latest?cb=20100720174519'
        },
        
        'cod7' : {    
          'color': 0x18819E,
          'name': 'Call of Duty: Black Ops',
          'icon': 'https://i.gyazo.com/93ca65b298bf3738d54304b0f184b5b5.png',
          'mp_nuked': 'https://vignette.wikia.nocookie.net/callofduty/images/2/2c/Bare_Load_Screen_Nuketown_BO.jpg/revision/latest?cb=20110303122337',
          'mp_cracked': 'https://vignette.wikia.nocookie.net/callofduty/images/1/1e/Bare_Load_Screen_Cracked_BO.jpg/revision/latest?cb=20110303121738',
          'mp_array': 'https://vignette.wikia.nocookie.net/callofduty/images/3/35/Bare_Load_Screen_Array_BO.jpg/revision/latest?cb=20110303121651',
          'mp_crisis': 'https://vignette.wikia.nocookie.net/callofduty/images/f/f6/Bare_Load_Screen_Crisis_BO.jpg/revision/latest?cb=20110303121824',
          'mp_firingrange': 'https://vignette.wikia.nocookie.net/callofduty/images/8/82/Bare_Load_Screen_Firing_Range_BO.jpg/revision/latest?cb=20110303121918',
          'mp_duga': 'https://vignette.wikia.nocookie.net/callofduty/images/4/41/Bare_Load_Screen_Grid_BO.jpg/revision/latest?cb=20110303122000',
          'mp_hanoi': 'https://vignette.wikia.nocookie.net/callofduty/images/e/eb/Bare_Load_Screen_Hanoi_BO.jpg/revision/latest?cb=20110303122041',
          'mp_cairo': 'https://vignette.wikia.nocookie.net/callofduty/images/e/e7/Bare_Load_Screen_Havana_BO.jpg/revision/latest?cb=20110303122124',
          'mp_havoc': 'https://vignette.wikia.nocookie.net/callofduty/images/c/c6/Bare_Load_Screen_Jungle_BO.jpg/revision/latest?cb=20110303122217',
          'mp_cosmodrome': 'https://vignette.wikia.nocookie.net/callofduty/images/c/c6/Bare_Load_Screen_Launch_BO.jpg/revision/latest?cb=20110303122251',
          'mp_radiation': 'https://vignette.wikia.nocookie.net/callofduty/images/2/20/Bare_Load_Screen_Radiation_BO.jpg/revision/latest?cb=20110303122417',
          'mp_mountain': 'https://vignette.wikia.nocookie.net/callofduty/images/5/54/Bare_Load_Screen_Summit_BO.jpg/revision/latest?cb=20110303122702',
          'mp_villa': 'https://vignette.wikia.nocookie.net/callofduty/images/2/2a/Bare_Load_Screen_Villa_BO.jpg/revision/latest?cb=20110303122503',
          'mp_russianbase': 'https://vignette.wikia.nocookie.net/callofduty/images/1/12/Bare_Load_Screen_WMD_BO.jpg/revision/latest?cb=20110303122544'
        }
        }        
        
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            self.debug('Admin Plugin not found!')
            return False
        else:
            self.debug('Plugin successfully loaded')

        self.registerEvent(b3.events.EVT_CLIENT_BAN) #27
        self.registerEvent(b3.events.EVT_CLIENT_KICK) #26
        self.registerEvent(b3.events.EVT_CLIENT_BAN_TEMP) #28
        self.registerEvent(b3.events.EVT_CLIENT_DISCONNECT) #10
        self._adminPlugin.registerCommand(self, 'report', 0, self.cmd_report)
        self._adminPlugin.registerCommand(self, 'clean', 40, self.cmd_clean)
        self.debug('Report Command registered in admin plugin')

    def stripColors(self, s):
        return re.sub('\^[0-9]{1}','',s)

    def onEvent(self, event):
        if event.type and event.client.name in self.reportedplayers:
            lastBan = event.client.lastBan
            embed = DiscordEmbed(self.url, color=0xFFFFFF)
            if not (event.type == b3.events.EVT_CLIENT_DISCONNECT):
                embed.set_mapview('https://www.iconsdb.com/icons/download/green/checkmark-16.png')
            
            if (event.type == b3.events.EVT_CLIENT_DISCONNECT):
                if (event.type == b3.events.EVT_CLIENT_BAN):
                    self.debug("Shouldn't happen")

            if (event.type == b3.events.EVT_CLIENT_KICK): 
                embed.set_desc("%s has been kicked." % (event.client.name))
                embed.set_footnote()
            elif (event.type == b3.events.EVT_CLIENT_BAN):
                embed.set_desc(event.client.name +" has been banned by " + self._adminPlugin.findClientPrompt('@%s' % str(lastBan.adminId), None).name)
                embed.set_footnote(text="Reason: " + self.stripColors(lastBan.reason.replace(',', '')))
            elif (event.type == b3.events.EVT_CLIENT_BAN_TEMP):
                embed.set_desc("%s has been temporarily banned by %s for %s" % (event.client.name, self._adminPlugin.findClientPrompt('@%s' % str(lastBan.adminId), None).name, functions.minutesStr(lastBan.duration)))
                embed.set_footnote(text="Reason: " + self.stripColors(lastBan.reason.replace(',', '')))
            elif (event.type == b3.events.EVT_CLIENT_DISCONNECT) and not lastBan:
                embed.set_desc("%s has left the game." % (event.client.name))
                embed.set_footnote()
                
            embed.post()
            self.reportedplayers.remove(event.client.name)
        if len(self.reportedplayers) > 6:
            self.reportedplayers.pop(0)
    
    def cmd_clean(self, data, client=None, cmd=None):
        if not data:
            client.message('^1Incorrect syntax. !clean <player>')
            return False
        else:
            input = self._adminPlugin.parseUserCmd(data)

            if not self._adminPlugin.findClientPrompt(input[0], client):
                return False
                
            player = str(self._adminPlugin.findClientPrompt(input[0], client)).split(':')[2]
            cleanplayer = player[1:-1]
            
            if cleanplayer in self.reportedplayers:
                self.reportedplayers.remove(cleanplayer)
                embed = DiscordEmbed(self.url, color=0xFFFFFF)
                embed.set_mapview('https://www.iconsdb.com/icons/download/green/checkmark-16.png')
                embed.set_desc("%s has been checked by %s" % (cleanplayer, self.stripColors(client.exactName)))
                embed.set_footnote()
                embed.post()
                client.message('Player has been checked.')
            elif cleanplayer not in self.reportedplayers:
                client.message('Player was ^1not reported.')
                return False


    def cmd_report(self, data, client=None, cmd=None):
        if not data:
            client.message('^1Incorrect syntax. !report <player>')
            return False
        else:
            input = self._adminPlugin.parseUserCmd(data)

            if not self._adminPlugin.findClientPrompt(input[0], client):
                return False

            cheater = str(self._adminPlugin.findClientPrompt(input[0], client)).split(':')[2]
            reporter = self.stripColors(client.exactName)
            
            dict = self.console.game.__dict__
            server = self.stripColors(str(dict['sv_hostname']))
            map = dict['_mapName'].lower()
            game = dict['gameName'].lower()

            if cheater[1:-1] not in self.reportedplayers:
                self.reportedplayers.append(cheater[1:-1])

            if game in self.gamelist:
                gamelist = self.gamelist[game]
                embed = DiscordEmbed(self.url, color=gamelist['color'])
                embed.set_gamename(name=gamelist['name'], icon=gamelist['icon'])
                embed.set_mapview('https://cdn0.iconfinder.com/data/icons/flat-design-basic-set-1/24/error-exclamation-512.png')
                
                for key in gamelist:
                    if key in map:
                        embed.set_mapview(gamelist[key])

            else:
                embed = DiscordEmbed(self.url, color=0xFF0000)
                embed.set_gamename(name='Cheater Report: '+ game)
                embed.set_mapview('https://cdn0.iconfinder.com/data/icons/flat-design-basic-set-1/24/error-exclamation-512.png')

            embed.textbox(name='Reported Player', value=cheater[1:-1])
            embed.textbox(name='Server', value=server)
            embed.set_footnote(text='reported by '+ reporter)
            embed.post()
            client.message('Player has been ^2reported on Discord!')
