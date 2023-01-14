# cd-cover-downloader

Cd Cover Downloader using the Discogs API to search Albums and fetch the Album Covers

## Requirements

You will have to install the discogs_client in order for this to work. You will also have to create an discogs account and afterwards create an user_token [here](https://www.discogs.com/de/settings/developers)

## Manually Adding Covers

In order to manually add covers you will have to create a file called "force_skip" or the cover will be replaced at every run

## Refreshing the Cache

The script has a cache because there is no need to always redownload covers and this way only new album covers will be downloaded.
In order to clear that cache you will have to either delete the cache.pickle file created in the directory or use the -r option
