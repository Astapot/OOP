import requests

def get_the_superint():
    supers = ['Hulk', 'Captain America', 'Thanos']
    result = {}
    url = 'https://akabab.github.io/superhero-api/api/all.json'
    response = requests.get(url)
    for sup in response.json():
        if sup['name'] in supers:
            result[sup['name']] = sup["powerstats"]["intelligence"]
    the_superint = supers[0]
    for man in result:
        if result[man] > result[the_superint]:
            the_superint = man
    return the_superint

print(get_the_superint())