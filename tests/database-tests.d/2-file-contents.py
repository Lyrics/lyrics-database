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

def testTheTests(*_):
  def testTheTestForNewlineAtEndOfFile():
    passing = testForNewlineAtEndOfFile('', b'', 'La la la\n', '', {}) == CODE_OK 
    failing = testForNewlineAtEndOfFile('', b'', 'La la', '', {}) == CODE_ERR
    return passing and failing
  def testTheTestForNoUnusualCharacters():
    passing = testForNoUnusualCharacters('', b'', 'La la la\n', '', {}) == CODE_OK 
    failing = testForNoUnusualCharacters('', b'', '`La la`\n© Some Publishing Company, LLC', '', {}) == CODE_ERR
    return passing and failing
  if not testTheTestForNewlineAtEndOfFile() \
  or not testTheTestForNoUnusualCharacters():
    return CODE_ERR
  return CODE_OK
