from phue import Bridge, PhueRegistrationException
from .utils import Utils
from enum import Enum
import datetime
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'config')))
import config


class HueController():
    def __init__(self, bot):
        self.bridge = Bridge(config.bridge_ip)
        self.bot = bot
        self.lights = self.bridge.lights
        self.groups = self.bridge.groups

    # Core Methods

    async def connect(self):
        self.bridge.connect()
    
    async def getAPI(self) -> dict:
        return self.bridge.get_api()

    # Utility Methods

    async def log(self, action: int, light: str):
        class Actions(Enum):
            LIGHT_ON = 1
            LIGHT_OFF = 2
            LIGHT_COLOUR = 3
            LIGHT_BRIGHTNESS = 4
            GROUP_ON = 5
            GROUP_OFF = 6
            GROUP_COLOUR = 7
            GROUP_BRIGHTNESS = 8
        
        print(f"Action {Actions(action).name} performed on {light} at {datetime.datetime.now()}.")

    async def retrieveLightName(self, lightName: str) -> str:
        """
        Retrieves the case sensitive light name.

        Params
        lightName: the caseunsensitive name.
        """

        for light in self.lights:
            if light.name.lower() == lightName.lower():
                return light.name

    async def retrieveGroupName(self, groupName: str) -> str:
        """
        Retrieves the case sensitive group name.

        Params
        groupName: the caseunsensitive name.
        """

        for group in self.groups:
            if group.name.lower() == groupName.lower():
                return group.name 

    async def groupNameToID(self, groupName: str) -> int:
        group = await self.retrieveGroupName(groupName)
        return self.bridge.get_group_id_by_name(group)

    # Lights

    async def lightStatus(self, ctx, lightName: str) -> dict:
        light = await self.retrieveLightName(lightName)
        if light:
            return self.bridge.get_light(light)

        await self.bot.utils.sendEmbed(ctx, description=f'{self.bot.cross} **Light {lightName} doesn\'t exist.**')
        return False
        
    async def getLights(self, mode: str) -> dict:
        """
        Params

        mode: dictionary key by -> [name, id]
        """

        return self.bridge.get_light_objects(mode)
    
    async def getLightName(self, ctx, id: int) -> str:
        return self.bridge.get_light(id, 'name')
    
    async def turnLightOn(self, ctx, lightName: str) -> bool:
        light = await self.retrieveLightName(lightName)
        if light:
            self.bridge.set_light(light, 'on', True)
            await self.log(action=1, light=light)
            return True

        await self.bot.utils.sendEmbed(ctx, description=f'{self.bot.cross} **Light {lightName} doesn\'t exist.**')
        return False

    async def turnLightOff(self, ctx, lightName: str) -> bool:
        light = await self.retrieveLightName(lightName)
        if light:
            self.bridge.set_light(light, 'on', False)
            await self.log(action=2, light=light)
            return True
        
        await self.bot.utils.sendEmbed(ctx, description=f'{self.bot.cross} **Light {lightName} doesn\'t exist.**')
        return False

    async def lightBrightness(self, ctx, lightName: str, brightness: float) -> bool:
        light = await self.retrieveLightName(lightName)
        if light:
            self.bridge.set_light(light, 'bri', round(brightness))
            await self.log(action=4, light=light)
            return True
        
        await self.bot.utils.sendEmbed(ctx, description=f'{self.bot.cross} **Light {lightName} doesn\'t exist.**')
        return False

    async def lightColour(self, ctx, lightName: str, colours: list) -> bool:
        light = await self.retrieveLightName(lightName)
        if light:
            self.bridge.set_light(light, 'xy', colours)
            await self.log(action=3, light=light)
            return True

        await self.bot.utils.sendEmbed(ctx, description=f'{self.bot.cross} **Light {lightName} doesn\'t exist.**')
        return False

    # Light Groups

    async def getGroups(self) -> dict:
        return self.bridge.get_group()

    async def turnGroupOn(self, ctx, groupName: str) -> bool:
        group = await self.retrieveGroupName(groupName)
        if group:
            self.bridge.set_group(group, 'on', True)
            await self.log(action=5, light=group)
            return True

        await self.bot.utils.sendEmbed(ctx, description=f'{self.bot.cross} **Group {groupName} doesn\'t exist.**')
        return False

    async def turnGroupOff(self, ctx, groupName: str) -> bool:
        group = await self.retrieveGroupName(groupName)
        if group:
            self.bridge.set_group(group, 'on', False)
            await self.log(action=6, light=group)
            return True

        await self.bot.utils.sendEmbed(ctx, description=f'{self.bot.cross} **Group {groupName} doesn\'t exist.**')
        return False
    
    async def groupColour(self, ctx, groupName: str, colours: list) -> bool:
        group = await self.retrieveGroupName(groupName)
        if group:
            self.bridge.set_group(group, 'xy', colours)
            await self.log(action=7, light=group)
            return True

        await self.bot.utils.sendEmbed(ctx, description=f'{self.bot.cross} **Group {groupName} doesn\'t exist.**')
        return False

    async def groupBrightness(self, ctx, groupName: str, brightness: float) -> bool:
        group = await self.retrieveGroupName(groupName)
        if group:
            self.bridge.set_group(group, 'bri', round(brightness))
            await self.log(action=8, light=group)
            return True

        await self.bot.utils.sendEmbed(ctx, description=f'{self.bot.cross} **Group {groupName} doesn\'t exist.**')
        return False
    
    async def groupDelete(self, ctx, groupName: str) -> bool:
        groupID = await self.groupNameToID(groupName)

        if groupID:
            self.bridge.delete_group(groupID)
            return True
        
        await self.bot.utils.sendEmbed(ctx, description=f'{self.bot.cross} **Group {groupName} doesn\'t exist.**')
        return False
    
    # Scenes

    async def getScenes(self) -> dict:
        return self.bridge.get_scene()
    
    async def runScene(self, groupName: str, sceneName: str) -> bool:
        self.bridge.run_scene(group_name=groupName, scene_name=sceneName)
        return True