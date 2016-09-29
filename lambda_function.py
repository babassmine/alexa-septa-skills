"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import requests
import json
# --------------- Stations -----------------------------------------------------
STATIONS = {
"30th street station": 90004,
"49th st": 90314,
"9th st": 90539,
"airport terminal a": 90404,
"airport terminal b": 90403,
"airport terminal c-d": 90402,
"airport terminal e-f": 90401,
"allegheny": 90208,
"allen lane": 90804,
"ambler": 90526,
"angora": 90313,
"ardmore": 90518,
"ardsley": 90412,
"bala": 90002,
"berwyn": 90508,
"bethayres": 90318,
"bridesburg": 90710,
"bristol": 90703,
"bryn mawr": 90516,
"carpenter": 90805,
"chalfont": 90535,
"chelten avenue": 90808,
"cheltenham": 90813,
"chester tc": 90207,
"chestnut hill east": 90720,
"chestnut hill west": 90801,
"claymont": 90204,
"clifton-aldan": 90309,
"colmar": 90533,
"conshohocken": 90225,
"cornwells heights": 90706,
"crestmont": 90414,
"croydon": 90704,
"crum lynne": 90209,
"curtis park": 90216,
"cynwyd": 90001,
"daylesford": 90507,
"darby": 90217,
"delaware valley college": 90537,
"devon": 90509,
"downingtown": 90502,
"doylestown": 90538,
"east falls": 90219,
"eastwick station": 90405,
"eddington": 90705,
"eddystone": 90208,
"elkins park": 90409,
"elm st": 90228,
"elwyn station": 90301,
"exton": 90504,
"fern rock tc": 90407,
"fernwood": 90312,
"folcroft": 90214,
"forest hills": 90320,
"ft washington": 90525,
"fortuna": 90532,
"fox chase": 90815,
"germantown": 90713,
"gladstone": 90310,
"glenolden": 90213,
"glenside": 90411,
"gravers": 90719,
"gwynedd valley": 90528,
"hatboro": 90416,
"haverford": 90517,
"highland ave": 90206,
"highland": 90802,
"holmesburg jct": 90708,
"ivy ridge": 90222,
"jenkintown-wyncote": 90410,
"langhorne": 90324,
"lansdale": 90531,
"lansdowne": 90311,
"lawndale": 90812,
"levittown": 90702,
"link belt": 90534,
"main st": 90227,
"malvern": 90505,
"manayunk east": 90221,
"marcus hook": 90205,
"market east": 90006,
"meadowbrook": 90317,
"media": 90302,
"melrose park": 90408,
"merion": 90521,
"miquon": 90223,
"morton": 90306,
"moylan-rose valley": 90303,
"mt airy": 90717,
"narberth": 90520,
"neshaminy falls": 90323,
"new britain": 90536,
"newark": 90201,
"norristown tc": 90226,
"north broad st": 90008,
"north hills": 90523,
"north philadelphia": 90711,
"north wales": 90529,
"norwood": 90212,
"olney": 90811,
"oreland": 90524,
"overbrook": 90522,
"paoli": 90506,
"penllyn": 90527,
"pennbrook": 90530,
"philmont": 90319,
"primos": 90308,
"prospect park": 90211,
"queen lane": 90809,
"radnor": 90513,
"ridley park": 90210,
"rosemont": 90515,
"roslyn": 90413,
"rydal": 90316,
"ryers": 90814,
"secane": 90307,
"sharon hill": 90215,
"somerton": 90321,
"spring mill": 90224,
"st. davids": 90512,
"st. martins": 90803,
"stenton": 90715,
"strafford": 90510,
"suburban station": 90005,
"swarthmore": 90305,
"tacony": 90709,
"temple u": 90007,
"thorndale": 90501,
"torresdale": 90707,
"trenton": 90701,
"trevose": 90322,
"tulpehocken": 90807,
"university city": 90406,
"upsal": 90806,
"villanova": 90514,
"wallingford": 90304,
"warminster": 90417,
"washington lane": 90714,
"wayne jct": 90009,
"wayne": 90511,
"west trenton": 90327,
"whitford": 90503,
"willow grove": 90514,
"wilmington": 90203,
"wissahickon": 90220,
"wister": 90712,
"woodbourne": 90325,
"wyndmoor": 90718,
"wynnefield avenue": 90003,
"wynnewood": 90519,
"yardley": 90326
}

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Septa regional rail helper " \
                    "Please tell me your septa regional rail route that I can help you with by saying, " \
                    "when is the train from Suburban Station to Lansdowne"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me your septa regional rail route that I can help you with by saying, " \
                    "when is the train from Suburban Station to Lansdowne"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Septa regional rail helper. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def get_my_route_info(from_station, to_station):
    to_cap = lambda x: x.capitalize()
    from_station = " ".join(map(to_cap, from_station.split(" ")))
    to_station = " ".join(map(to_cap, to_station.split(" ")))
    print("septa endpoint = " + 'http://www3.septa.org/hackathon/NextToArrive/'+from_station+'/'+to_station)
    response = requests.get('http://www3.septa.org/hackathon/NextToArrive/'+from_station+'/'+to_station)
    schedule = json.loads(response.text)
    return {
        "departure_time": schedule[0]['orig_departure_time'],
        "arrival_time": schedule[0]['orig_arrival_time'],
        "delay": schedule[0]['orig_delay'],
        "line": schedule[0]['orig_line']
        }


def get_next_train_info(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = True

    if ('FromStation' in intent['slots']) and ('ToStation' in intent['slots']):
        # favorite_color = intent['slots']['Color']['value']
        from_station = intent['slots']['FromStation']['value']
        to_station = intent['slots']['ToStation']['value']
        route_info = get_my_route_info(from_station, to_station)
        speech_output = "The next train from " + \
                        from_station + \
                        " to " +\
                        to_station + \
                        " is at " +\
                        route_info["departure_time"] + \
                        ". It will be arriving at " + \
                        route_info["arrival_time"] + \
                        ". The current delay is " + \
                        route_info["delay"]
        reprompt_text = None
    else:
        speech_output = "I am not sure what stations you want information about. " \
                        "Please try again."
        reprompt_text = "I'm not sure when your train is. " \
                        "You can ask me when is the next train, " \
                        "regional rails only."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "WhenIsMyTrainIntent":
        return get_next_train_info(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.ask.skill.22754375-6d40-4dd2-9f0c-33651b755517"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
