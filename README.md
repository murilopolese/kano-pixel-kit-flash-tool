# Pixel Kit Flash Tool

![](https://i.imgur.com/x1J3YPM.png)

This is a very simple tool to flash your Pixel Kit with the [Kano Code](https://kano.me/landing/app/uk) firmware (factory firmware) and [MicroPython](https://micropython.org) (with [pixel32](http://github.com/murilopolese/pixel32)).

## Download

Check the [releases page](https://github.com/murilopolese/kano-pixel-kit-flash-tool/releases).

## Features

- Recognise Pixel Kits connected over USB (refresh ports).
- Flash Kano Code (factory firmware).
- Flash MicroPython and [Pixel32](http://github.com/murilopolese/pixel32) to your board.

## MicroPython firmware

Pixel32 is a MicroPython application that allows it to be programmed on the browser, offline and with built in documentation. To read more about that, check [Pixel32](http://github.com/murilopolese/pixel32).

## Kano Code firmware

Kano Code firmware is what makes your Pixel Kit able to interact with the [Kano Code App](https://kano.me/landing/app/uk).

## Building

1. Make sure you have Python 3 and pip installed
1. Run `python -m venv venv` and `. venv/bin/activate`
1. Run `pip install -r requirements.txt`
1. Run `./build_macos.sh`, `./build_linux.sh` or `./build_win.bat`


## I want more!!

If you are looking at a more complete, flexible yet still friendly way to flash your Pixel Kit I can't recommend [the `nodemcu-pyflasher` project](https://github.com/marcelstoer/nodemcu-pyflasher) enough.

If you are not afraid of command line, perhaps even the [esptool](https://github.com/espressif/esptool) itself?

All you will need to do is to find or build a suitable firmware for ESP32. Here is a list of places you might find it:

- [MicroPython](https://micropython.org/download#esp32)
- [LuaNode](https://github.com/Nicholas3388/LuaNode)
- [Espruino (javascript)](https://www.espruino.com/)
- [BASIC](https://hackaday.com/2016/10/27/basic-interpreter-hidden-in-esp32-silicon/)
