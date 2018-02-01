# EZ Ban - League of Legends Ranked Bans
This script fetches stats from champion.gg and tells you the (theoretical) best bans for each elo.

This script can be run with both python2 and python3

# Usage
`python easyban.py [options] [elo] [# of Results]`

You can combine or omit anything in brackets.

```
python -v silver 5
```

This command will show the top 5 best picks/bans for silver.
It will also show more verbose output due to the -v flag.

## Options
`-v`<br />
  verbose : spits out extra information when printing results.<br />
    Specifically - winrate, banrate, pickrate, and true pickrate(ban adjusted).

No other options currently exist.

## Elo
Champion.gg currently supports `bronze`, `silver`, `gold`, `plat`, `platplus`.

If Elo is not specified, Gold is used by default.

The default Elo can be changed.
Open up the easyban.py in a text editor such as notepad
and change `ELO = "gold"` to the Elo of your choice.


For example:

```
ELO = "gold"` -> `ELO = "silver"
```

## Increase/Decrease number of Results
You can additionally specify the number of results to show;
simply add the number at the end.

```
python easyban.py 5
```

This command will show you the top 5 best bans for the default Elo.
