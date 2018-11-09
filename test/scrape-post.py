import requests
from bs4 import BeautifulSoup

new_url = 'https://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags/1733489#1733489'
new_response = requests.get(new_url)
new_soup = BeautifulSoup(new_response.text, 'html.parser')

new_title = new_soup.find(
    'h1', {'class': 'grid--cell fs-headline1 fl1'}).get_text().replace('\n', '')
print()

print('#'*50)
print(new_title)
print('#'*50, end="\n\n")

# post_bodies = new_soup.find_all(class_ = 'post-text')
post_body = new_soup.find(class_ ='answer')

# print(post_body)
pbody = post_body.find_all('p')  #find all p
for p in pbody:
    print(p.get_text())
    print()
# print(pbody)

pcode = post_body.find_all('code')  #find all code
for c in pcode:
    print(c.get_text())
    print()
# print(pcode)

pvote = post_body.find(class_="vote").find('span').get_text()
print()
print('*'*18)
print("*    VOTES : ",end = '')
print(pvote+"   *")

print('*'*18)


print()
print()
