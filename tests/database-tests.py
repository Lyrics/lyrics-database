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
  BOLD = '\033[1m'
  RESET_ALL = '\033[0m'

def formatTestModuleName(fileName):
  result = re.match(r'\d+-(.*).py', fileName)
  name = result[1]
  name = name.replace('-', ' ')
  name = name.capitalize()
  return name

def formatTestName(functionName):
  return re.sub(r'(?<!^)(?=[A-Z])', ' ', functionName).lower().capitalize()

def formatStatsLine(key, value):
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

def supportsColors():
    supported_platform = sys.platform != 'win32' or 'ANSICON' in os.environ
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    return supported_platform and is_a_tty

def formatTestStatusLabel(code):
  result = '['
  if code == CODE_OK:
    if supportsColors():
      result += colors.SUCCESS
    result += 'OK'
  elif code == CODE_WARN:
    if supportsColors():
      result += colors.WARNING
    result += 'WARN'
  elif code == CODE_ERR:
    if supportsColors():
      result += colors.ERROR
    result += 'ERR'
  if supportsColors():
    result += colors.RESET_ALL
  result += ']'
  return result

def boldText(text):
  if supportsColors():
    return colors.BOLD + text + colors.RESET_ALL
  else:
    return text

def printStats(lines):
  print("_" * len(lines[0]))
  for line in lines:
    print(line)
  print("‾" * len(lines[-1]))
  print() # Print newline at end for equal vertical margin

def readDatabaseDirectory(databaseSourceDir):
  database = {}
  for letter in sorted(os.listdir(databaseSourceDir)):
    letterPath = os.path.join(databaseSourceDir, letter)
    if os.path.isfile(letterPath):
      database[letter] = { 'b': b'', 'p': '', 'l': '', 'm': '' }
    else:
      for artist in sorted(os.listdir(letterPath), key=str.lower):
        artistPath = os.path.join(letterPath, artist)
        artistShortPath = os.path.join(letter, artist)
        if os.path.isfile(artistPath):
          database[artistShortPath] = { 'b': b'', 'p': '', 'l': '', 'm': '' }
        else:
          for album in sorted(os.listdir(artistPath), key=str.lower):
            albumPath = os.path.join(artistPath, album)
            albumShortPath = os.path.join(artistShortPath, album)
            if os.path.isfile(albumPath):
              database[albumShortPath] = { 'b': b'', 'p': '', 'l': '', 'm': '' }
            else:
              for recording in sorted(os.listdir(albumPath), key=str.lower):
                recordingPath = os.path.join(albumPath, recording)
                # Read file as bytes
                file = open(recordingPath, 'rb')
                lyricsFileBinaryContents = file.read()
                file.close()
                lyricsFileContents = lyricsFileBinaryContents.decode('utf-8')
                recordingShortPath = os.path.join(letter, artist, album, recording)
                database[recordingShortPath] = {
                  'b': lyricsFileBinaryContents,
                  'p': lyricsFileContents,
                  'l': getText(lyricsFileContents),
                  'm': parseMetadata(getMetadata(lyricsFileContents))
                }
  return database

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
database = readDatabaseDirectory('../database')

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
  print(boldText(testModuleFilename + ' tests') + ':')
  # Iterate through tests within the current test module
  for testName in testModules[testModuleFilename]:
    readableTestName = formatTestName(testName)
    testres = CODE_OK
    if testName == "testForTests":
      # Run self-tests only once instead of for every item in the database
      res = testModules[testModuleFilename]["testForTests"]()
      if res != CODE_OK:
        print('Failed to pass ' + readableTestName.lower())
        testErrorCount += 1
      if res > testres:
        testres = res
    else:
      # Perform current test on every item in the database
      for path in database:
        item = database[path]
        res = testModules[testModuleFilename][testName](path, item['b'], item['p'], item['l'], item['m'], database)
        if res == CODE_ERR:
          print('Failed to pass ' + readableTestName + ' (error):', path, file=sys.stderr)
          testErrorCount += 1
          errorCausingFiles[path] = 1
          okFiles.pop(path, None)
        elif res == CODE_WARN:
          print('Failed to pass ' + readableTestName + ' (warning):', path, file=sys.stderr)
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

# 4. Print stats summary
printStats([
  formatStatsLine("Test module count", str(len(testModules))),
  formatStatsLine("Total number of tests", testCount),
  formatStatsLine("Number of errors triggered by tests", testErrorCount),
  formatStatsLine("Number of warnings triggered by tests", testWarningCount),
  formatStatsLine("Total number of texts in the database", len(database)),
  formatStatsLine("Number of text files that contain errors", len(errorCausingFiles)),
  formatStatsLine("Number of text files that contain warnings", len(warningCausingFiles)),
  formatStatsLine("Number of text files without errors or warnings", len(okFiles)),
  formatStatsLine("Percentage of text files without errors or warnings", '{0:.2f}'.format(len(okFiles) / len(database) * 100) + '%'),
  formatStatsLine("Test suite running time", '{0:.3f}'.format(time.process_time() - startTime) + 's'),
])

# 5. Return proper exit code
if testErrorCount > 0:
  sys.exit(CODE_ERR)
else:
  sys.exit(CODE_OK)
