from bs4 import BeautifulSoup
import requests


new_url = 'https://stackoverflow.com/questions/18166581/python-looping-through-a-multidimensional-dictionary'
new_response = requests.get(new_url)
new_soup = BeautifulSoup(new_response.text, 'html.parser')

new_title = new_soup.find(
    'h1', {'class': 'grid--cell fs-headline1 fl1'}).get_text().replace('\n', '')
print()

print('#'*100)
print(new_title)
print('#'*100)

post_bodies = new_soup.find_all(class_ = 'post-text')
# print(post_bodies)
for post_body in post_bodies:
    # print(post_body)
    pbody = post_body.find('p').get_text()
    pcode = post_body.find('code').get_text()
    print('-'*40)
    print()
    print(pbody)
    print(pcode)
    print()
print()
# print(post_body)
