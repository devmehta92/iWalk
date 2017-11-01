# NOTE: this example requires PyAudio because it uses the Microphone class
from google import google
from datetime import datetime
import googlemaps
import speech_recognition as sr
import html2text
import serial
import LatLon


def getGPS():
    recordNotFound = True
    gps = serial.Serial("/dev/ttyS0", baudrate=9600)
    while recordNotFound:
        line = gps.readline()
        data = line.split(",")
        if data[0] == "$GPRMC":
            if data[2] == "A":
                i = 2
                j = 2
                cord_lat = data[3]
                cord_long = data[5]
                lat_update = str(cord_lat)
                long_update = str(cord_long)
                print lat_update
                print long_update
                latitude = cord_lat.split(".")
                longitude = cord_long.split(".")
                if len(latitude[0]) == 5:
                    i = 3
                if len(longitude[0]) == 5:
                    j = 3

                lat_deg = lat_update[:i]
                lat_min = lat_update[i:]
                lat_min_update = float(lat_min) / 60
                long_deg = long_update[:j]
                print long_deg
                long_min = long_update[j:]
                print long_min
                long_min_update = float(long_min) / 60
                lat = float(lat_deg) + lat_min_update
                longitude_update = float(long_deg) + long_min_update
                result_lat = str(lat)
                result_long = str(longitude_update)
                if data[4] == "S":
                    result_lat = "-" + str(lat)

                elif data[6] == "W":
                    result_long = "-" + str(longitude_update)
                result = result_lat + "," + result_long
                recordNotFound = False
    return (result)

gmaps = googlemaps.Client(key='AIzaSyDcX1ys0BXit1nLqtpLJGys0eSaPpXdulo')

#KEY = AIzaSyDcX1ys0BXit1nLqtpLJGys0eSaPpXdulo
# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)
    #print audio

# recognize speech using Sphinx
#try:
#    print("Sphinx thinks you said " + r.recognize_sphinx(audio))
#except sr.UnknownValueError:
#    print("Sphinx could not understand audio")
#except sr.RequestError as e:
#    print("Sphinx error; {0}".format(e))

# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    voice = r.recognize_google(audio)
    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    #print voice
    search_results = google.search(voice)
    #print search_results
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("413 Summit Avenue, Arlington, TX",
                                     voice,
                                     mode="walking",
                                     departure_time=now)

print directions_result

directions_result = directions_result[0]

print directions_result


for leg in directions_result['legs']:
    startAddress = leg['start_address']
    print "Start Address:", startAddress
    endAddress = leg['end_address']
    print "End Address:", endAddress
    for step in leg['steps']:
        direction_instructions = html2text.html2text(step['html_instructions'])
        direction_distance = step['distance']
        print "Direction instructions", direction_instructions
        print "Direction distance", direction_distance

gps = getGPS()
print ("GPS = "+ gps)