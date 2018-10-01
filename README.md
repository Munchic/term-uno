# UNO Game on Python

### Rules
1. Each player gets 7 random cards
2. Cards contain two parameters: value and color
3. They can be number (0-10) or action cards (add 4, add 2, ...)
4. A card can be placed if it matches the top card in at least one of the parameters, it then becomes the top card
5. Game starts with a top card taken from the main deck
6. Certain action cards (add 4, add 2, skip) ban the next player from his/her turn
7. Reverse card changes the turn order

### Running
```
$ cd KP
$ python3 uno.py
# Follow in-game instructions
```

### Rationale
1. Data structure for deck and hands: linked list. This allows us to pop out any list element in O(1).
2. Alternatively, deck could be made into a queue since we are only taking elements out from the top and he handsc could be made into sets, because the time to remove an element at any point with O(1).
3. Class Uno() is used to store game conditions, such as whose turn, rotation direction, and what action is being casted on whom, as well as players and their cards.