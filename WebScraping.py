#import libraries
import requests
from bs4 import BeautifulSoup

'''
March 26, 2020 - Huynh Hoang Tan:
- Create initial file
- Update web structure, 

'''


'''
Structure of Cambridge Dictionary website

Entry (div - "pr entry-body__el")
    Header (div - "pos-header dpos-h"):

        - Word ("hw dhw")
        - Part of speech ("pos dpos")
        - Phonetic symbol ("ipa dipa lpr-2 lpl-1")
        - Sound ("uk dpron-i", "us dpron-i")

    Body (div - pos-body)
        - In div - "class" : "def-block ddef_block"
            - div - "class" : "ddef_h"
                - div - "class" : "def ddef_d db"       => Definition
            - div - "class" : "def-body ddef_b"
                - div - "class" : "examp dexamp"        => Example 

1 Entry only have 1 Header - Include Word, parts of speech, sound, phonetic symbol
1 Entry have multiple body - Definition, example, idiom, synonym

Dictionary structure: 
Dic = { ID1: {
"": ...,
"Word": ...,
"PartofSpeech",
SoundUS, SoundUK,
(DID1, Definition, example), (DID2, Definition, example),
MoreExample,
Thesaurus
}
ID2: {..., ...}, ID3: {... , ...}
}
'''
Output_dict = {}

#function macro_FindElement(element): Use for macro a dulicate function
def FindElement(soup_url,object_name,type_name,id_name):
    return soup_url.find(object_name, attrs= {type_name : id_name})
def FindExactElement(soup_url,object_name,type_name,id_name):
    return soup_url.find(lambda tag: tag.name == object_name and tag.get(type_name) == [id_name])
def FindAllElements(soup_url,object_name,type_name,id_name):
    return soup_url.find_all(object_name, attrs= {type_name : id_name})

DictionaryOnline_url = "https://dictionary.cambridge.org/dictionary/english/bunk"

#Get data from URL
RequestURL = requests.get(DictionaryOnline_url)    
#Parser HTML 
soup = BeautifulSoup(RequestURL.text, 'html.parser')

#Get entry level

EntryWord_multipleitems = soup.find_all("div", attrs = {"class" : "pr entry-body__el"})
# for EntryWord_singleitem in EntryWord_items:
#     print(EntryWord_singleitem.text)

def ScrapingData(URL, Output_dict):
    RequestURL = requests.get(URL)    
    soup = BeautifulSoup(RequestURL.text, 'html.parser')
    #Find all infomation related to this word
    EntryWord_multipleitems = soup.find_all("div", attrs = {"class" : "pr entry-body__el"})
    for EntryWord_singleitem in EntryWord_multipleitems:
        print("id:" + EntryWord_singleitem.div["id"])
        #Get the multiple definition and locate it by id
        cid_body = EntryWord_singleitem.div["id"]
        #Create empty dictionary 
        Output_dict[cid_body] = {}
        GetHeader(EntryWord_singleitem, Output_dict[cid_body])
        GetBody(EntryWord_singleitem, Output_dict[cid_body])
        # Output_dict[cid_body] = cid_body_dictionary

#----------------------------------------------------------------------------------------------------------------------------#
#Function GetHeader(): Get all information from header
#Include Word, parts of speech, sound, phonetic symbol
def GetHeader(EntryWord_singleitem, cid_body):
    print("-------------------------------------------------------------------------------------")
    print("===---Header step---===")
    Headerdata = FindElement(EntryWord_singleitem,"div", "class","pos-header dpos-h")
    #Get Word name
    Word_name = FindElement(Headerdata, "span", "class", "hw dhw").text
    cid_body["Word"] = Word_name
    print("Added word : " + Word_name)
    #Get Parts of Speech
    PartsOfSpeech_name = FindElement(Headerdata, "span", "class", "pos dpos").text
    #After collecting all data, add it to dictionary 
    cid_body["PartsOfSpeech"] = PartsOfSpeech_name
    print("Added PartsOfSpeech : " + PartsOfSpeech_name)
    #Get Phonetic Symbol and Sound
    AudiolinksPosition_UK = FindElement(Headerdata, "span", "class", "uk dpron-i")
    AudiolinksPosition_US = FindElement(Headerdata, "span", "class", "us dpron-i")
    #Some dictionary word record don't have record. it need condition:
    if AudiolinksPosition_UK:
        Soundlink_UK_name = "https://dictionary.cambridge.org" + FindElement(AudiolinksPosition_UK, 'source', "type", "audio/mpeg")['src']
        #Check if Phonetic Symbol is available:
        PhoneticSymbol_UK_block = FindElement(AudiolinksPosition_UK, "span", "class", "ipa dipa lpr-2 lpl-1")
        if PhoneticSymbol_UK_block:
            PhoneticSymbol_UK_name = "/" + PhoneticSymbol_UK_block.text + "/"
            cid_body["PhoneticSymbol_UK"] = PhoneticSymbol_UK_name
        cid_body["Soundlink_UK"] = Soundlink_UK_name
        print("Added UK sound")
    if AudiolinksPosition_US:
        Soundlink_US_name = "https://dictionary.cambridge.org" + FindElement(AudiolinksPosition_US, 'source', "type", "audio/mpeg")['src']
        PhoneticSymbol_US_block = FindElement(AudiolinksPosition_US, "span", "class", "ipa dipa lpr-2 lpl-1")
        if PhoneticSymbol_US_block:
            PhoneticSymbol_US_name = "/" + PhoneticSymbol_US_block.text + "/" 
            cid_body["PhoneticSymbol_US"] = PhoneticSymbol_US_name
        cid_body["Soundlink_US"] = Soundlink_US_name
        print("Added US sound")
    #Show console if it done
    print("[Added Header contents]")    
    print(cid_body)
    
    


#----------------------------------------------------------------------------------------------------------------------------#
#function GetBody(): Get all information from body
#Definition, example, idiom, synonym
def GetBody(EntryWord_singleitem, cid_body):
    print("===---Body step---===")
    #Get Body Data position
    BodyData = FindElement(EntryWord_singleitem,"div","class","pos-body")
    
    #In Body, there're multiple definition for 1 part of speech of Word. So we need to find all definition
    DefinitionBlock_multipleItems = FindAllElements(BodyData,"div", "class", "def-block ddef_block")

    for DefinitionBlock_singleitem in DefinitionBlock_multipleItems:
        DefinitionID = DefinitionBlock_singleitem["data-wl-senseid"]
        print("DefinitionID: " + DefinitionID)
        cid_body["defi"+DefinitionID] = {}
        GetDefinitionData(DefinitionBlock_singleitem, cid_body["defi"+DefinitionID])
    
    #Check if Body content has More Example Block:
    #Because this block id daccord has a lots of class use it. So macro need to update to find exactly it.
    MoreExample_Block = FindExactElement(DefinitionBlock_singleitem,"div", "class", "daccord")
    if MoreExample_Block:
        GetMoreExampleData(MoreExample_Block, cid_body)
    #Check if this block support:
    ExtraInfomation_Block = FindElement(DefinitionBlock_singleitem,"div", "class", "smartt daccord")
    if ExtraInfomation_Block:
        GetExtraInfomationData(ExtraInfomation_Block, cid_body)
    print("Added Body contents")
    print("-------------------------------------------------------------------------------------")
#----------------------------------------------------------------------------------------------------------------------------#
#Function GetDefinitionData()
#Get definition and example phreases from body block.
def GetDefinitionData(DefinitionBlock_singleitem, cid_body):
    #Get definition
    Definition_block = FindElement(DefinitionBlock_singleitem,"div", "class", "def ddef_d db")
    DefinitionWord_name = Definition_block.text
    cid_body["Definition: "] = DefinitionWord_name
    print("Added definition: " + DefinitionWord_name)
    #Create empty example list
    cid_body["Example: "] = []
    #Get examples
    #Check if examples is available:
    Example_multipleItems = FindAllElements(DefinitionBlock_singleitem, "div" , "class", "examp dexamp")
    if Example_multipleItems:
        for Example_singleItem in Example_multipleItems:
            #Add example to a list        
            cid_body["Example: "].append(Example_singleItem.text)
            print("Added example: " + Example_singleItem.text)
    #Print console to inform added done
    print("Added definition data block: ")
    print(cid_body)


#----------------------------------------------------------------------------------------------------------------------------#
#Function GetMoreExampleData():
#Get example phreases from Example Data block
def GetMoreExampleData(MoreExample_Block, cid_body):
    #Create empty MoreExampleList
    cid_body["MoreExample"] = []
    #Get example phreases
    MoreExample_multipleItems =  FindAllElements(MoreExample_Block, "li", "class", "eg dexamp hax")
    #print("MoreExampleBlock:")
    print(MoreExample_multipleItems)
    for MoreExample_singleImtems in MoreExample_multipleItems:
        cid_body["MoreExample"].append(MoreExample_singleImtems.text)
        print("Added more example block: " + MoreExample_singleImtems.text)
    print("Added MoreExample block")
    print(cid_body)

#----------------------------------------------------------------------------------------------------------------------------#
#Function GetExtraInformationData():
#Get Synonyms, Related words from Thesaurus block
def GetExtraInfomationData(ExtraInfomation_Block, cid_body):
    #Get Thesaurus: describe synonyms and related words
    Thesaurus_name = FindElement(ExtraInfomation_Block,"div", "class", "daccord_lt").text
    cid_body["Synonym"] = Thesaurus_name
    #Get extra words
    extrawords_multipleItems = FindAllElements(ExtraInfomation_Block, "span", "class", "hw haf")
    #Create emtry extra word list:
    cid_body["Extra words"] = []
    for extrawords_singleItem in extrawords_multipleItems:
        cid_body["Extra words"].append(extrawords_singleItem.text)
        print("Added extra words: " + extrawords_singleItem.text)
    print("Added ExtraInformation Block: ")
    print(cid_body)
#----------------------------------------------------------------------------------------------------------------------------#

ScrapingData(DictionaryOnline_url,Output_dict)
print("Added done")
print(Output_dict)
dictionary_test = {}
cid = 1





"""
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



'''
Elements need to scrap:
-Example for each definition
-Synonym
'''


'''
This is a example:

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
"""