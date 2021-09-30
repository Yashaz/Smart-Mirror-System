from __future__ import print_function
import time 
import requests
import cv2
import operator
import numpy as np
import matplotlib.pyplot as plt
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
# Variables

_url = 'https://api.projectoxford.ai/emotion/v1.0/recognize'
#_key = None #Here you have to paste your primary key
#_maxNumRetries = 10


def processRequest( json, data, headers, params ):

    """
    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )

        if response.status_code == 429: 

            print( "Message: %s" % ( response.json()['error']['message'] ) )

            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                result = None 
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                if 'application/json' in response.headers['content-type'].lower(): 
                    result = response.json() if response.content else None 
                elif 'image' in response.headers['content-type'].lower(): 
                    result = response.content

        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json()['error']['message'] ) )

        break
        
    return result




def renderResultOnImage( result, img ):
    
    """Display the obtained results onto the input image"""
    
    for currFace in result:
        faceRectangle = currFace['faceRectangle']
        cv2.rectangle( img,(faceRectangle['left'],faceRectangle['top']),
                           (faceRectangle['left']+faceRectangle['width'], faceRectangle['top'] + faceRectangle['height']),
                       color = (255,0,0), thickness = 5 )


    for currFace in result:
        faceRectangle = currFace['faceRectangle']
        currEmotion = max(currFace['scores'].items(), key=operator.itemgetter(1))[0]



        textToWrite = "%s" % ( currEmotion )
	

	target = open("emo.txt", 'w')
	print (str(currEmotion))
	mood = str(currEmotion)
	if mood=='happiness':
		target.write('happy,happy,goofy,gripping,sweet,sunday,cute')
	elif mood=='sadness':
		target.write('sad,heart-warming,cute,funny,uplifting,absorbing,relatable')
	elif mood=='anger':
		target.write('anger,action-packed,fast,intense,uplifting,no-brainer')
	elif mood=='neutral':
		target.write('neutral,well-cast,thought-provoking,thrilling,funny')
	elif mood=='surprise':
		target.write('surprise,shocking,mysterious,fascinating,powerful')
	else:
		target.write('none')
	target.close()
        #cv2.putText( img, textToWrite, (faceRectangle['left'],faceRectangle['top']-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1 )


pathToFileInDisk = r'./pic1.jpg'
with open( pathToFileInDisk, 'rb' ) as f:
    data = f.read()

headers = dict()
headers['Ocp-Apim-Subscription-Key'] = '51f9f6f868294910a56711ee87ce9eac'
headers['Content-Type'] = 'application/octet-stream'

json = None
params = None

result = processRequest( json, data, headers, params )

if result is not None:
    # Load the original image from disk
    data8uint = np.fromstring( data, np.uint8 ) # Convert string to an unsigned int array

    img = cv2.cvtColor( cv2.imdecode( data8uint, cv2.IMREAD_COLOR ), cv2.COLOR_BGR2RGB )
    renderResultOnImage( result, img )
    
    #ig, ax = plt.subplots(figsize=(15, 20))
    #ax.imshow( img )
    #plt.show()

