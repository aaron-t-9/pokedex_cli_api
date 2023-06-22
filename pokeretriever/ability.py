from pokeretriever import pokedex_object


class Ability(pokedex_object.PokedexObject):
    """
    Provided a Pokemon ability, this class stores the information of that ability
    and reports it.
    """

    def __init__(self, name: str, ability_id: str, generation: str, effect: str, effect_short: str, pokemon: list):
        """
        Initializer method.
        :param name: a string, the name of the ability
        :param ability_id: an int, the ID of the Pokémon ability
        :param generation: an string, the generation of game the Pokémon move is found in
        :param effect: a string, the effect of the ability
        :param effect_short: a string, a brief summary of the effect of the ability
        :param pokemon: a list of strings, containing the names of the Pokémon who can learn the move
        """
        super().__init__(name, ability_id)
        self.generation = generation
        self.effect = effect
        self.effect_short = effect_short
        self.pokemon = pokemon

    def __str__(self):
        """
        Overridden string method.
        """
        return f"{self.name.title()} - ID: {self.id}\n" \
               f"Generation: {self.generation[11:].upper()}\n" \
               f"Effect: {self.effect}\n" \
               f"Effect (short): {self.effect_short}\n" \
               f"Pokemon that can learn {self.name.lower()}: {self.unpack_pokemon()}\n"

    def unpack_pokemon(self) -> str:
        """
        Unpacks the Pokémon who can learn this ability.
        :return: a string
        """
        pokemon_string = ""
        for pokemon in self.pokemon:
            pokemon_string += f"{pokemon.title()}, "

        pokemon_string = pokemon_string[:-2]
        pokemon_string += "."
        return pokemon_string
