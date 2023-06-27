import json
import urllib.request

# Download the given file
def download_file(url, filename):
    try:
        print("Downloading file:", filename)
        urllib.request.urlretrieve(url, filename)
        print("File downloaded:", filename)
    except Exception as e:
        print("Error downloading file", filename + ":", str(e))

json_file = "Representation\BeeSoundParsing\src\ScrappingRobot\ToBeeOrNotToBee.json"

try:
    file = open(json_file)
    data = json.load(file)
    files = data["files"]

    for file_data in files:
        download_link = file_data["links"]["self"]
        filename = "Representation\BeeDataset\FromWeb\\" + file_data["key"]
        download_file(download_link, filename)
    print("All files downloaded successfully!")

except FileNotFoundError:
    print("File not found:", json_file)
except json.JSONDecodeError:
    print("Invalid JSON file:", json_file)
