#!/usr/bin/env python3

import importlib.util
import os
import re

CODE_OK   = 0
CODE_WARN = 1
CODE_ERR  = 2

def formatTestName(fileName):
  result = re.match(r'\d+-(.*).py', fileName)
  name = result[1]
  name = name.replace('-', ' ')
  name = name.capitalize()
  return name

# Load test modules
testModules = {}
testModulesDirectory = "database-tests.d"
for moduleFilename in sorted(os.listdir(testModulesDirectory), key=str.lower):
  if moduleFilename.endswith(".py"):
    spec = importlib.util.spec_from_file_location(moduleFilename, os.path.join(testModulesDirectory, moduleFilename))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    testName = formatTestName(moduleFilename)
    testModules[testName] = {}
    for testAttrName in module.__dict__.keys():
      if testAttrName.startswith('test'):
        testModules[testName][testAttrName] = getattr(module, testAttrName)

# Read files into memory
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
                  't': 'TODO',
                  'm': 'TODO'
                }

# Run tests and write logs
for testModuleFilename in testModules:
  print(testModuleFilename)
  # TODO: write logs
  for testName in testModules[testModuleFilename]:
    tret = CODE_OK
    for path in database:
      item = database[path]
      ret = testModules[testModuleFilename][testName](path, item['b'], item['c'], item['t'], item['m'])
      if ret > tret:
        tret = ret
      # TODO: log this into a file
    if ret == CODE_ERR:
      print('[ERROR]', testName)
      break
    elif ret == CODE_WARN:
      print('[WARNING]', testName)
    else:
      print('[OK]', testName)
