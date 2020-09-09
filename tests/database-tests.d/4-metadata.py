CODE_OK   = 0
CODE_WARN = 1
CODE_ERR  = 2

def testForMetadataToBePresent(path, bytes, contents, text, metadata):
  if len(metadata) < 1:
    return CODE_ERR
  return CODE_OK

def testTheTests(*_):
  def testTheTestForMetadataToBePresent():
    passing = testForMetadataToBePresent('', b'', '', '', { 'Name': 'Song Name', 'Artist': 'Artist Name' }) == CODE_OK
    failing = testForMetadataToBePresent('', b'', '', '', {}) == CODE_ERR
    return passing and failing
  if not testTheTestForMetadataToBePresent():
    return CODE_ERR
  return CODE_OK
