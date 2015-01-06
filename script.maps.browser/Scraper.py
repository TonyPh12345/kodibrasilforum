import xbmc
import os
import sys
import time
import xbmcgui
import xbmcaddon
import xbmcvfs
import urllib
from default import dialog_select_UI
from ImageTags import *
from Utils import *
if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

__addon__ = xbmcaddon.Addon()
__addonid__ = __addon__.getAddonInfo('id')
__language__ = __addon__.getLocalizedString
__addonpath__ = __addon__.getAddonInfo('path')

Addon_Data_Path = os.path.join(xbmc.translatePath("special://profile/addon_data/%s" % __addonid__).decode("utf-8"))
googlemaps_key_normal = 'AIzaSyBESfDvQgWtWLkNiOYXdrA9aU-2hv_eprY'
googlemaps_key_streetview = 'AIzaSyCo31ElCssn5GfH2eHXHABR3zu0XiALCc4'
googlemaps_key_places = 'AIzaSyCgfpm7hE_ufKMoiSUhoH75bRmQqV8b7P4'
foursquare_id = "OPLZAEBJAWPE5F4LW0QGHHSJDF0K3T5GVJAAICXUDHR11GPS"
foursquare_secret = "0PIG5HGE0LWD3Z5TDSE1JVDXGCVK4AJYHL50VYTJ2CFPVPAC"
lastfm_apikey = '6c14e451cd2d480d503374ff8c8f4e2b'
factual_key = 'n1yQsp5q68HLgKSYkBmRSWG710KI0IzlQS55hOIY'
factual_secret = '8kG0Khj87JfcNiabqmixuQYuGgDUvu1PnWN5IVca'
wunderground_key = "xx"
max_limit = 25


# def GetRadarImage(self, lat, lon):
#     url = "http://api.wunderground.com/api/%s/animatedradar/image.gif?centerlat=%s&centerlon=%s&radius=100&width=280&height=280&newmaps=0" % (wunderground_key, str(self.lat), str(self.lon))
#     pass


def HandleLastFMEventResult(self, results):
    events = []
    if "events" in results and results['events'].get("event"):
        for event in results['events']['event']:
            artists = event['artists']['artist']
            if isinstance(artists, list):
                my_arts = ' / '.join(artists)
            else:
                my_arts = artists
            lat = ""
            lon = ""
            try:
                if event['venue']['location']['geo:point']['geo:long']:
                    lon = event['venue']['location']['geo:point']['geo:long']
                    lat = event['venue']['location']['geo:point']['geo:lat']
                    search_string = lat + "," + lon
                elif event['venue']['location']['street']:
                    search_string = urllib.quote_plus(event['venue']['location']['city'] + " " + event['venue']['location']['street'])
                elif event['venue']['location']['city']:
                    search_string = urllib.quote_plus(event['venue']['location']['city'] + " " + event['venue']['name'])
                else:
                    search_string = urllib.quote_plus(event['venue']['name'])
            except:
                search_string = ""
            googlemap = 'http://maps.googleapis.com/maps/api/staticmap?&sensor=false&scale=2&maptype=roadmap&center=%s&zoom=13&markers=%s&size=640x640&key=%s' % (search_string, search_string, googlemaps_key_old)
            event = {'date': event['startDate'],
                     'name': event['venue']['name'],
                     'id': event['venue']['id'],
                     'street': event['venue']['location']['street'],
                     'eventname': event['title'],
                     'website': event['website'],
                     'description': cleanText(event['description']),
                    # 'city': event['venue']['location']['postalcode'] + " " + event['venue']['location']['city'],
                     'city': event['venue']['location']['city'],
                     'country': event['venue']['location']['country'],
                     'geolong': event['venue']['location']['geo:point']['geo:long'],
                     'geolat': event['venue']['location']['geo:point']['geo:lat'],
                     'artists': my_arts,
                     'googlemap': googlemap,
                     'artist_image': event['image'][-1]['#text'],
                     'venue_image': event['venue']['image'][-1]['#text'],
                     'headliner': event['artists']['headliner']}
            events.append(event)
    else:
        log("Error in HandleLastFMEventResult. JSON query follows:")
     #   prettyprint(results)
    return events


def GetNearEvents(self, tag=False, festivalsonly=False):
    if festivalsonly:
        festivalsonly = "1"
    else:
        festivalsonly = "0"
    url = 'method=geo.getevents&festivalsonly=%s&limit=40' % (festivalsonly)
    if tag:
        url = url + '&tag=%s' % (urllib.quote_plus(tag))
    if self.lat:
        url = url + '&lat=%s&long=%s' % (self.lat, self.lon)  # &distance=60
    results = GetLastFMData(self, url)
    return self.CreateVenueList(results)


def CreateVenueList(self, results):
    PinString = ""
    letter = ord('A')
    count = 0
    events_list = list()
    if "events" in results and results['events'].get("event"):
        for event in results['events']['event']:
            artists = event['artists']['artist']
            if isinstance(artists, list):
                my_arts = ' / '.join(artists)
            else:
                my_arts = artists
            lat = ""
            lon = ""
            if event['venue']['location']['geo:point']['geo:long']:
                lon = event['venue']['location']['geo:point']['geo:long']
                lat = event['venue']['location']['geo:point']['geo:lat']
                search_string = lat + "," + lon
            elif event['venue']['location']['street']:
                search_string = event['venue']['location']['city'] + " " + event['venue']['location']['street']
            elif event['venue']['location']['city']:
                search_string = event['venue']['location']['city'] + " " + event['venue']['name']
            else:
                search_string = event['venue']['name']
            googlemap = 'http://maps.googleapis.com/maps/api/staticmap?&sensor=false&scale=2&maptype=roadmap&center=%s&zoom=13&markers=%s&size=640x640&key=%s' % (search_string, search_string, googlemaps_key_normal)
            item = xbmcgui.ListItem(event['venue']['name'])
            item.setProperty("date", event['startDate'])
            item.setProperty("name", event['venue']['name'])
            item.setProperty("id", event['startDate'])
            item.setProperty("street", event['venue']['location']['street'])
            item.setProperty("eventname", event['title'])
            item.setProperty("website", event['website'])
            item.setProperty("description", cleanText(event['description']))
            item.setProperty("city", event['venue']['location']['city'])
            item.setProperty("country", event['venue']['location']['country'])
            item.setProperty("lon", event['venue']['location']['geo:point']['geo:long'])
            item.setProperty("lat", event['venue']['location']['geo:point']['geo:lat'])
            item.setProperty("index", str(count))
            item.setProperty("artists", my_arts)
            item.setProperty("sortletter", chr(letter))
            item.setProperty("googlemap", googlemap)
            item.setProperty("artist_image", event['image'][-1]['#text'])
            item.setProperty("venue_image", event['venue']['image'][-1]['#text'])
            item.setProperty("headliner", event['artists']['headliner'])
            item.setArt({'thumb': event['venue']['image'][-1]['#text']})
            item.setLabel(event['venue']['name'])
            item.setLabel2(event['startDate'])
            events_list.append(item)
            PinString = PinString + "&markers=color:blue%7Clabel:" + chr(letter) + "%7C" + str(event['venue']['location']['geo:point']['geo:lat']) + "," + str(event['venue']['location']['geo:point']['geo:long'])
            count += 1
            letter += 1
            if count > max_limit:
                break
    else:
        log("Error when handling LastFM results")
    return events_list, PinString


def GetImages(self, path=""):
    self.PinString = "&markers=color:blue"
    letter = ord('A')
    count = 0
   # results = GetLastFMData(self,url)
    images_list = list()
    if True:
        for image in xbmcvfs.listdir(path):  # check that
            for test in image:
                try:
                    img = Image.open(path + test)
                    exif_data = get_exif_data(img)
                    lat, lon = get_lat_lon(exif_data)
                    if lat:
                        log(lat)
                        item = xbmcgui.ListItem(test)
                        item.setLabel(test)
                        item.setProperty("name", test)
                        item.setProperty("lat", str(lat))
                        item.setProperty("lon", str(lon))
                        item.setArt({'thumb': path + test})
                        images_list.append(item)
                        item.setProperty("index", str(count))
                        if len(self.PinString) < 1850:
                            self.PinString = self.PinString + "%7C" + str(lat) + "," + str(lon)
                            item.setProperty("sortletter", chr(letter))
                            letter += 1
                        count += 1
                except Exception as e:
                    log("Error when handling GetImages results")
                    log(e)
    else:
        log("Error when handling GetImages results")
    return images_list


def GetLastFMData(self, url="", cache_days=14):
    from base64 import b64encode
    filename = b64encode(url).replace("/", "XXXX")
    path = Addon_Data_Path + "/" + filename + ".txt"
    if xbmcvfs.exists(path) and ((time.time() - os.path.getmtime(path)) < (cache_days * 86400)):
        return read_from_file(path)
    else:
        url = 'http://ws.audioscrobbler.com/2.0/?api_key=%s&format=json&%s' % (lastfm_apikey, url)
        response = GetStringFromUrl(url)
        results = simplejson.loads(response)
        save_to_file(results, filename, Addon_Data_Path)
        return results


def GetEvents(self, id, pastevents=False):
    id = urllib.quote(id)
    if pastevents:
 #       url = 'method=artist.getpastevents&mbid=%s' % (id)
        url = 'method=artist.getpastevents&autocorrect=1&artist=%s' % (id)
    else:
  #      url = 'method=artist.getevents&mbid=%s' % (id)
        url = 'method=artist.getevents&autocorrect=1&artist=%s' % (id)
    results = GetLastFMData(self, url)
    try:
        return self.CreateVenueList(results)
    except:
        log("Error in GetEvents()")
        return []


def GetGoogleMapURLs(self):
    try:
        if self.aspect == "square":
            size = "640x640"
        else:
            size = "640x400"
        if self.lat and self.lon:
            self.search_string = str(self.lat) + "," + str(self.lon)
        else:
            self.search_string = urllib.quote_plus(self.search_string.replace('"', ''))
        base_url = 'http://maps.googleapis.com/maps/api/staticmap?&sensor=false&scale=2&'
        self.GoogleMapURL = base_url + 'maptype=%s&center=%s&zoom=%s&markers=%s&size=%s&key=%s' % (self.type, self.search_string, self.zoom_level, self.search_string, size, googlemaps_key_normal) + self.PinString
        zoom = 120 - int(self.zoom_level_streetview) * 6
        base_url = 'http://maps.googleapis.com/maps/api/streetview?&sensor=false&'
        self.GoogleStreetViewURL = base_url + 'location=%s&size=%s&fov=%s&key=%s&heading=%s&pitch=%s' % (self.search_string, size, str(zoom), googlemaps_key_streetview, str(self.direction), str(self.pitch))
        setWindowProperty(self.window, self.prefix + 'location', self.location)
        setWindowProperty(self.window, self.prefix + 'lat', str(self.lat))
        setWindowProperty(self.window, self.prefix + 'lon', str(self.lon))
        setWindowProperty(self.window, self.prefix + 'zoomlevel', str(self.zoom_level))
        setWindowProperty(self.window, self.prefix + 'direction', str(self.direction/18))
        setWindowProperty(self.window, self.prefix + 'type', self.type)
        setWindowProperty(self.window, self.prefix + 'aspect', self.aspect)
        setWindowProperty(self.window, self.prefix + 'map_image', self.GoogleMapURL)
        setWindowProperty(self.window, self.prefix + 'streetview_image', self.GoogleStreetViewURL)
        setWindowProperty(self.window, self.prefix + 'NavMode', "")
        setWindowProperty(self.window, self.prefix + 'streetview', "")
        if self.street_view:
            setWindowProperty(self.window, self.prefix + 'streetview', "True")
        if self.NavMode_active:
            setWindowProperty(self.window, self.prefix + 'NavMode', "True")
    except Exception as e:
        log(e)

# def GetBingMap(self):
   # # url = 'http://dev.virtualearth.net/REST/v1/Imagery/Map/AerialWithLabels/%s?mapSize=800,600&key=%s' % (urllib.quote(self.search_string),bing_key)
    # url = 'http://dev.virtualearth.net/REST/v1/Imagery/Map/AerialWithLabels/%.6f,%.6f/5?key=%s' % (self.lat,self.lon, bing_key)
   ##         'http://dev.virtualearth.net/REST/v1/Imagery/Map/AerialWithLabels/%.6f,%.6f/%i?fmt=%s&key=%s' % (self.lat, self.lon, self.zoom_level, self._format, bing_key)
    # log(url)
    # return url


def GetGeoCodes(self, show_dialog, search_string):
    try:
        search_string = urllib.quote_plus(search_string)
        url = 'https://maps.googleapis.com/maps/api/geocode/json?&sensor=false&address=%s' % (search_string)
        log("Google Geocodes Search:" + url)
        response = GetStringFromUrl(url)
        results = simplejson.loads(response)
        events = []
        for item in results["results"]:
            locationinfo = item["geometry"]["location"]
            search_string = str(locationinfo["lat"]) + "," + str(locationinfo["lng"])
            googlemap = 'http://maps.googleapis.com/maps/api/staticmap?&sensor=false&scale=1&maptype=roadmap&center=%s&zoom=13&markers=%s&size=640x640&key=%s' % (search_string, search_string, googlemaps_key_normal)
            event = {'generalinfo': item['formatted_address'],
                     'lat': str(locationinfo["lat"]),
                     'lon': str(locationinfo["lng"]),
                     'map': str(locationinfo["lng"]),
                     'preview': googlemap,
                     'id': item['formatted_address']}
            events.append(event)
        first_hit = results["results"][0]["geometry"]["location"]
        if show_dialog:
            if len(results["results"]) > 1:  # open dialog when more than one hit
                w = dialog_select_UI('DialogSelect.xml', __addonpath__, listing=events)
                w.doModal()
                log(w.lat)
                return (w.lat, w.lon)
            elif len(results["results"]) == 1:
                return (first_hit["lat"], first_hit["lng"])  # no window when only 1 result
            else:
                return (self.lat, self.lon)  # old values when no hit
        else:
            return (first_hit["lat"], first_hit["lng"])
    except Exception as e:
        log(e)
        return ("", "")


def GetLocationCoordinates(self):
    try:
        url = 'http://www.telize.com/geoip'
        response = GetStringFromUrl(url)
        results = simplejson.loads(response)
        self.lat = results["latitude"]
        self.lon = results["longitude"]
    except Exception as e:
        log(e)


def GetPlacesList(self):
    ################### code based on script.maps by a.a.alsaleh. credits to him.
    url = 'https://api.foursquare.com/v2/venues/search?ll=%.8f,%.8f&limit=50&client_id=%s&client_secret=%s&v=20130815' % (self.lat, self.lon, foursquare_id, foursquare_secret)
  #  url = 'https://api.foursquare.com/v2/venues/search?ll=%.6f,%.8f&query=%s&limit=50&client_id=%s&client_secret=%s&v=20130815' % (self.lat, self.lon, "Food", foursquare_id, foursquare_secret)
   # url = 'https://api.foursquare.com/v2/venues/explore?ll=%.8f,%.8f&section=%s&limit=50&client_id=%s&client_secret=%s&v=20130815' % (self.lat, self.lon, "topPicks", foursquare_id, foursquare_secret)
    log(url)
    response = GetStringFromUrl(url)
    results = simplejson.loads(response)
    prettyprint(results)
    places_list = list()
    self.PinString = ""
    letter = ord('A')
    count = 0
    if True:
        if results and 'meta' in results:
            if results['meta']['code'] == 200:
                for v in results['response']['venues']:
                    p = {'id': v['id'], 'name': v['name'], 'distance': v['location']['distance'], 'comments': v['stats']['tipCount'], 'visited': v['stats']['usersCount']}
                    if 'formattedAddress' in v['location']:
                        p['address'] = "aa"
                    if 'phone' in v['contact']:
                        p['phone'] = v['contact']['phone']
                    if 'twitter' in v['contact']:
                        p['phone'] = v['contact']['twitter']
                             # create a list item
                    item = xbmcgui.ListItem(v['name'])
                    item.setProperty("id", str(v['id']))
                    item.setProperty("lat", str(v['location']['lat']))
                    item.setProperty("lon", str(v['location']['lng']))
                    self.PinString = self.PinString + "&markers=color:blue%7Clabel:" + chr(letter) + "%7C" + str(v['location']['lat']) + "," + str(v['location']['lng'])
                    try:
                        icon = v['categories'][0]['icon']['prefix'] + "88" + v['categories'][0]['icon']['suffix']
#                        if count < 12:
                   #     self.PinString = self.PinString + "&markers=icon:" + v['categories'][0]['icon']['prefix'] + "64" +  v['categories'][0]['icon']['suffix'] + "|" + str(v['location']['lat']) + "," + str(v['location']['lng'])
                    #    self.PinString = self.PinString + "&markers="+ str(v['location']['lat']) + "," + str(v['location']['lng'])
                    #
                    except Exception as e:
                        icon = ""
                        log("Error: Exception in GetPlacesList with message:")
                        log(e)
                    item.setArt({'thumb': icon})
                    item.setLabel(v['name'])
                    item.setLabel2(v['name'])
                    item.setProperty("name", v['name'])
                    item.setProperty("index", str(count))
                    item.setProperty("sortletter", chr(letter))
                    item.setProperty("eventname", ', '.join(filter(None, v['location']['formattedAddress'])))
                    item.setProperty("Venue_Image", icon)
                    item.setProperty("GoogleMap", icon)
                    places_list.append(item)
                    count += 1
                    letter += 1
                    if count > max_limit:
                        break
            elif results['meta']['code'] == 400:
                log("LIMIT EXCEEDED")
            else:
                log("ERROR")
        else:
            log("ERROR")
    else:
        log("ERROR")
    return places_list


def GetPlacesListExplore(self, placetype):
   # url = 'https://api.foursquare.com/v2/venues/search?ll=%.8f,%.8f&limit=50&client_id=%s&client_secret=%s&v=20130815' % (self.lat, self.lon, foursquare_id, foursquare_secret)
  #  url = 'https://api.foursquare.com/v2/venues/search?ll=%.6f,%.8f&query=%s&limit=50&client_id=%s&client_secret=%s&v=20130815' % (self.lat, self.lon, "Food", foursquare_id, foursquare_secret)
    url = 'https://api.foursquare.com/v2/venues/explore?ll=%.8f,%.8f&section=%s&limit=25&venuePhotos=1&client_id=%s&client_secret=%s&v=20130815' % (self.lat, self.lon, placetype, foursquare_id, foursquare_secret)
    log(url)
    response = GetStringFromUrl(url)
    results = simplejson.loads(response)
   # prettyprint(results)
    places_list = list()
    self.PinString = ""
    letter = ord('A')
    count = 0
    if results and 'meta' in results:
        if results['meta']['code'] == 200:
            for v in results['response']['groups'][0]['items']:
                if True:
                    item = xbmcgui.ListItem(v['venue']['name'])
                    icon = v['venue']['categories'][0]['icon']['prefix'] + "88" + v['venue']['categories'][0]['icon']['suffix']
                    try:
                        photo_node = v['venue']['photos']['groups'][0]['items'][0]
                        photo = photo_node['prefix'] + str(photo_node['height']) + photo_node['suffix']
                    except:
                        photo = ""
                    item.setArt({'thumb': photo})
                    item.setArt({'icon': icon})
                    item.setLabel(v['venue']['name'])
                    item.setProperty('name', v['venue']['name'])
                    item.setLabel2(v['venue']['categories'][0]['name'])
                    item.setProperty("sortletter", chr(letter))
                    item.setProperty("index", str(count))
                    item.setProperty("Venue_Image", photo)
                    address = "[CR]".join(v['venue']['location']['formattedAddress'])
                    item.setProperty("description", address)
                    item.setProperty("lat", str(v['venue']['location']['lat']))
                    item.setProperty("lon", str(v['venue']['location']['lng']))
                    self.PinString = self.PinString + "&markers=color:blue%7Clabel:" + chr(letter) + "%7C" + str(v['venue']['location']['lat']) + "," + str(v['venue']['location']['lng'])
                    places_list.append(item)
                    count += 1
                    letter += 1
                    if count > max_limit:
                        break
          #  difference_lat = results['response']['suggestedBounds']['ne']['lat'] - results['response']['suggestedBounds']['sw']['lat']
           # difference_lon = results['response']['suggestedBounds']['ne']['lng'] - results['response']['suggestedBounds']['sw']['lng']
           # log(difference_lat)
        elif results['meta']['code'] == 400:
            log("LIMIT EXCEEDED")
        else:
            log("ERROR")
    else:
        log("ERROR")
    return places_list


def GetGooglePlacesList(self, locationtype):
    location = str(self.lat) + "," + str(self.lon)
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s&types=%s&radius=500&key=%s' % (location, locationtype, googlemaps_key_places)
    log(url)
    response = GetStringFromUrl(url)
    results = simplejson.loads(response)
    places_list = list()
    PinString = ""
    letter = ord('A')
    count = 0
    if "results" in results:
        if True:
            for v in results['results']:
                item = xbmcgui.ListItem(v['name'])
                try:
                    photo_ref = v['photos'][0]['photo_reference']
                    photo = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=%s&key=%s' % (photo_ref, googlemaps_key_places)
                except:
                    photo = ""
                typestring = ""
                typestring = " / ".join(v['types'])
                item.setArt({'thumb': photo})
                item.setArt({'icon': v['icon']})
                item.setLabel(v['name'])
                item.setProperty('name', v['name'])
                item.setProperty('description', v['vicinity'])
                item.setLabel2(typestring)
                item.setProperty("sortletter", chr(letter))
                item.setProperty("index", str(count))
                lat = str(v['geometry']['location']['lat'])
                lon = str(v['geometry']['location']['lng'])
                item.setProperty("lat", lat)
                item.setProperty("lon", lon)
                item.setProperty("index", str(count))
                if "rating" in v:
                    rating = str(v['rating']*2.0)
                    item.setProperty("rating", rating)
                PinString = PinString + "&markers=color:blue%7Clabel:" + chr(letter) + "%7C" + lat + "," + lon
                places_list.append(item)
                count += 1
                letter += 1
                if count > max_limit:
                    break
          #  difference_lat = results['response']['suggestedBounds']['ne']['lat'] - results['response']['suggestedBounds']['sw']['lat']
           # difference_lon = results['response']['suggestedBounds']['ne']['lng'] - results['response']['suggestedBounds']['sw']['lng']
           # log(difference_lat)
        elif results['meta']['code'] == 400:
            log("LIMIT EXCEEDED")
        else:
            log("ERROR")
    else:
        log("ERROR")
    return PinString, places_list
