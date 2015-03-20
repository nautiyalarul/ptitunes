# Quick introduction the project #

### Some screenshots & videos ###
#### PC-side screenshots ####

#### Boards screenshots ####

#### Videos of our device running ####

# Available documentation #

## Introduction to the project ##

## PC Software Design ##

The PC software is made up of a GUI + 2 daemons (USB and DCOM or DBUS) has a cross-platform-friendly design.

### General UML diagram ###


### Graphical User Interface ###
This interface is made in Java Swing(?) and shows in real time the finger position on the plugged device's sensors as well as the gestures that have recognized on the OS side thanks to packet filtering.

#### GUI Features ####
**1. Display of daemons states**
Show status of connections with the DCOM/DBUS application and with the USB device with text.
Statuses are:
  1. Unplugged, (icon theme: gtk-no)
  1. Plugged, (icon theme: gtk-yes).

**2. Display of click wheel**
Have a nice non-clickable image with 8-spots corresponding to our 8 buttons changing aspect when pressed... Have

Python + QT4 + SVG for the click wheel canvas
we keep the main UI
we do DBUS for Linux (MPRIS protocol) & COM for Windows

Qt Svg drawing things with different colors (chess example)
http://forum.qtfr.org/viewtopic.php?id=7269

MPRIS for several media players
http://wiki.xmms2.xmms.se/wiki/MPRIS#D-Bus
http://wiki.xmms2.xmms.se/wiki/Media_Player_Interfaces#About_MPRIS
Projects involved
> XMMS2
For XMMS2, a proxy could be developed to translate between DBUS and XMMS2's own  IPC mechanism. (Anders may have already done some work on this)
> BMPx
> VLC
> Amarok
> Audacious
> Dragon player


**2. Disabling of view if no USB device found**

**3.**

### Multimedia playback controller daemon ###
It is made in Java and uses the for sending playback commands:
  * over COM/DCOM on Windows to iTunes thanks to the libjacob library
  * over DBus on Linux to control Rhythmbox (or Amarok.. undetermined for now...).

### USB/COM3 monitoring ###
This part is made in Java or C interfaced through JNI (Java Native Interface).
Our sensor device is plugged over regular USB into the computer and has a special well-spread driver virtually mapping it to COM3 on the OS side which makes that the usual PC software tools for serial communication can be used.
This is of use thanks to the driver comes from the technological choice made to use and ft245r USB FIFO on the device's board.

## Microcontroller design ##
### Microcontroller software design ###
### Microcontroller hardware design ###