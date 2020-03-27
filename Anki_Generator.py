'''More infomation we can get here: https://foosoft.net/projects/anki-connect/index.html#cards '''

import requests
import json



# Show all deck in Anki - deckNames
ShowAllDeck_json = {
    "action": "deckNames",
    "version": 6
}

# Delete decks - deleteDecks
DeleteDeck_json = {
    "action": "deleteDecks",
    "version": 6,
    "params": {
        "decks": ["Japanese::JLPT N5", "Easy Spanish"],
        "cardsToo": True
    }
}

# Show models card type
GetModelsNames_json = {
    "action": "modelNames",
    "version": 6
}

# Get model names and ids - modelNamesAndIds
GetModelNamesAndIDs_json = {
    "action": "modelNamesAndIds",
    "version": 6
}

# Model field names - modelFieldNames
GetModelFieldNames_json = {
    "action": "modelFieldNames",
    "version": 6,
    "params": {
        "modelName": "English type"
    }
}

#Create model - createModel
SetModel_json = {
    "action": "createModel",
    "version": 6,
    "params": {
        "modelName": "newModelName",
        "inOrderFields": ["Field1", "Field2", "Field3"],
        "css": "Optional CSS with default to builtin css",
        "cardTemplates": [
            {
                "Name": "My Card 1",
                "Front": "Front html {{Field1}}",
                "Back": "Back html  {{Field2}}"
            }
        ]
    }
}

# Get model templates - modelTemplates
GetModelTemplate_json = {
    "action": "modelTemplates",
    "version": 6,
    "params": {
        "modelName": "Basic (and reversed card)"
    }
}

# Update model template - updateModelTemplates
UpdateModelTemplate_json = {
    "action": "updateModelTemplates",
    "version": 6,
    "params": {
        "model": {
            "name": "Custom",
            "templates": {
                "Card 1": {
                    "Front": "{{Question}}?",
                    "Back": "{{Answer}}!"
                }
            }
        }
    }
}

# Add Notes - addNote
AddNotes_json = {
    "action": "addNote",
    "version": 6,
    "params": {
        "note": {
            "deckName": "Default",
            "modelName": "Basic",
            "fields": {
                "Front": "front content",
                "Back": "back content"
            },
            "options": {
                "allowDuplicate": False
            },
            "tags": [
                "yomichan"
            ],
            "audio": [{
                "url": "https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=猫&kana=ねこ",
                "filename": "yomichan_ねこ_猫.mp3",
                "skipHash": "7e2c2f954ef6051373ba916f000168dc",
                "fields": [
                    "Front"
                ]
            }]
        }
    }
}

# Update note fields - updateNoteFields
UpdateNoteFields_json = {
    "action": "updateNoteFields",
    "version": 6,
    "params": {
        "note": {
            "id": 1514547547030,
            "fields": {
                "Front": "new front content",
                "Back": "new back content"
            },
            "audio": [{
                "url": "https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=猫&kana=ねこ",
                "filename": "yomichan_ねこ_猫.mp3",
                "skipHash": "7e2c2f954ef6051373ba916f000168dc",
                "fields": [
                    "Front"
                ]
            }]
        }
    }
}

example = requests.post('http://127.0.0.1:8765', json = GetModelFieldNames_json)
print(example.json())

# # Example 1: Generate Json
# # Some JSON:
# x =  '{ "name":"John", "age":30, "city":"New York"}'
# # parse x:
# y = json.loads(x)
# # the result is a Python dictionary:
# print(y)

# ShowAllDeck_json = requests.post('http://127.0.0.1:8765', json={
#     "action": "deckNames",
#     "version": 6
# })

# print(ShowAllDeck_json.json())



""" r = requests.post('http://127.0.0.1:8765', json={
    "action": "addNote",
    "version": 6,
    "params": {
        "note": {
            "deckName": "Test",
            "modelName": "Basic (type in the answer)",
            "fields": {
                "Front": "front content",
                "Back": "back content"
            },
            "tags": [
                "yomichan"
            ],
            "audio": {
                "url": "https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=猫&kana=ねこ",
                "filename": "yomichan_ねこ_猫.mp3",
                "skipHash": "7e2c2f954ef6051373ba916f000168dc",
                "fields": [
                    "Front"
                ]
            }
        }
    }
})


# print(r.json())
"""