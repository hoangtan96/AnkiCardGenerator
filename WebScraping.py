#import libraries
import requests
from bs4 import BeautifulSoup
'''
page = requests.get('https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ1.htm')



soup = BeautifulSoup(page.text, 'html.parser')


artist_name_list = soup.find(class_='BodyText')
artist_name_list_items = artist_name_list.find_all('a')

# for artist_name in artist_name_list_items:
#     print(artist_name.prettify())

for artist_name in artist_name_list_items:
    names = artist_name.contents[0]
    print(names)
'''

DictionaryOnline_url = "https://dictionary.cambridge.org/dictionary/english/something"

RequestURL = requests.get(DictionaryOnline_url)    

soup = BeautifulSoup(RequestURL.text, 'html.parser')


#Word =
word_item = soup.find("span", attrs ={ "class" : "hw dhw" })
#solution 2: print(soup.find("ul", id="mylist")) 
word_name = word_item.text
print(word_name)

#Definition of word
#Because there're a lots of definition
Definition_items = soup.find_all("div", attrs= {"class" : "def ddef_d db"})

for definition_name in Definition_items:
    print(definition_name.text)

#Parts of Speech: 
PartsOfSpeech_item = soup.find("span", attrs= {"class" : "pos dpos"})
PartsOfSpeech_name = PartsOfSpeech_item.text
print(PartsOfSpeech_name)

#PhoneticSymbol
#Actually there're 2 phonetic symbol (US and UK)
PhoneticSymbol_items = soup.find_all("span", attrs= {"class" : "ipa dipa lpr-2 lpl-1"})
for PhoneticSymbol_name in PhoneticSymbol_items:
    print(PhoneticSymbol_name.text)

#Sounds_item
AudiolinksPosition_UK = soup.find("span", attrs= {"class" :  "uk dpron-i"}).find('source', attrs={"type": "audio/mpeg"})
AudiolinksPosition_UK_link = "https://dictionary.cambridge.org" + AudiolinksPosition_UK['src']
print(AudiolinksPosition_UK_link)
AudiolinksPosition_US = soup.find("span", attrs= {"class" :  "us dpron-i"}).find('source', attrs={"type": "audio/mpeg"})
AudiolinksPosition_US_link = "https://dictionary.cambridge.org" + AudiolinksPosition_US['src']
print(AudiolinksPosition_US_link)

#Example:


'''




Sounds_item

Synonym_items
'''
