from ClueGenerator import ClueGeneratorSeries

# Hint: The Love Song of J. Alfred Prufrock
cg = ClueGeneratorSeries("LETUSGONOWYOUANDI,WHENTHE", (5, 5))
c = cg.generate_puzzle()
print(c)
