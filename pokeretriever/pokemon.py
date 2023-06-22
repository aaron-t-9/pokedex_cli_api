from pokeretriever import pokedex_object


class Pokemon(pokedex_object.PokedexObject):
    """
    Represent a Pokémon. Stores the information of the Pokémon it's representing.
    """

    def __init__(self, name: str, pkm_id: str, height: str, weight: str, stats: list, types: list, abilities: list,
                 moves: list):
        """
        Initializer method
        :param name: a string, the Pokémon name
        :param pkm_id: an int, the ID of the Pokémon
        :param height: an int, the height of the Pokémon
        :param weight: an int, the weight of the Pokemon
        :param stats: a list, containing the name of the stat and it's base value
        :param types: a list of strings, of the Pokémon types
        :param abilities: a list, containing the abilities of the Pokémon and their URLs
        :param moves: a list, containing details of the Pokémon moves
        """
        super().__init__(name, pkm_id)
        self.height = height
        self.weight = weight
        self.stats = stats
        self.types = types
        self.abilities = abilities
        self.moves = moves

    def __str__(self):
        """
        Overridden string method.
        """
        return f"\n==================== Pokemon: {self.name.title()} ====================\n" \
               f"Height: {int(self.height) / 10} meters\n" \
               f"Weight: {int(self.weight) / 10} kg\n\n" \
               f"----- Stats -----\n{self.get_stats()}\n" \
               f"----- Type(s) ----- {self.get_types()}\n" \
               f"\n----- Abilities ----- {self.get_abilities()}\n" \
               f"----- Moves ----- {self.get_moves()}" \
               f"{'='*100}\n\n"

    def get_stats(self) -> str:
        """
        Gets the stats of the Pokémon to be printed.
        :return: a string
        """
        stats = ""
        for stat in self.stats:
            stats += f"{stat['name'].title()} - Base Value: {stat['base_stat']}\n"

        return stats

    def get_types(self) -> str:
        """
        Gets the types of the Pokémon to be printed.
        :return: a string
        """
        types = "\n"
        for pkm_type in self.types:
            types += f"{pkm_type.title()} "

        return types

    def get_abilities(self) -> str:
        """
        Gets the abilities of the Pokémon to be printed.
        :return: a string
        """
        abilities = "\n"
        for ability in self.abilities:
            try:
                abilities += f"{ability['expanded']}\n"
            except KeyError:
                abilities += f"{ability['name'].title()} -> Additional Info: {ability['url']}\n"

        return abilities

    def get_moves(self) -> str:
        """
        Gets the moves of the Pokémon to be printed.
        :return: a string
        """
        moves = "\n"
        for move in self.moves:
            try:
                moves += f"{move['expanded']}\n"
            except KeyError:
                moves += f"{move['name'].title()} -> Additional Info: {move['url']}\n"

        return moves
