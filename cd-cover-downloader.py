import os
import shutil
import requests
import discogs_client

d = discogs_client.Client('Mozilla/5.0',
                          user_token='your_user_token')  # You will have to create an discogs account and go to this link: https://www.discogs.com/de/settings/developers

path = 'your_cd_directory'
list_ = os.listdir(path)
total = len(list_)
failures = []
skips = []
counter = 0


def fetchcover(dir, counter):
    album = dir

    if os.path.exists(path + '/' + dir + '/force_skip'):
        print(album + " (" + str(counter) + "/" + str(total) + ")")
        print("Album force skipped")
        skips.append(album)
        return False

    elif os.path.isfile(path + "/" + dir):
        return False

    elif os.path.isdir(path + '/' + dir):
        try:
            results = d.search(album, type="release")
            result = results.page(0)[1]
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


for dir_ in list_:
    counter += 1
    fetchcover(dir_, counter)

if failures:
    print("")
    print("The Following Album(s) could not be processed: ")
    for album in failures:
        print(album)

    if skips:
        print("")
        print("The Following Album(s) were force skipped: ")
        for album in skips:
            print(album)
if not failures:
    print("")
    print("All Album(s) were successfully processed")

    if skips:
        print("")
        print("The Following Album(s) were force skipped: ")
        for album in skips:
            print(album)