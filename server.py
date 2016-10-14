from flask import Flask, render_template, request  
import json
import scraper
import os
import codecs
import time
app = Flask(__name__)

CONFIG = json.load(open('config.json', 'r'))
GOOGLE_MAPS_API_KEY = CONFIG['GOOGLE_MAPS_API_KEY']


def get_or_show(date, max_price=1000000000):
    # data for an specific starting date is cached
    data_file_name = 'static/sakura-%s.json' % (date.replace("/", "_"))
    if (os.path.exists(data_file_name)):
        data = json.load(open(data_file_name, 'r'))
        print(data)
    else:
        # if it is not cached fetch it, this take time.
        print("fetching data..")
        data = scraper.get_sakura_data(date)
        print("finished fetching data..")
        out = codecs.open(data_file_name, 'w', 'utf-8')
        out.write(json.dumps(data))
        out.close()

    return render_template('index.html', sakura_data=data,
                           google_maps_api_key=GOOGLE_MAPS_API_KEY,
                           date=date)


@app.route('/')
def index():
    date = request.args.get('date', '')
    if not date:
        today = time.strftime("%Y/%m/%d")
        date = today
    return get_or_show(date)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
