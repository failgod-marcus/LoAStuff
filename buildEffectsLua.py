#!/usr/bin/env python3
import re
import os

animations = set()
effects = set()
sounds = set()

def findEffects(filepath):
    with open(filepath, 'rb', 0) as file:
        for line in file:
            if b'PlayAnimation(' in line:
                animations.add(getEffectName(line))
            if b'PlayEffect(' in line:
                effects.add(getEffectName(line))
            if b'PlayEffectAtLoc(' in line:
                effects.add(getEffectName(line))
            if b'PlayObjectSound(' in line:
                sounds.add(getEffectName(line))

def getEffectName(str_as_bytes):
    str = str_as_bytes.decode()
    pattern = re.compile(r'"*(.+?)"')
    results = pattern.findall(str)
    if results:
        return results[1]
    else:
        return None

def scanAllFiles(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".lua"):
                filepath = os.path.join(root, file)
                findEffects(filepath)

def generateLuaList(lualist, header):
    string = header + " = {\n"
    for entry in lualist:
        if entry:
            entryString = '"' + entry + '",\n'
            string += entryString
    string += '},\n'
    return string

def saveLuaFile():
    completeString = 'EffectPlayer = {\n'
    completeString += generateLuaList(animations, 'AnimationEffects')
    completeString += generateLuaList(sounds, 'SoundEffects')
    completeString += generateLuaList(effects, 'VisualEffects')
    completeString += '}'
    file = open('EffectPlayer.lua', 'w')
    file.write(completeString)
    file.close()

scanAllFiles(".")
saveLuaFile()
