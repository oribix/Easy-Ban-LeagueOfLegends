import sys
import json
import re

#import support for python 2 and 3
try:
  import urllib.request as urllib2
except ImportError:
  import urllib2

#constants
CHAMPION = 0
WINRATE = 1
BANRATE = 2
PICKRATE = 3
TRUEPICKRATE = 4
THREAT = 5

#flags and args
VERBOSE = False
RESULTNUM = 10
ELO = "gold"

def setVerbose():
  global VERBOSE
  VERBOSE = True
  return

def setFlag(f):
  try:
    {
      "v": setVerbose
    }[f]()
  except KeyError:
    print("No such flag '" + f + "'")
    exit()

def parseArgs(argv):
  arglen = len(argv)

  #get argument list
  longargs = []
  shortargs = []
  for arg in argv:
    if(arg.startswith("--")):
      longargs.append(arg[2:])
    elif(arg.startswith("-")):
      shortargs.append(arg[1:])
    else:
      try:
        rn = int(arg) #get the number of results to return
        global RESULTNUM
        RESULTNUM = rn
        continue
      except ValueError: pass

      global ELO
      ELO = arg

  #set short flags
  for arg in shortargs:
    for flag in arg:
      setFlag(flag)

  #set long flags
  for arg in longargs:
    continue

def threatgetter(e):
  return e[THREAT]

def printStats(champions):
  #print( list)
  for i in range(RESULTNUM):
    c = None
    if(len(champions) > 0):
      c = champions.pop()

    if(c != None):
      print( "champion:  " + c[CHAMPION])
      print( "THREAT LEVEL: " + "%.6f" % (c[THREAT] * 100) + "%")
      if(VERBOSE):
        print( "win rate:  " + "%.2f" % (c[WINRATE] * 100) + "%")
        print( "ban rate:  " + "%.2f" % (c[BANRATE] * 100) + "%")
        print( "pick rate: " + "%.2f" % (c[PICKRATE] * 100) + "%")
        print( "true pick: " + "%.2f" % (c[TRUEPICKRATE] * 100) + "%")

      print("")

def main():
  #TODO: Get default options from a file

  #parse arguments
  args = sys.argv
  args.pop(0)
  parseArgs(args)

  #generate the URL to query
  statbase = "http://champion.gg/statistics/"
  query = "?league=" + ELO + "#?sortBy=general.playPercent&order=descend"
  url = statbase + query

  #Get r
  response = urllib2.urlopen(url)
  html = response.read()

  match = re.search(r'matchupData.stats = ([^\n]*\])', html.decode("utf-8"))

  stats = json.loads(match.group(1))

  champions = []
  for item in stats:
    champion = item["key"]
    role = item["role"]
    banRate = item["general"]["banRate"]
    pickRate = item["general"]["playPercent"]
    winRate = item["general"]["winPercent"]

    #calculate threat level
    truePickRate = pickRate/(1.0-banRate)
    threat = truePickRate * (winRate - 0.5) + 0.5

    champwithrole = champion + "(" + role + ")"

    elem = [champwithrole, winRate, banRate, pickRate, truePickRate, threat];

    champions.append(elem)

  champions.sort(key=threatgetter)

  printStats(champions)

if __name__ == "__main__":
  main()
