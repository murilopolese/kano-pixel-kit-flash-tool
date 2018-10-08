# Pixel Kit Flash Tool

![](https://i.imgur.com/x1J3YPM.png)

This is a very simple tool to flash your Pixel Kit with the Kano Code firmware (factory firmware) and MicroPython.

## Download

Check the [releases page](https://github.com/murilopolese/kano-pixel-kit-flash-tool/releases).

## Features

- Recognise Pixel Kits connected over USB (refresh ports).
- Flash Kano Code (factory firmware).
- Flash MicroPython with all the libraries and documentation needed. Check [pixel32](http://github.com/murilopolese/pixel32) for more information.

## MicroPython firmware

The MicroPython firmware comes with all the libraries and documentation you need to start coding your Pixel Kit only with your browser. To read more about that, check [pixel32](http://github.com/murilopolese/pixel32).

## Kano Code firmware

Kano Code firmware is what makes your Pixel Kit able to interact with the [Kano Code App](https://kano.me/landing/app/uk).

## Building

### MacOS

1. Make sure you have Python 3 and pip installed
1. Run `pip install --user -r requirements.txt`
1. Run `python setup.py macos`
