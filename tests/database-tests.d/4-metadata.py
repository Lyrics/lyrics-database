CODE_OK   = 0
CODE_WARN = 1
CODE_ERR  = 2

def testForMetadataToBePresent(path, bytes, plaintext, lyrics, metadata, database):
  if len(metadata) < 1:
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

def testForIdenticalTrackNumbers(path, bytes, plaintext, lyrics, metadata, database):
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

def testTheTests(*_):
  def testTheTestForMetadataToBePresent():
    passing = testForMetadataToBePresent('', b'', '', '', { 'Name': 'Song Name', 'Artist': 'Artist Name' }, {}) == CODE_OK
    failing = testForMetadataToBePresent('', b'', '', '', {}, {}) == CODE_ERR
    return passing and failing
  def testTheTestForUnknownMetadataKeys():
    passing = testForUnknownMetadataKeys('', b'', '', '', { 'Name': 'Song Name', 'Artist': 'Artist Name' }, {}) == CODE_OK
    failing = testForUnknownMetadataKeys('', b'', '', '', { 'Copyright': 'Some company' }, {}) == CODE_ERR
    return passing and failing
  def testTheTestForIdenticalTrackNumbers():
    passing = testForIdenticalTrackNumbers('', b'', '', '', { 'Track no': '1' }, {}) == CODE_OK
    mockDatabase = { 'A/Artist/Album/Recording 2': { 'b': '', 'p': '', 'l': '', 'm': { 'Track no': '6' } } }
    failing = testForIdenticalTrackNumbers('A/Artist/Album/Recording', b'', '', '', { 'Track no': '6' }, mockDatabase) == CODE_ERR
    return passing and failing
  if not testTheTestForMetadataToBePresent()\
  or not testTheTestForUnknownMetadataKeys()\
  or not testTheTestForIdenticalTrackNumbers():
    return CODE_ERR
  return CODE_OK
