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

for dir_ in list_:
    if os.path.isdir(path + '/' + dir_):
        album = dir_
        counter += 1
        try:
            results = d.search(album)
            result = results.page(0)[1]

            images = result.images
            image = images[0]
            imageurl = image['uri']
            ext = imageurl.rsplit(".", 1)[1]
        except:
            print(album + " (" + str(counter) + "/" + str(total) + ")")
            print("An exception error for occurred")
            failures.append(album)
            continue

        imageres = requests.get(imageurl, stream=True, headers={"User-Agent": 'Mozilla/5.0'})

        if imageres.status_code == 200:
            with open(path + "/" + dir_ + "/cover." + ext, 'wb') as f:
                shutil.copyfileobj(imageres.raw, f)
            print(album + " (" + str(counter) + "/" + str(total) + ")")
            print("Album Cover Successfully downloaded")
        else:
            print(album + " (" + str(counter) + "/" + str(total) + ")")
            print("Album Cover failed to download")
            failures.append(album)

    if os.path.isfile(path + "/" + dir_):
        continue

if failures:
    print("")
    print("The Following Albums could not be processed, please verify that their names are correct or download the covers manually")
    for album in failures:
        print(album)
if not failures:
    print("")
    print("All Covers have been downloaded successfully")