import os
import shutil
import requests
import discogs_client

d = discogs_client.Client('Mozilla/5.0', user_token='your_user_token') # You will have to create an discogs account and go to this link: https://www.discogs.com/de/settings/developers

path = 'your_cd_directory'
list_ = os.listdir(path)
total = len(list_)
failures = []
counter = 0

def fetchcover(dir, counter):
    if os.path.isdir(path + '/' + dir):
        album = dir
        try:
            results = d.search(album, type="release, master")
            result = results.page(0)[0]
            images = result.images
            image = images[0]
            imageurl = image['uri']
            ext = imageurl.rsplit(".", 1)[1]
        except:
            print(album + " (" + str(counter) + "/" + str(total) + ")")
            print("An exception error occurred")
            failures.append(album)
            return False

        imageres = requests.get(imageurl, stream=True, headers={"User-Agent": 'Mozilla/5.0'})

        if imageres.status_code == 200:
            with open(path + "/" + dir + "/cover." + ext, 'wb') as f:
                shutil.copyfileobj(imageres.raw, f)
            print(album + " (" + str(counter) + "/" + str(total) + ")")
            print("Album Cover Successfully downloaded")
        else:
            print(album + " (" + str(counter) + "/" + str(total) + ")")
            print("Album Cover failed to download")
            failures.append(album)

    if os.path.isfile(path + "/" + dir):
        return False

for dir_ in list_:
    counter += 1
    fetchcover(dir_, counter)

if len(failures) == 1:
    print("")
    print("The Following Album could not be processed. Please verify their names are correct or consider downloading them manually.")
    for album in failures:
        print(album)
elif failures:
    print("")
    print("The Following " + str(len(failures)) + " Albums could not be processed. Please verify their names are correct or consider downloading them manually.")
    for album in failures:
        print(album)
if not failures:
    print("")
    print("All Covers have been downloaded successfully.")