## Durak (a russian card game) 

### Introduction

This is a learning project I made during Nucamp coding bootcamp course "Python Fundamentals"

### Description of the game

This version is a single-player game: a player vs the computer. The objective of the game is to get rid of all one's cards when there are no more cards left in the deck before the opponent does.  
The game uses a deck of 36 cards, shuffled, each player receives 6 cards, the last card determines the trump suit.  
A trump card of any rank beats all cards in the other three suits.
The player who has the lowest trump card will be the first attacker.

A round:

The attacker opens their turn by playing a card from their hand as an attacking card.  
The defender attempts to beat the attacking card by playing a higher-ranking defending card of the same suit as the attacking card or a card of the trump suit from their hand.  
If the defender is successful, the attacker may start a new attack by playing a card of the same rank as any card that had been played in this round. Max number of attacks is 6 in one round.  
If the defender has beaten all attacking cards, the cards from this round are placed in the discard pile. And in the next round it will be the defender's turn to attack.  
If the defender has given up, they must take in all the cards played during this round and skip their turn to attack.  
If players after a round have less than 6 cards, they draw new cards from the remaining deck (the attacker draws first) until they have 6 cards each, or the deck has been exhausted.

Rounds get repeated until the deck is exhausted and one of the players has played all their cards, they are considered the winner. The other player who still has cards in their hand is the loser.

The current version of the game doesn’t include any strategy for the computer player, it just chooses cards randomly and is easy to defeat.

