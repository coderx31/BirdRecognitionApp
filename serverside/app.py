# importing components
import os
import requests
from flask import Flask, request, render_template, send_from_directory, jsonify, json
import save_image, image_classification

app = Flask(__name__)

# get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))
prediction_index = 1

# getting all bird names
# here just to testing purposes
birdName = ""
birdScName = ""
birdLocation = ""
success = False
bird_categories = ['AFRICAN CROWNED CRANE', 'AFRICAN FIREFINCH', 'ALBATROSS', 'ALEXANDRINE PARAKEET',
                   'AMERICAN AVOCET', 'AMERICAN BITTERN', 'AMERICAN COOT', 'AMERICAN GOLDFINCH',
                   'AMERICAN KESTREL', 'AMERICAN PIPIT', 'AMERICAN REDSTART', 'ANHINGA', 'ANNAS HUMMINGBIRD',
                   'ANTBIRD', 'ARARIPE MANAKIN', 'ASIAN CRESTED IBIS', 'BALD EAGLE', 'BALI STARLING',
                   'BALTIMORE ORIOLE', 'BANANAQUIT', 'BANDED BROADBILL', 'BAR-TAILED GODWIT', 'BARN OWL',
                   'BARN SWALLOW', 'BARRED PUFFBIRD', 'BAY-BREASTED WARBLER', 'BEARDED BARBET',
                   'BELTED KINGFISHER', 'BIRD OF PARADISE', 'BLACK FRANCOLIN', 'BLACK SKIMMER', 'BLACK SWAN',
                   'BLACK THROATED WARBLER', 'BLACK VULTURE', 'BLACK-CAPPED CHICKADEE', 'BLACK-NECKED GREBE',
                   'BLACK-THROATED SPARROW', 'BLACKBURNIAM WARBLER', 'BLUE GROUSE', 'BLUE HERON', 'BOBOLINK',
                   'BROWN NOODY', 'BROWN THRASHER', 'CACTUS WREN', 'CALIFORNIA CONDOR', 'CALIFORNIA GULL',
                   'CALIFORNIA QUAIL', 'CANARY', 'CAPE MAY WARBLER', 'CAPUCHINBIRD', 'CARMINE BEE-EATER',
                   'CASPIAN TERN', 'CASSOWARY', 'CHARA DE COLLAR', 'CHIPPING SPARROW', 'CHUKAR PARTRIDGE',
                   'CINNAMON TEAL', 'COCK OF THE  ROCK', 'COCKATOO', 'COMMON FIRECREST', 'COMMON GRACKLE',
                   'COMMON HOUSE MARTIN', 'COMMON LOON', 'COMMON POORWILL', 'COMMON STARLING', 'COUCHS KINGBIRD',
                   'CRESTED AUKLET', 'CRESTED CARACARA', 'CRESTED NUTHATCH', 'CROW', 'CROWNED PIGEON',
                   'CUBAN TODY', 'CURL CRESTED ARACURI', 'D-ARNAUDS BARBET', 'DARK EYED JUNCO',
                   'DOWNY WOODPECKER', 'EASTERN BLUEBIRD', 'EASTERN MEADOWLARK', 'EASTERN ROSELLA',
                   'EASTERN TOWEE', 'ELEGANT TROGON', 'ELLIOTS  PHEASANT', 'EMPEROR PENGUIN', 'EMU',
                   'EURASIAN GOLDEN ORIOLE', 'EURASIAN MAGPIE', 'EVENING GROSBEAK', 'FIRE TAILLED MYZORNIS',
                   'FLAME TANAGER', 'FLAMINGO', 'FRIGATE', 'GAMBELS QUAIL', 'GILA WOODPECKER', 'GILDED FLICKER',
                   'GLOSSY IBIS', 'GO AWAY BIRD', 'GOLD WING WARBLER', 'GOLDEN CHEEKED WARBLER',
                   'GOLDEN CHLOROPHONIA', 'GOLDEN EAGLE', 'GOLDEN PHEASANT', 'GOLDEN PIPIT', 'GOULDIAN FINCH',
                   'GRAY CATBIRD', 'GRAY PARTRIDGE', 'GREAT POTOO', 'GREATOR SAGE GROUSE', 'GREEN JAY',
                   'GREY PLOVER', 'GUINEA TURACO', 'GUINEAFOWL', 'GYRFALCON', 'HARPY EAGLE', 'HAWAIIAN GOOSE',
                   'HELMET VANGA', 'HOATZIN', 'HOODED MERGANSER', 'HOOPOES', 'HORNBILL', 'HORNED GUAN',
                   'HORNED SUNGEM', 'HOUSE FINCH', 'HOUSE SPARROW', 'IMPERIAL SHAQ', 'INCA TERN',
                   'INDIAN BUSTARD', 'INDIAN PITTA', 'INDIGO BUNTING', 'JABIRU', 'JAVA SPARROW', 'JAVAN MAGPIE',
                   'KAKAPO', 'KILLDEAR', 'KING VULTURE', 'KIWI', 'KOOKABURRA', 'LARK BUNTING', 'LEARS MACAW',
                   'LILAC ROLLER', 'LONG-EARED OWL', 'MALABAR HORNBILL', 'MALACHITE KINGFISHER', 'MALEO',
                   'MALLARD DUCK', 'MANDRIN DUCK', 'MARABOU STORK', 'MASKED BOOBY', 'MASKED LAPWING',
                   'MIKADO  PHEASANT',
                   'MOURNING DOVE', 'MYNA', 'NICOBAR PIGEON', 'NORTHERN BALD IBIS', 'NORTHERN CARDINAL',
                   'NORTHERN FLICKER',
                   'NORTHERN GANNET', 'NORTHERN GOSHAWK', 'NORTHERN JACANA', 'NORTHERN MOCKINGBIRD', 'NORTHERN PARULA',
                   'NORTHERN RED BISHOP', 'OCELLATED TURKEY', 'OKINAWA RAIL', 'OSPREY', 'OSTRICH', 'OYSTER CATCHER',
                   'PAINTED BUNTIG', 'PALILA', 'PARADISE TANAGER', 'PARUS MAJOR', 'PEACOCK', 'PELICAN',
                   'PEREGRINE FALCON',
                   'PHILIPPINE EAGLE', 'PINK ROBIN', 'PUFFIN', 'PURPLE FINCH', 'PURPLE GALLINULE', 'PURPLE MARTIN',
                   'PURPLE SWAMPHEN', 'QUETZAL', 'RAINBOW LORIKEET', 'RAZORBILL', 'RED BEARDED BEE EATER',
                   'RED BELLIED PITTA',
                   'RED FACED CORMORANT', 'RED FACED WARBLER', 'RED HEADED DUCK', 'RED HEADED WOODPECKER',
                   'RED HONEY CREEPER',
                   'RED WINGED BLACKBIRD', 'RED WISKERED BULBUL', 'RING-NECKED PHEASANT', 'ROADRUNNER', 'ROBIN',
                   'ROCK DOVE',
                   'ROSY FACED LOVEBIRD', 'ROUGH LEG BUZZARD', 'RUBY THROATED HUMMINGBIRD', 'RUFOUS KINGFISHER',
                   'RUFUOS MOTMOT', 'SAMATRAN THRUSH', 'SAND MARTIN', 'SCARLET IBIS', 'SCARLET MACAW', 'SHOEBILL',
                   'SHORT BILLED DOWITCHER', 'SMITHS LONGSPUR', 'SNOWY EGRET', 'SNOWY OWL', 'SORA', 'SPANGLED COTINGA',
                   'SPLENDID WREN', 'SPOON BILED SANDPIPER', 'SPOONBILL', 'SRI LANKA BLUE MAGPIE', 'STEAMER DUCK',
                   'STORK BILLED KINGFISHER', 'STRAWBERRY FINCH', 'STRIPPED SWALLOW', 'SUPERB STARLING',
                   'SWINHOES PHEASANT',
                   'TAIWAN MAGPIE', 'TAKAHE', 'TASMANIAN HEN', 'TEAL DUCK', 'TIT MOUSE', 'TOUCHAN', 'TOWNSENDS WARBLER',
                   'TREE SWALLOW', 'TRUMPTER SWAN', 'TURKEY VULTURE', 'TURQUOISE MOTMOT', 'UMBRELLA BIRD',
                   'VARIED THRUSH',
                   'VENEZUELIAN TROUPIAL', 'VERMILION FLYCATHER', 'VIOLET GREEN SWALLOW', 'VULTURINE GUINEAFOWL',
                   'WATTLED CURASSOW', 'WHIMBREL', 'WHITE CHEEKED TURACO', 'WHITE NECKED RAVEN', 'WHITE TAILED TROPIC',
                   'WILD TURKEY', 'WILSONS BIRD OF PARADISE', 'WOOD DUCK', 'YELLOW BELLIED FLOWERPECKER',
                   'YELLOW CACIQUE',
                   'YELLOW HEADED BLACKBIRD']


@app.route('/')
def index():
    return 'Bird recognition system.'


@app.route('/classification', methods=["POST", "GET"])
def classification():
    # print('method works')
    json_data = request.json
    value = bytes(json_data['image'], 'utf-8')
    save_image.save(value)  # process decode and save the image
    index = image_classification.recognition()  # prediction
    global prediction_index
    prediction_index = index
    print(index)
    return "", 204


@app.route('/bird', methods=["GET"])
def bird():
    # invoke url of the aws dynamo db database
    url = "https://15c071drx0.execute-api.us-east-2.amazonaws.com/birdov2/birdo_bird_details?birdID="
    global prediction_index
    # concatenate url with the key
    url_with_key = url + str(prediction_index + 1)
    bird_details = requests.request("GET", url_with_key)
    bird_details = bird_details.json()
    return jsonify({
        "bird": bird_details['body']['birdName'],
        "birdScName": bird_details['body']['birdScName'],
        "location": bird_details['body']['location']
    })



@app.route('/birdDes', methods=["POST", "GET"])
def search():
    json_data = request.json
    bird_name = json_data['birdName'].upper()
    try:
       url = "https://twm47yfmxg.execute-api.us-east-2.amazonaws.com/birdoSearch/birdo_bird_details?birdName="
       # concatinate url with the birdName
       url_with_bird = url + bird_name
       bird_details = requests.request("GET", url_with_bird)
       bird_details = bird_details.json()
       print(bird_details["body"][0])
       global birdName, birdScName, birdLocation
       birdName =  bird_details['body'][0]['birdName']
       birdScName = bird_details['body'][0]['birdScName']
       birdLocation = bird_details['body'][0]['location']
       return jsonify({
               "bird": bird_details['body'][0]['birdName'],
               "birdScName": bird_details['body'][0]['birdScName'],
               "location": bird_details['body'][0]['location']
           })
    except:
        print("null")
        return {"bird" : "null"}


@app.route('/dataFromDB',methods=["GET"])
def data_db():
    return jsonify({
        "bird": birdName,
        "birdScName": birdScName,
        "location": birdLocation
    })


@app.route('/tagLocation', methods=["POST"])
def tag_location():
    json_data = request.json
    bird_name = json_data['birdName'].upper()
    bird_location = json_data['birdLocation']
    url = "https://w7v57l6d77.execute-api.us-east-2.amazonaws.com/birdoUpdate/birdo_bird_details?birdName="
    url_name_location = url+bird_name+"&birdLocation="+bird_location
    status = requests.request("GET", url_name_location)
    status = status.json()
    global success
    print(status["statusCode"])
    if (status["statusCode"] == 200):
        success = True
        return {"return": "success"}
    else:
        success = False
        return {"return": "unsuccess"}
    print(bird_name)
    print(bird_location)
    print("Method Works")
    return "", 204


@app.route('/locationSuccess', methods=["GET"])
def success_tag():
    return {"success": success}


if __name__ == '__main__':
    app.run(host='192.168.8.100', debug=True)
