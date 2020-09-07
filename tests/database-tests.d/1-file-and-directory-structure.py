CODE_OK   = 0
CODE_WARN = 1
CODE_ERR  = 2

def testForPathToAlwaysHaveFourParts(path, bytes, contents, text, metadata):
  if len(path.split('/')) != 4:
    return CODE_ERR
  return CODE_OK

def testForNoFilenameExtensions(path, bytes, contents, text, metadata):
  filename = path.split('/')[3]
  if filename.lower().endswith('.txt'):
    return CODE_WARN # Not an error because song names may produce false positives
  return CODE_OK

def testForNoSpacesWithinFileDirNames(path, bytes, contents, text, metadata):
  for part in path.split('/'):
    if part.startswith(' ') or part.endswith(' '):
      return CODE_ERR
  return CODE_OK

def testTheTests(*_):
  def testTheTestForPathToAlwaysHaveFourParts():
    passing = testForPathToAlwaysHaveFourParts('A/Artist/Album/Recording', b'', '', '', {}) == CODE_OK
    failing = testForPathToAlwaysHaveFourParts('A/Artist/Recording', b'', '', '', {}) == CODE_ERR
    return passing and failing
  def testTheTestForNoFilenameExtensions():
    passing = testForNoFilenameExtensions('A/Artist/Album/Recording', b'', '', '', {}) == CODE_OK 
    warning = testForNoFilenameExtensions('A/Artist/Album/Recording.txt', b'', '', '', {}) == CODE_WARN
    return passing and warning
  def testTheTestForNoSpacesWithinFileDirNames():
    passing = testForNoSpacesWithinFileDirNames('A/Artist/Album/Recording', b'', '', '', {}) == CODE_OK 
    failing = testForNoSpacesWithinFileDirNames(' A / Artist / Album / Recording.txt ', b'', '', '', {}) == CODE_ERR
    return passing and failing
  if not testTheTestForPathToAlwaysHaveFourParts() \
  or not testTheTestForNoFilenameExtensions() \
  or not testTheTestForNoSpacesWithinFileDirNames():
    return CODE_ERR
  return CODE_OK
