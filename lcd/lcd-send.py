import dbus
import feedparser
import time
from futures import Future

hit_list = [ "http://rss.cnn.com/rss/edition.rss", "http://feeds.bbci.co.uk/news/rss.xml?edition=int", "http://feeds.huffingtonpost.com/huffingtonpost/LatestNews" ] # list of feeds to pull down

# pull down all feeds
future_calls = [Future(feedparser.parse,rss_url) for rss_url in hit_list]
# block until they are all in
feeds = [future_obj() for future_obj in future_calls]

bus = dbus.SystemBus()
helloservice = bus.get_object('com.svesoftware.raspberry.lcd', '/com/svesoftware/raspberry/lcd')
hello = helloservice.get_dbus_method('draw', 'com.svesoftware.raspberry.lcd')

entries = []
for feed in feeds:
    entries.extend( feed[ "items" ] )

print(entries)
sorted_entries = sorted(entries, key=lambda entry: entry["published_parsed"])
sorted_entries.reverse() # for most recent entries first

for item in sorted_entries:
        print(len(item["title"]))
        print(hello(item["title"], 'a'))
#        print(hello('hi, how are you?'))
print("Over and out")
