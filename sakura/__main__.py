import codecs
import click
import server
import scraper
import json


@click.command()
@click.argument('action')
@click.option('--move_date', help='expected date to movie in. i.e: 2016/10/28')
@click.option('--output', help='output folder for extracted data')
def main(action, move_date, output):

    if action == "dump":
        output_path = "sakura-%s.json" % (move_date.replace("/", "-"))
        print("dumping data: %s" % output_path)
        data = scraper.get_sakura_data(move_in_date=move_date)
        out = codecs.open(output_path, 'w', 'utf-8')
        out.write(json.dumps(data))
        out.close()
        print("successfully dumped data at: %s" % output_path)
    elif action == "server":
        server.run()

    else:
        print("please use a valid command.")
        click.echo(click.get_current_context().get_help()) 
        


if __name__ == "__main__":
    main()
