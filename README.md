# Python based Pokédex Interface

---

The purpose of this program is to simulate a Pokédex. By making calls to a public and free Pokémon API
(<a href="https:pokeapi.co/">https:pokeapi.co/</a>), the program is able to return comprehensive information on any 
Pokémon, or any Pokémon Ability or Move!

To run the program, simply download the repository and extract it. Navigate to the folder within your favourite terminal
of choice, and execute the program with the following command (make sure you have at least Python version 3.10 
installed):

python3 driver.py {pokemon | ability | move} {--inputfile "filename.txt" | --inputdata "name or ID"} {--expanded} 
{--output "filename.txt"} 

Where the first argument is specifying if you're querying for information on a Pokémon, Ability, or Move, the second 
argument specifies if the type of arguments, whether or not you want to query a single item, or a text file with 
multiple items. If the input is a file, then the file must be a text file with each item on a new line. Each item is 
either a specific name (e.g. Pikachu, tail-whip, intimidate) or ID (e.g. 151). If there is a space inbetween the item 
then use a hyphen ("-") in place of the blank space (e.g. ice beam should be ice-beam).

The "expanded" argument specifies whether or not additional information will be included with the query, and if an 
"output" is specified then a file name must be specified. The results would then be written to the specified text file. 
For naming the output text file, the name should end with ".txt".

Any deviation from the above instructions of parameters may result in the program crashing or not functioning as 
intended.
---
---

