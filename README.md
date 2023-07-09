# scrapers
Various web to json scraper scripts - intended to be used along side of Thomas J's AllSky via CRONTAB

I'm not a dedicated coder - a lot of my scripting capabilities come from tiral & error, google searches, stackExchange, and other sources. I know they can be cleaned up and streamlined better, but I don't have the know-how to do so (yet?).

# bme280_csv_logger.py
a simple logger script for AdaFruit's BME280 chip. 
* Reads chip
* Formats and stores data in CSV file
* ~ Also stores data in .json file for use in Thomas J's AllSky to use in its overlay editor.

# scrape_swx.py
Web-scraper to query available live satellite data to format and store in .json format for use with AllSky's overlay editor.

# scrape_wx.py
Web-scraper that uses Visual Crossing's API to get local weather data, and also has functionality for using (downloaded) visual graphics for AllSky's Overlay editor

# Notes
If there are glaring issues - please let me know and I'll see what I can do to fix them. 
- Some errors do still come up from time to time on my system, slowly trying to tackle them as they arrise, and as I find solutions.
