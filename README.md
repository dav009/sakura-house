# Sakura-House

So you are looking for a new place to live via [Sakura House](https://www.sakura-house.com).
Chances are you are new to Tokyo, and You are struggling to compare properties locations and prices,
and probably you ended up with lots of tabs (at least 3,4 tabs per property)

This project lets you scrape the property data out of Sakura House given a starting renting day.
It also visualizes it on google maps.


# Installation

- `python3.4`
- `lxml`
- `pip install -r requirements.txt`


# how to ?

## Scraping & Vissualizing
- create a `config.json` and place your `GOOGLE MAPS API KEY` : `{"GOOGLE_MAPS_API_KEY":"your key"}`
- `python3 server.py`
- `http://localhost:5000` will visualize properties with availability by the current daye
- `http://localhost:5000/?date=2017/05/12` will visualize properties with availability by the given date

- data will be saved at `static/sakura-DATE.json`


## Just Scraping



Note: This might take a while as the scraper pulls data from sakura-house. This is slow by default to prevent hitting the website too hard.



