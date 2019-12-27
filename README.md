# 💡 Huecord

<p align="left">
    <img src="https://img.shields.io/github/last-commit/venoras/Huecord">
</p>

**A lightweight Discord bot for interacting with Philips Hue lights. Built using [discord.py](https://github.com/Rapptz/discord.py) and [pHue](https://github.com/studioimaginaire/phue).**

## Features

- Enable and disable lights, light groups and scenes.
- Modify groups and scenes.
- Manage brightness, colour and view individual light statuses.
- Bridge configuration information.

## Dependencies

- [discord.py](https://github.com/Rapptz/discord.py)
- [pHue](https://github.com/studioimaginaire/phue)
- [Jishaku](https://github.com/gorialis/jishaku)

## Setup

1. Clone this repository: `$ git clone https://github.com/venoras/Huecord`

2. Run `pip3 install -r requirements.txt` to install all dependencies.

3. Modify the `config.example.py` with the relevant parameters, and rename it to `config.py`.

    1. Go to [Discord Developers](https://discordapp.com/developers) and create a **New Application**. Navigate to **Bot**, and click **Add Bot**. Paste the **token** into the configuration file.

    2. To find your **Discord User ID**, right click your profile and click **Copy ID**. Developer Mode must be enabled in `Settings -> Appearance`. Paste this ID into `owner_id` in the configuration file.

    3. To find your **Hue Bridge IP**, click **[here](https://discovery.meethue.com)** and copy the `Internal IP Address` value.

4. To run the bot, use `python3 launcher.py`. If it is your first time running the bot, ensure you have pushed the **sync button** on your **Hue Bridge** prior to launching it.

## Configuration

- If you'd like the commands to be executable by any user, modify `owner_only` in `config.py` to `False`.
