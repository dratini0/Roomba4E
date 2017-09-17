########### Python 3.2 #############

##take pic, send to server, return what it thinks it is
import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import picamera, time

def image_analysis():
    
    camera = picamera.PiCamera()
    camera.rotation = 180
    
    imageInfo = {}
    
    headers = {
            # Request headers
            'Content-Type': 'application/octet-stream',
            'Prediction-key': '91916ba6f068410e86e939028982bc2a',
    }

    camera.capture('image.jpg')
    
    time.sleep(1)
    
    f = open('image.jpg','rb')
    image = f.read()
    f.close()
    #os.remove('image.jpg')

    params = urllib.parse.urlencode({
    # Request parameters
   'iterationId': '47f3a19e-e08d-4212-a0dc-ebef32f40dce',
   #'application': 'quicktest',
    })


    conn = http.client.HTTPSConnection('southcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "https://southcentralus.api.cognitive.microsoft.com/customvision/v1.0/Prediction/f584ed23-b5b8-4b96-954d-a2f80ea0c373/inline/image?%s" %params, image, headers)
    response = conn.getresponse()
    data = response.read().decode("ascii")

    
    d = json.loads(data)

    for i in range (0,len(d["Predictions"])):
        imageInfo[str(d["Predictions"][i]["Tag"])] = d["Predictions"][i]["Probability"]
    
    conn.close() 
       
    return(imageInfo)

    


print(image_analysis())
####################################