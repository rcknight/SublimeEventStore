SublimeEventStore
=================

A plugin to allow editing of your Event Store (http://GetEventStore.com) projections in Sublime Text 2

No more copying and pasting!

###Installation

Available in [Sublime Package Control](http://wbond.net/sublime_packages/package_control) as "Event Store Projection Editor"
 (reccomended, you will receive automatic updates)


Alternatively, you can clone this repo into your *Sublime Text 2/Packages*

*Windows*
```shell
cd c:/Users/john.smith/AppData/Roaming/Sublime\ Text\ 2/Packages/
git clone git@github.com:rcknight/SublimeEventStore.git
```

*OSX*
```shell
cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/
git clone git@github.com:rcknight/SublimeEventStore.git
```

*Ubuntu*
```shell
cd ~/.config/sublime-text-2/Packages
git clone git@github.com:rcknight/SublimeEventStore.git
```

###Usage

The plugin can be accessed via the Tools menu, or the Command Palette

The default keybindings are:

```ctrl+e, ctrl+o``` to open a projection from the Event Store

```ctrl+e, ctrl+s``` to save a projection to the Event Store

When a new projection is saved, it is given the same name as the file it came from.

###Settings

By default the event store URL used is http://127.0.0.1:2113
You can change this by edditing the file EventStore.sublime-settings in the package directory
![GAProxy analytics](http://localhost:57290/UA-40151795-1/woftam1/woftam2)
