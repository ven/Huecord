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

## Setup

- `$ git clone https://github.com/venoras/Huecord`
- Modify the `config.example.py` with the relevant parameters, and rename it to `config.py`.
- To find your **Hue Bridge IP**, click **[here](https://discovery.meethue.com)** and copy the `Internal IP Address` value.
- To run the bot, use `python3 launcher.py`. If it is your first time running the bot, ensure you have pushed the **sync button** on your **Hue Bridge** prior to launching it.

## Configuration

If you'd like the commands to be executable by any user, modify `owner_only` in `config.py` to `False`.
