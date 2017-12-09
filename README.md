# EZ Ban - League of Legends Ranked Bans
This script fetches stats from champion.gg and tells you the (theoretical) best bans for each elo.
So far, the script has been tested on bash on ubuntu on windows.
It should work with python 3 but is tested with python 2.

# Usage
`python easyban.py [options] [elo]`

Note: anything enclosed in brackets[] is optional

## Options
`-v`<br />
  verbose : spits out extra information when printing results.<br />
    Specifically - winrate, banrate, pickrate, and true pickrate(ban adjusted).

No other options currently exist.

## Elo
Champion.gg currently supports `bronze`, `silver`, `gold`, `plat`, `platplus`.

Gold is the default elo since I am a scrub.
The default elo can be easily changed by modifying the ELO variable in the script to the elo you want.

For example:

```
ELO = "gold"` -> `ELO = "silver"
```
