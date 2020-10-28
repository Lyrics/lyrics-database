#!/usr/bin/env python3

# Imports
import importlib.util
import os
import re
import sys
import time

# Exit/return codes
CODE_OK   = 0
CODE_WARN = 1
CODE_ERR  = 2

class colors:
  SUCCESS = '\033[92m'
  WARNING = '\033[93m'
  ERROR = '\033[91m'
  RESET_ALL = '\033[0m'

def formatTestModuleName(fileName):
  result = re.match(r'\d+-(.*).py', fileName)
  name = result[1]
  name = name.replace('-', ' ')
  name = name.capitalize()
  return name

def formatTestName(functionName):
  return re.sub(r'(?<!^)(?=[A-Z])', ' ', functionName).lower().capitalize()

def formatStatLine(key, value):
  return '{:·<53}{}'.format(key, value)

def splitLyricsIntoTextAndMetadata(lyricsFileContents):
  return re.split('_+', lyricsFileContents)

def getText(lyricsFileContents):
  partials = splitLyricsIntoTextAndMetadata(lyricsFileContents)
  lyricsText = ""
  if len(partials) > 1:
    lyricsText = partials[0]
  else:
    lyricsText = lyricsFileContents
  ## Trim text
  lyricsText = lyricsText.strip()
  return lyricsText

def getMetadata(lyricsFileContents):
  partials = splitLyricsIntoTextAndMetadata(lyricsFileContents)
  lyricsMetadata = ""
  if len(partials) > 1:
    lyricsMetadata = partials[1]
    ## Trim metadata
    lyricsMetadata = lyricsMetadata.strip()
  return lyricsMetadata

def parseMetadata(metadata):
  datalines = []
  for line in metadata.splitlines():
    line = line.rstrip() ## Discard trailing whitespaces
    if line[0] == ' ':
      if len(datalines) == 0:
        print('Warning: metadata keys cannot begin with a space')
      else:
        ## The value is split between multiple lines,
        ## append this line to the previous one
        datalines[-1] += line
    else:
      datalines.append(line)
  dictionary = {}
  for dataline in datalines:
    partials = re.split('\s{2,}', dataline)
    key = partials[0]
    rawvalue = dataline[len(key):].strip()
    valuepartials = re.split(',\s{2,}', rawvalue)
    dictionary[key] = valuepartials
  return dictionary

def supports_colors():
    supported_platform = sys.platform != 'win32' or 'ANSICON' in os.environ
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    return supported_platform and is_a_tty

def formatTestStatusLabel(code):
  result = '['
  if code == CODE_OK:
    if supports_colors():
      result += colors.SUCCESS
    result += 'OK'
  elif code == CODE_WARN:
    if supports_colors():
      result += colors.WARNING
    result += 'WARN'
  elif code == CODE_ERR:
    if supports_colors():
      result += colors.ERROR
    result += 'ERR'
  if supports_colors():
    result += colors.RESET_ALL
  result += ']'
  return result

# Mark test script start time
startTime = time.process_time()

# 1. Load test modules
testModules = {}
testModulesDirectory = "database-tests.d"
testCount = 0
for moduleFilename in sorted(os.listdir(testModulesDirectory), key=str.lower):
  if moduleFilename.endswith(".py"):
    spec = importlib.util.spec_from_file_location(moduleFilename, os.path.join(testModulesDirectory, moduleFilename))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    testName = formatTestModuleName(moduleFilename)
    testModules[testName] = {}
    for testAttrName in module.__dict__.keys():
      if testAttrName.startswith('test'):
        testModules[testName][testAttrName] = getattr(module, testAttrName)
        testCount += 1

# 2. Read files into memory
# TODO convert it into a function
database = {}
databaseSourceDir = '../database'
for letter in sorted(next(os.walk(databaseSourceDir))[1]):
    letterPath = os.path.join(databaseSourceDir, letter)
    letterShortPath = os.path.join(letter)
    if os.path.isfile(letterPath):
      database[letterShortPath] = { 'b': b'', 'c': '', 't': '', 'm': '' }
    else:
      for artist in sorted(next(os.walk(letterPath))[1], key=str.lower):
        artistPath = os.path.join(letterPath, artist)
        artistShortPath = os.path.join(letter, artist)
        if os.path.isfile(artistPath):
          database[artistShortPath] = { 'b': b'', 'c': '', 't': '', 'm': '' }
        else:
          for album in sorted(next(os.walk(artistPath))[1], key=str.lower):
            albumPath = os.path.join(artistPath, album)
            albumShortPath = os.path.join(letter, artist, album)
            if os.path.isfile(artistPath):
              database[artistShortPath] = { 'b': b'', 'c': '', 't': '', 'm': '' }
            else:
              for recording in sorted(next(os.walk(albumPath))[2], key=str.lower):
                recordingPath = os.path.join(albumPath, recording)
                # Read file as bytes
                file = open(recordingPath, 'rb')
                lyricsFileBinaryContents = file.read()
                file.close()
                lyricsFileContents = lyricsFileBinaryContents.decode('utf-8')
                recordingShortPath = os.path.join(letter, artist, album, recording)
                database[recordingShortPath] = {
                  'b': lyricsFileBinaryContents,
                  'c': lyricsFileContents,
                  't': getText(lyricsFileContents),
                  'm': parseMetadata(getMetadata(lyricsFileContents))
                }

# 3. Run tests
testErrorCount = 0
testWarningCount = 0
testOkCount = 0
errorCausingFiles = {}
warningCausingFiles = {}
okFiles = {}
for path in database:
  okFiles[path] = 1
# Iterate through test modules
for testModuleFilename in testModules:
  print(testModuleFilename + ':')
  # Iterate through tests within the current test module
  for testName in testModules[testModuleFilename]:
    readableTestName = formatTestName(testName)
    testres = CODE_OK
    if testName == "testTheTests":
      # Run self-tests only once instead of for every item
      res = testModules[testModuleFilename]["testTheTests"]()
      if res != CODE_OK:
        print('Failed to pass ' + readableTestName.lower())
        testErrorCount += 1
      if res > testres:
        testres = res
    else:
      # Perform current test on every item in the database
      for path in database:
        item = database[path]
        res = testModules[testModuleFilename][testName](path, item['b'], item['c'], item['t'], item['m'])
        if res == CODE_ERR:
          print('Failed to pass ' + readableTestName.lower() + ' (error):', path, file=sys.stderr)
          testErrorCount += 1
          errorCausingFiles[path] = 1
          okFiles.pop(path, None)
        elif res == CODE_WARN:
          print('Failed to pass ' + readableTestName.lower() + ' (warning):', path, file=sys.stderr)
          testWarningCount += 1
          warningCausingFiles[path] = 1
          okFiles.pop(path, None)
        if res > testres:
          testres = res
    if testres == CODE_ERR:
      print(formatTestStatusLabel(CODE_ERR), readableTestName)
      # continue # No need to continue with this test after first error
    elif testres == CODE_WARN:
      print(formatTestStatusLabel(CODE_WARN), readableTestName)
    else:
      print(formatTestStatusLabel(CODE_OK), readableTestName)
  # Separate output of test modules with a single newline
  print()

# 4. Print stats
lines = [
  formatStatLine("Test module count", str(len(testModules))),
  formatStatLine("Total number of tests", testCount),
  formatStatLine("Number of errors triggered by tests", testErrorCount),
  formatStatLine("Number of warnings triggered by tests", testWarningCount),
  formatStatLine("Total number of texts in the database", len(database)),
  formatStatLine("Number of text files that contain errors", len(errorCausingFiles)),
  formatStatLine("Number of text files that contain warnings", len(warningCausingFiles)),
  formatStatLine("Number of text files without errors or warnings", len(okFiles)),
  formatStatLine("Percentage of text files without errors or warnings", '{0:.2f}'.format(len(okFiles) / len(database) * 100) + '%'),
  formatStatLine("Test suite running time", '{0:.3f}'.format(time.process_time() - startTime) + 's'),
]
print("_" * len(lines[0]))
for line in lines:
  print(line)
print("‾" * len(lines[-1]))
print() # Print newline at end for equal vertical margin

# 5. Return proper exit code
if testErrorCount > 0:
  sys.exit(CODE_ERR)
else:
  sys.exit(CODE_OK)
