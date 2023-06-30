import json
import requests

profanities = {
    "anus": 0,
    "ass": 0,
    "asshole": 0,
    "bastard": 0,
    "bitch": 0,
    "bullshit": 0,
    "crap": 0,
    "cum": 0,
    "dick": 0,
    "fucker": 0,
    "fucking": 0,
    "fuck": 0,
    "pissed": 0,
    "shitty": 0,
    "shit": 0,
    "tits": 0,
}


def fetch_data(url):
    if url:
        response = requests.get(url)
        return response.json()['data']
    return []


def get_urls(data):
    return [item['url'] for item in data['links'] if item.get('url')]


def count_profanities(content):
    for profanity in profanities:
        profanities[profanity] += content.count(profanity)


def find_profanities(name, endpoint):
    response = requests.get(f"https://squabbles.io/api/user/{name}/{endpoint}")
    data = response.json()
    urls = get_urls(data)
    for url in urls:
        posts_data = fetch_data(url)
        for item in posts_data:
            content = item.get('content', '').lower()
            count_profanities(content)


def generate_markdown_table(profanities):
    table = "| Profanity | Count |\n"
    table += "| --------- | ----- |\n"
    for profanity, count in profanities.items():
        if count > 0:
            table += f"| {profanity} | {count} |\n"
    return table


def find_and_send_profanities(name, location, authorization):
    find_profanities(name, 'posts')
    find_profanities(name, 'comments')

    total_profanities = sum(profanities.values())

    if total_profanities > 0:
        sorted_profanities = {k: v for k, v in sorted(profanities.items(), key=lambda item: item[1], reverse=True)}
        table = generate_markdown_table(sorted_profanities)
        send_comment(location, authorization, table)
    else:
        print(f"No profanities from user: {name}")


def send_comment(location, authorization, content):
    url = f"https://squabbles.io{location}"
    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json"
    }
    data = {
        "content": content
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 201:
        print("Comment posted successfully.")
    else:
        print("Failed to post the comment.")


if __name__ == '__main__':
    user = 'PuppiestDoggo'
    location = "/api/posts/d5xkQ9Q02k/reply"
    authorization = "Bearer XXXXX"
    find_and_send_profanities(user, location, authorization)
