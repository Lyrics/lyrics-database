CODE_OK   = 0
CODE_WARN = 1
CODE_ERR  = 2

def testForNewlineAtEndOfFile(path, bytes, contents, text, metadata):
  if not contents.endswith('\n'):
    return CODE_ERR
  return CODE_OK

def testForNoUnusualCharacters(path, bytes, contents, text, metadata):
  unusualChars = ['`', '©']
  for char in unusualChars:
    if char in contents:
      return CODE_ERR
  return CODE_OK

def testForNoSpacesAroundLines(path, bytes, contents, text, metadata):
  for line in contents.splitlines():
    # if line.startswith(' ') or line.endswith(' '):
    if line.endswith(' '):
      return CODE_ERR
  return CODE_OK

def testForTests(*_):
  def testTestForNewlineAtEndOfFile():
    passing = testForNewlineAtEndOfFile('', b'', 'La la la\n', '', {}) == CODE_OK 
    failing = testForNewlineAtEndOfFile('', b'', 'La la', '', {}) == CODE_ERR
    return passing and failing

  def testTestForNoUnusualCharacters():
    passing = testForNoUnusualCharacters('', b'', 'La la la\n', '', {}) == CODE_OK 
    failing = testForNoUnusualCharacters('', b'', '`La la`\n', '', {}) == CODE_ERR
    return passing and failing

  def testTestForNoSpacesAroundLines():
    passing = testForNoSpacesAroundLines('', b'', 'La la la\nLa la\nLa\n', '', {}) == CODE_OK 
    failing = testForNoSpacesAroundLines('', b'', 'La la \n La \n', '', {}) == CODE_ERR
    return passing and failing

  if not testTestForNewlineAtEndOfFile():
    return CODE_ERR
  if not testTestForNoUnusualCharacters():
    return CODE_ERR
  if not testTestForNoSpacesAroundLines():
    return CODE_ERR
  return CODE_OK
