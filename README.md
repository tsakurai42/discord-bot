# discord-bot

##Current Features

1. Party gold tracking
   - partyadd/partyspend to split evenly
    - playeradd/playerspend for single person
    - igot/ispent for self (currently hard coded for discord user id)
    - total to view totals
    - lookup and lookupdate to search notes or dates and return table
2. Dice rolling
   - \#d# to roll dice
   - stats to roll 4d6k3
3. Random gifs and videos triggered by certain words or phrases, because why not.

##Future additions

1. Move from csv storage to something better? Not needed really for just a personal project but it just feels better.
2. Capability to track gold for multiple parties - would require a total rehaul of data formatting, since currently character names are dataframe columns and several things are hard coded for 5 columns since my party has 5 players.
3. TBD as feature requests come up