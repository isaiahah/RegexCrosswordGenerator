# RegexCrosswordGenerator

This is some relatively simple code to generate 
a Regex Crossword when given the desired solution.

`ClueGeneatorOptionPairs` is the most basic method of 
generating puzzles. Each cell is specified by the
two options of letters in the row and 
column clues.

`ClueGeneratorSeries` incorporates a 
series of letters into each row clue. The column
clues are bland by comparison.

# Example

Hint: The Love Song of J. Alfred Prufrock

```
-------------------------------------------------------------------------------------------------------------------
|                      | [LX][35GJ]YD[8E] | [AEIOU].[FOR][INT][NO] | .+[,02D]+ | .[4AIMO][AC][WHY]+ | S[0EPQW]N.. |
-------------------------------------------------------------------------------------------------------------------
|   [ALMN](ET|UV)U.    |                  |                        |           |                    |             |
-------------------------------------------------------------------------------------------------------------------
| (GON|TY4)[6BNO][UWU] |                  |                        |           |                    |             |
-------------------------------------------------------------------------------------------------------------------
|    .(OU|8F)[AVX]+    |                  |                        |           |                    |             |
-------------------------------------------------------------------------------------------------------------------
|   .[IF][,K](WH|RX)   |                  |                        |           |                    |             |
-------------------------------------------------------------------------------------------------------------------
|   [LET](NTH|V8U)E    |                  |                        |           |                    |             |
-------------------------------------------------------------------------------------------------------------------
```

Solution: `LETUSGONOWYOUANDI,WHENTHE`