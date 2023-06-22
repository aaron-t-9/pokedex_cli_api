
class PokedexObject:
    """
    Base class that is the superclass of the Pokemon, Ability, and Move subclasses.
    """

    def __init__(self, name, id):
        self.name = name
        self.id = id
