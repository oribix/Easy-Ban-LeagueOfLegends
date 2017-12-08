import sys
import json
import re
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
  return{
    "v" : setVerbose
  }[f]

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
      global ELO
      ELO = arg

  #set short flags
  for arg in shortargs:
    for flag in arg:
      setFlag(flag)()

  #set long flags
  for arg in longargs:
    print( arg)

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
  args = sys.argv
  args.pop(0)
  parseArgs(args)

  statbase = "http://champion.gg/statistics/"
  query = "?league=" + ELO + "#?sortBy=general.playPercent&order=descend"
  url = statbase + query

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
