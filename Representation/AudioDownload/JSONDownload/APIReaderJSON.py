import json
import urllib.request


def download_file(url : str, fileName : str, verbose : bool = False):
    # Download the given file with an url
    # @arguments : - url : url of the file to download
    #              - fileName : name of the file to save
    #              - verbose : do we want to print or not (default : False)

    try:
        if verbose :
            print("Downloading file:", fileName)

        urllib.request.urlretrieve(url, fileName)

        if verbose :
            print("File downloaded:", fileName)
    except Exception as e:
        print(f"Warning : Could not download {fileName} : {str(e)}")


if __name__ == "__main__" :
    json_file = "Representation\AudioDownload\JSONDownload\ToBeeOrNotToBee.json"

    try:
        # Download JSON file
        file = open(json_file)
        data = json.load(file)
        files = data["files"]

        # Download all the files
        for file_data in files:
            download_link = file_data["links"]["self"]
            fileName = "Audio\\beeDataset\\RawFilesFromWeb\\" + file_data["key"]
            download_file(download_link, fileName)
        print("All files downloaded successfully!")

    except FileNotFoundError:
        print(f"File not found : {json_file}")
    except json.JSONDecodeError:
        print(f"Invalid JSON File : {json_file}")
