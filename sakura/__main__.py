import codecs
import click
import server
import scraper
import json


@click.command()
@click.argument('action')
@click.option('--move_date', help='expected date to movie in')
@click.option('--output', help='output folder for extracted data')
def main(action, move_date, output):

    if action == "dump":
        filename = "sakura-%s.json" % (move_date)
        print("dumping data: %s") % (filename)
        data = scraper.get_sakura_data(move_in_date=move_date)
        out = codecs.open(filename, 'w', 'utf-8')
        out.write(json.dumps(data))
        out.close()
        print("successfully dumped data at: %s" % filename)
    elif action == "server":
        server.run()

    else:
        print("please use a valid command.")


if __name__ == "__main__":
    main()
