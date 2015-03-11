Trakt.tv scrobbler and library sync
==============================================

###What is Trakt?
Automatically scrobble all TV episodes and movies you are watching to Trakt.tv! Keep a comprehensive history of everything you've watched and be part of a global community of TV and movie enthusiasts. Sign up for a free account at [Trakt.tv](http://trakt.tv) and get a ton of features:

* Automatically scrobble what you're watching
* [Mobile apps](http://trakt.tv/downloads) for iPhone, iPad, Android, and Windows Phone
* Share what you're watching (in real time) and rating to facebook and twitter
* Personalized calendar so you never miss a TV show
* Follow your friends and people you're interesed in
* Use watchlists so you don't forget what to watch
* Track your media collections and impress your friends
* Create custom lists around any topics you choose
* Easily track your TV show progress across all seasons and episodes
* Track your progress against industry lists such as the IMDb Top 250
* Discover new shows and movies based on your viewing habits
* Widgets for your forum signature

###What can this addon do?
* Automatically scrobble TV episodes and movies you are watching 
* Sync your TV episode and movie collections to Trakt (manually or triggered by a library update)
* Keep watched statuses synced between Kodi and Trakt
* Rate movies and episodes after watching them
* Custom skin/keymap actions for toggling watched status, and rating (tagging and listing disabled for now)

###What can be scrobbled?
This plugin will scrobble local media and most remote streaming content. Local media should be played in Kodi library mode and you should use [TVDb](http://thetvdb.com/) (for tv shows) and [TMDb](http://themoviedb.org) (for movies) as your scrapers. TV shows are identified using their TVDb ID. Movies are identified using the IMDb ID. This allows Trakt to match the correct show or movie more accurately, regardless of the title.

Remote streaming content will scrobble assuming the metadata is correctly set in Kodi. Add-ons that stream content need to correctly identify TV episodes and movies with as much metadata as possible for Trakt to know what you're watching.

###Installation
1. Download the zip ([download it here](../../zipball/master))
2. Install script.trakt by zip. Go to *Settings* > *Add-ons* > *Install from zip file* > Choose the just downloaded zip
3. Navigate to *Settings* > *Add-ons* > *Enabled add-ons* > *Services* > **Trakt**
4. Select *Trakt* and go to **Configure**
5. Enter your **username** and **password**, change any other settings as needed
6. Select **OK** to save your settings
7. Watch something and see it show up on Trakt.tv!

or

1. Clone this repository (or [download it here](../../zipball/master)) into a folder called **script.trakt** inside your Kodi **addons** folder
2. Start Kodi (or restart if its already running)
3. Make sure you have the modules Trakt and dateutil installed. Check under *Settings* > *Add-ons* > *Get Add-ons* > *All Add-ons* > *Add-on libraries* (restart if you had to install these)
4. Navigate to *Settings* > *Add-ons* > *Enabled add-ons* > *Services* > **Trakt**
5. Select *Trakt* and go to **Configure**
6. Enter your **username** and **password**, change any other settings as needed
7. Select **OK** to save your settings
8. Watch something and see it show up on Trakt.tv!

###Problems?
####"I found something that doesn't work"
* Search the issues on github to see if it has already been reported, if so add your information there.
* If not, create a new issue and provide as much data about your system as possible, a logfile will also be needed.

####Creating logfiles
* To create a logfile, enable the debug setting in Kodi AND script.trakt, otherwise the logfile won't show any data from script.trakt. Check the Kodi documentation if you don't know where your logfile can be found.

###Contribute

####Pull requests
* Please make your pull requests on the branch named "dev" only.

####Translations
* Translations are done via the Transifex project of Kodi. If you want to support translation efforts, read [this] (http://kodi.wiki/view/Translation_System) and look for script-trakt under the XBMC Addons project in Transifex.

###Thanks
* Special thanks to all who contribute to this plugin! Check the commit history and changelog to see these talented developers.
* Special thanks to fuzeman for [trakt.py] (https://github.com/fuzeman/trakt.py).
