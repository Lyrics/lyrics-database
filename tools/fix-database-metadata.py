#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

srcDir = "../database"

regexp = re.compile(r'_{2}')

# 1. Loop through letters in the database
for letter in sorted(os.listdir(srcDir)):
    print letter
    letterPath = os.path.join(srcDir, letter)
    if os.path.isdir(letterPath):
        letters = sorted(os.listdir(letterPath), key=str.lower)
        # 2. Loop through artists starting with letter x
        for artist in letters:
            artistPath = os.path.join(letterPath, artist)
            if os.path.isdir(artistPath):
                albums = sorted(os.listdir(artistPath), key=str.lower)
                # 3. Loop through artist's albums
                for album in albums:
                    albumPath = os.path.join(artistPath, album)
                    if os.path.isdir(albumPath):
                        songs = sorted(os.listdir(albumPath), key=str.lower)
                        # 4. Loop through songs
                        for song in songs:
                            songPath = os.path.join(albumPath, song)
                            if os.path.isfile(songPath):
                                lyrics = open(songPath, 'r').read().strip()
                                if not regexp.search(lyrics):
                                    metaName = 'Name  ' + song
                                    metaArtist = 'Artist  ' + artist
                                    metaAlbum = 'Album  ' + album
                                    metadata = '\n\n' + '_' * len(metaName) + '\n' + metaName + '\n' + metaArtist + '\n' + metaAlbum + '\n'
                                    songFile = open(songPath, 'w')
                                    songFile.write(lyrics + metadata)
