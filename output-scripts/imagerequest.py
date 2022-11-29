import sys
import requests

url = 'http://www.dev-machine.link:5000/upload_image'
filename = str(sys.argv[1])
my_img = {'image': open(filename, 'rb')}
r = requests.post(url, files=my_img)

# convert server response into JSON format.
print(r.json())
