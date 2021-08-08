#!/usr/bin/python3
import spotipy
from os import getcwd
from spotipy.oauth2 import SpotifyOAuth

scopes = "user-read-playback-state"
clientId = input("Input client id: ")
secretId = input("Input secret id: ")
redirect = input("Input redirect URI: ")
sp = SpotifyOAuth(client_id=clientId, client_secret=secretId, redirect_uri=redirect, scope=scopes, cache_path=getcwd() + "/sp_token")
sp.get_access_token()
print("Done")
