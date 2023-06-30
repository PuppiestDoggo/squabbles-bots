import requests

def fetch_data(url):
    response = requests.get(url)
    data = response.json()
    return data['data']

def get_urls(data):
    return [item['url'] for item in data['links'] if item['url'] is not None]

def print_data(data):
    print("\n\n".join(["Url: {}\nContent: {}".format(item['url'], item['content']) for item in data]))

def posts(name):
    response = requests.get("https://squabbles.io/api/user/{}/posts".format(name))
    data = response.json()
    urls = get_urls(data)
    all_data = [item for url in urls for item in fetch_data(url)]
    print_data(all_data)

def comments(name):
    response = requests.get("https://squabbles.io/api/user/{}/comments".format(name))
    data = response.json()
    urls = get_urls(data)
    all_data = [item for url in urls for item in fetch_data(url)]
    print_data(all_data)

if __name__ == '__main__':
    posts('USER')
    comments('USER')
