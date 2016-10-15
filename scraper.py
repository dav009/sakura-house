import requests
from lxml.cssselect import CSSSelector
from lxml import html
import re

BASE_URL = "https://www.sakura-house.com"
SEARCH_URL = BASE_URL + "/en/search/search?authenticity_token=27rK+vjqpcyEZ2oexbeeL4ZVhHkHHycYBrgAL70KXvI=&page={current_page}&move_in_date={move_in_date}&price_min={price_min}&price_max={price_max}&building_id=&train=&show_all="


def extract_digits(string):
    """
    extracts numbers out of a string
    """
    price = "-1"
    try:
        price = re.findall("(\d+)", string.replace(",", ""))[0]
    except Exception:
        print("\tcouldnt find price")
    return price


def get_html_content(url):
    """
    fetches and parses the html content of an url
    """
    content = html.fromstring(get_content(url))
    return content


def get_content(url):
    """
    fetches the content from an url
    """
    r = requests.get(url)
    content = ""
    if r.status_code == 200:
        try:
            content = r.text
        except Exception as e:
            print("error while fetching page : %s -> %s" % (url, e))
    return content


def extract_info(property_url):
    """
    returns a dictionary with information about a property.
    Location, price, URL, property type
    """

    def extract_subproperties(property_url):
        html_content = get_html_content(property_url)
        doc_tags = CSSSelector(".unitInner .set .doc")(html_content)

        def extract_info_from_doc_tag(html_tag):
            price_tag = CSSSelector("h5")(html_tag)[0]
            price = extract_digits(price_tag.text)
            property_type = CSSSelector(".detail .style")(html_tag)[0].text_content()
            sub_property = {"price": price, "type": property_type}
            return sub_property
            
        subproperties = [extract_info_from_doc_tag(tag) for tag in doc_tags]
        return subproperties

    def extract_location(property_url):
        maps_location_regex = r'new google\.maps\.LatLng\(([\d \. \, \ ]+)\)'
        english_base_url = "https://www.sakura-house.com/en/"
        property_id = property_url.split(english_base_url)[1].split("/")[0]
        location_url = english_base_url + property_id + "/access"
        location_page_text = get_content(location_url)
        location = re.findall(maps_location_regex, location_page_text)[0].split(',')
        return {'lat': float(location[0]), 'lng': float(location[1])}
        
    
    subproperties = {'subproperties': extract_subproperties(property_url)}
    subproperties['location'] = extract_location(property_url)
    subproperties['url'] = property_url
    return subproperties
    
def extract_properties(move_in_date, price_min, price_max):   

    def format_url(page):
        data = {'current_page': page,
                'move_in_date': move_in_date,
                'price_min': price_min,
                'price_max': price_max}
        url = SEARCH_URL.format(**data)
        return url

    def extract_property_urls(html_content):
        """
        extracts the property urls from the html of a search page
        """
        property_anchors = CSSSelector(".box .boxInner .propertySet h2 a")(html_content)
        property_links = list([BASE_URL + anchor.get('href') for anchor in property_anchors])
        return property_links

    def extract_number_of_pages(html_content):
        """
        extracts the number of pages in a search page
        """
        items = CSSSelector(".pagination li")(html_content)
        pages = len(items) - 4
        if pages < 0:
            pages = 0
        return pages

    def get_search_pages_content(current_page=1):
        """
        get the html content of search pages
        """
        content = list()
        url = format_url(current_page)
        current_page_content = get_html_content(url)
        number_of_pages = extract_number_of_pages(current_page_content)
        print("fetching search page : %s out of %s" % (current_page, number_of_pages))
        if current_page_content:
            content.append(current_page_content)
        if number_of_pages <= current_page:
            return content
        else:
            return content + get_search_pages_content(current_page + 1)

    search_pages_content = get_search_pages_content()

    list_of_properties = list()
    for search_page_content in search_pages_content:
        current_page_properties = extract_property_urls(search_page_content)
        list_of_properties = list_of_properties + current_page_properties
    return list_of_properties


def get_sakura_data(move_in_date, price_min="", price_max=""):
    """
    given a move_in_date fetches the search pages and all the properties matching that criteria
    """
    
    properties_urls = extract_properties(move_in_date=move_in_date,
                                         price_min=price_min,
                                         price_max=price_max)
    data = list()
    total_urls = len(properties_urls)
    for index, property_url in enumerate(properties_urls):
        print("%s out of %s, fetching: %s" % (index, total_urls, property_url))
        data.append(extract_info(property_url))
    return data
