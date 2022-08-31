CODE_OK   = 0
CODE_WARN = 1
CODE_ERR  = 2

def testForMetadataToBePresent(path, bytes, plaintext, lyrics, metadata, database):
  if len(metadata) < 1:
    return CODE_ERR
  return CODE_OK

def testForRequiredMetadataKeysToBePresent(path, bytes, plaintext, lyrics, metadata, database):
  if not 'Name' in metadata or not 'Artist' in metadata:
    return CODE_ERR
  return CODE_OK

def testForUnknownMetadataKeys(path, bytes, plaintext, lyrics, metadata, database):
  keys = list(metadata.keys())
  knownMetadataKeys = [
    "Name",
    "Artist",
    "Album",
    "Disc no",
    "Track no",
    "Year",
    "Language",
    "MusicBrainz ID",
    "Cover of",
    "Parody of",
    "Samples",
    "Original text by",
    "Original text copyright",
  ]
  for key in keys:
    if not key in knownMetadataKeys:
      return CODE_ERR
  return CODE_OK

def testForDuplicateTrackNumbers(path, bytes, plaintext, lyrics, metadata, database):
  trackNumber = metadata['Track no'] if 'Track no' in metadata else None
  if trackNumber != None:
    albumPath = "/".join(path.split("/")[:-1]) + "/"
    discNumber = metadata['Disc no'] if 'Disc no' in metadata else None
    for (k, v) in database.items():
      if k.startswith(albumPath) and k != path:
          tN = v['m']['Track no'] if 'Track no' in v['m'] else None
          if tN != None:
            if discNumber == None:
              if tN == trackNumber:
                return CODE_ERR
            else:
              dN = v['m']['Disc no'] if 'Disc no' in v['m'] else None
              if dN != None:
                if dN == discNumber and tN == trackNumber:
                  return CODE_ERR
  return CODE_OK

def testForMatchingArtistNames(path, bytes, plaintext, lyrics, metadata, database):
  trackArtist = metadata['Artist'][0] if 'Artist' in metadata else None
  if trackArtist != None:
    albumPath = "/".join(path.split("/")[:-1]) + "/"
    for (k, v) in database.items():
      if k.startswith(albumPath) and k != path:
          tA = v['m']['Artist'][0] if 'Artist' in v['m'] else None
          if tA != None and tA != trackArtist:
                return CODE_ERR
  return CODE_OK

def testForMatchingAlbumNames(path, bytes, plaintext, lyrics, metadata, database):
  trackAlbum = metadata['Album'][0] if 'Album' in metadata else None
  if trackAlbum != None:
    albumPath = "/".join(path.split("/")[:-1]) + "/"
    for (k, v) in database.items():
      if k.startswith(albumPath) and k != path:
          tA = v['m']['Album'][0] if 'Album' in v['m'] else None
          if tA != None and tA != trackAlbum:
                return CODE_ERR
  return CODE_OK

def testForProperMetadataLanguageValues(path, bytes, plaintext, lyrics, metadata, database):
  keys = list(metadata.keys())
  properMetadataLanguageValues = [
    "Unknown",
    "American English",
    "Australian English",
    "British English",
    "Canadian English",
    "French",
    "Italian",
    "German",
    "New Zealand English",
    "Portuguese",
    "Russian",
  ]
  if "Language" in keys:
    for language in metadata['Language']:
      if not language in properMetadataLanguageValues:
        return CODE_ERR
  return CODE_OK

def testForTests(*_):
  def testTheTestForMetadataToBePresent():
    passing = testForMetadataToBePresent('', b'', '', '', { 'Name': 'Song Name', 'Artist': 'Artist Name' }, {}) == CODE_OK
    failing = testForMetadataToBePresent('', b'', '', '', {}, {}) == CODE_ERR
    return passing and failing
  def testTheTestForRequiredMetadataKeysToBePresent():
    passing = testForRequiredMetadataKeysToBePresent('', b'', '', '', { 'Name': 'Song Name', 'Artist': 'Artist Name' }, {}) == CODE_OK
    failing = testForRequiredMetadataKeysToBePresent('', b'', '', '', {}, {}) == CODE_ERR
    return passing and failing
  def testTheTestForUnknownMetadataKeys():
    passing = testForUnknownMetadataKeys('', b'', '', '', { 'Name': 'Song Name', 'Artist': 'Artist Name' }, {}) == CODE_OK
    failing = testForUnknownMetadataKeys('', b'', '', '', { 'Copyright': 'Some company' }, {}) == CODE_ERR
    return passing and failing
  def testTheTestForDuplicateTrackNumbers():
    passing = testForDuplicateTrackNumbers('', b'', '', '', { 'Track no': '1' }, {}) == CODE_OK
    mockDatabase = { 'A/Artist/Album/Recording 2': { 'b': '', 'p': '', 'l': '', 'm': { 'Track no': '6' } } }
    failing = testForDuplicateTrackNumbers('A/Artist/Album/Recording', b'', '', '', { 'Track no': '6' }, mockDatabase) == CODE_ERR
    return passing and failing
  def testTheTestForMatchingArtistNames():
    mockDatabase = { 'A/Artist/Album/Recording 2': { 'b': '', 'p': '', 'l': '', 'm': { 'Artist': 'Artist Name' } } }
    passing = testForMatchingArtistNames('', b'', '', '', { 'Artist': 'Artist Name' }, mockDatabase) == CODE_OK
    mockDatabase = { 'A/Artist/Album/Recording 2': { 'b': '', 'p': '', 'l': '', 'm': { 'Artist': 'artist name' } } }
    failing = testForMatchingArtistNames('A/Artist/Album/Recording', b'', '', '', { 'Artist': 'Artist Name' }, mockDatabase) == CODE_ERR
    return passing and failing
  def testTheTestForMatchingAlbumNames():
    mockDatabase = { 'A/Artist/Album/Recording 2': { 'b': '', 'p': '', 'l': '', 'm': { 'Album': 'Album Name' } } }
    passing = testForMatchingAlbumNames('', b'', '', '', { 'Album': 'Album Name' }, mockDatabase) == CODE_OK
    mockDatabase = { 'A/Artist/Album/Recording 2': { 'b': '', 'p': '', 'l': '', 'm': { 'Album': 'album name' } } }
    failing = testForMatchingAlbumNames('A/Artist/Album/Recording', b'', '', '', { 'Album': 'Album Name' }, mockDatabase) == CODE_ERR
    return passing and failing
  def testTheTestForProperMetadataLanguageValues():
    passing = testForProperMetadataLanguageValues('', b'', '', '', { 'Language': [ 'American English', 'French', 'Unknown' ] }, {}) == CODE_OK
    failing = testForProperMetadataLanguageValues('', b'', '', '', { 'Language': [ 'en_US' ] }, {}) == CODE_ERR
    return passing and failing
  if not testTheTestForMetadataToBePresent() \
  or not testTheTestForRequiredMetadataKeysToBePresent() \
  or not testTheTestForUnknownMetadataKeys() \
  or not testTheTestForDuplicateTrackNumbers() \
  or not testTheTestForMatchingArtistNames() \
  or not testTheTestForMatchingAlbumNames() \
  or not testTheTestForProperMetadataLanguageValues():
    return CODE_ERR
  return CODE_OK
