import asyncio
from bot import Huecord
from phue import Bridge, PhueRegistrationException

async def retrieve_bot(loop):
    return Huecord(loop=loop)

def run_bot():
    loop = asyncio.get_event_loop()
    bot = loop.run_until_complete(retrieve_bot(loop))
    bot.run()

if __name__ == "__main__":
    connected = False

    while not connected:

        try: # attempt to connect to bridge, start bot if successful.
            bridge = Bridge('192.168.0.2') 
            connected = True
            print(f"✅ Hue Bridge on {bridge.ip} successfully connected.")
            run_bot()

        except PhueRegistrationException as e: # if bridge can't be connected to, repeat process
            print(f"\n❌ Connection failed. The Hue Bridge sync button must be pressed (within 30 seconds) in order for a connection to the Bridge to be established.\n")
            choice = str(input("🔄 Would you like to try again? (y/n)\n\n")).upper()

            if choice not in ['Y', 'YES']:
                break