########### Python 3.2 #############

##take pic, send to server, return what it thinks it is
import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import picamera, time

def image_analysis():
    
    with picamera.PiCamera() as camera:
        camera.rotation = 180
        camera.capture('image.jpg')
        
    headers = {
            # Request headers
            'Content-Type': 'application/octet-stream',
            'Prediction-key': 'fc40ccc6a5ad4729b9151ede4f1a7fd1',
    }

    f = open('image.jpg','rb')
    image = f.read()
    f.close()
    #os.remove('image.jpg')

    params = urllib.parse.urlencode({
    # Request parameters
   'iterationId': 'c3cfe161-a9e8-4bcd-a5a2-05a980d96563',
   #'application': 'quicktest',
    })


    conn = http.client.HTTPSConnection('southcentralus.api.cognitive.microsoft.com')
    conn.request("POST","https://southcentralus.api.cognitive.microsoft.com/customvision/v1.0/Prediction/cd8cb564-37bf-442a-842e-87857dd9359b/inline/image?%s" %params, image, headers)
    
    # "https://southcentralus.api.cognitive.microsoft.com/customvision/v1.0/Prediction/f584ed23-b5b8-4b96-954d-a2f80ea0c373/inline/image?%s
    
    response = conn.getresponse()
    data = response.read().decode("ascii")
    
    d = json.loads(data)

    imageInfo = {}

    for i in range (0,len(d["Predictions"])):
        imageInfo[str(d["Predictions"][i]["Tag"])] = d["Predictions"][i]["Probability"]
    
    conn.close() 
       
    return(imageInfo)

    


print(image_analysis())
####################################