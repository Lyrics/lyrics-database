CODE_OK   = 0
CODE_WARN = 1
CODE_ERR  = 2

def testForMetadataToBePresent(path, bytes, contents, text, metadata):
  if len(metadata) < 1:
    return CODE_ERR
  return CODE_OK

def testForUnknownMetadataKeys(path, bytes, contents, text, metadata):
  keys = list(metadata.keys())
  knownMetadataKeys = [
    "Name",
    "Artist",
    "Album",
    "Track no",
    "Year",
    "MusicBrainz ID",
    "Parody of",
    "Original text by",
    "Original text copyright",
  ]
  for key in keys:
    if not key in knownMetadataKeys:
      return CODE_ERR
  return CODE_OK

def testTheTests(*_):
  def testTheTestForMetadataToBePresent():
    passing = testForMetadataToBePresent('', b'', '', '', { 'Name': 'Song Name', 'Artist': 'Artist Name' }) == CODE_OK
    failing = testForMetadataToBePresent('', b'', '', '', {}) == CODE_ERR
    return passing and failing
  def testTheTestForUnknownMetadataKeys():
    passing = testForUnknownMetadataKeys('', b'', '', '', { 'Name': 'Song Name', 'Artist': 'Artist Name' }) == CODE_OK
    failing = testForUnknownMetadataKeys('', b'', '', '', { 'Copyright': 'Some company' }) == CODE_ERR
    return passing and failing
  if not testTheTestForMetadataToBePresent()\
  or not testTheTestForUnknownMetadataKeys():
    return CODE_ERR
  return CODE_OK
