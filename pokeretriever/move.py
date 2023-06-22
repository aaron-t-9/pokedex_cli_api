from pokeretriever import pokedex_object


class Move(pokedex_object.PokedexObject):
    """
    Stores and provides the information of the specified Pokemon move.
    """

    def __init__(self, name: str, move_id: str, generation: str, accuracy: str, pp: str, power: str, move_type: str,
                 damage_class: str, effect_short: str):
        """
        Initializer method.
        :param name: a string, of the move name
        :param move_id: an int, of the ID of the move
        :param generation: a string, the generation of game the Pokemon move is found in
        :param accuracy: an int, the accuracy of the move
        :param pp: an int, the PP of the move
        :param power: an int, the power of the move
        :param move_type: a string, the type of the move
        :param damage_class: a string, the damage class of the move
        :param effect_short: a string, a brief summary of the effect of the move
        """
        super().__init__(name, move_id)
        self.generation = generation
        self.accuracy = accuracy
        self.pp = pp
        self.power = power
        self.move_type = move_type
        self.damage_class = damage_class
        self.effect_short = effect_short

    def __str__(self):
        """
        Overridden string method.
        """
        return f"{self.name.title().replace('-', ' ')} - ID: {self.id}\n" \
               f"Generation: {self.generation[11:].upper()}\n" \
               f"Accuracy: {self.accuracy}\n" \
               f"PP: {self.pp}\n" \
               f"Power: {self.power}\n" \
               f"Move Type: {self.move_type.title()}\n" \
               f"Damage Class: {self.damage_class.title()}\n" \
               f"Effect: {self.effect_short}\n"
