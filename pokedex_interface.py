import file_handler
from pokeretriever import pokemon, ability, move, api_handler

import asyncio
import requests


class PokedexInterface:
    """
    The facade class that abstracts the complexity of classes and methods within the pokeretriever package that the user
    does not need to see. Contains the methods required for handling user requests, and create & returning the
    specified Pokédex objects.
    """

    @staticmethod
    def get_raw_pokedex_info(query_type: str, input_data: list) -> list:
        """
        Returns the raw JSON data from the API URL(s).
        :param query_type: a string, of the type of data to be queried
        :param input_data: a list, of the input data
        :return: a list of dictionaries, containing the raw JSON data
        """
        target_urls = api_handler.APIHandler.generate_api_urls(query_type, input_data)

        api_handler_obj = api_handler.APIHandler(query_type, target_urls)
        data_json = api_handler_obj.handle_api_requests()

        return data_json

    def execute_request(self, request: requests.Requests) -> list:
        """
        Executes the user specified request, and creates, and returns, the appropriate Pokédex object. Handles calling
        helper methods to get API responses and to transform the raw JSON data into the appropriate Pokédex objects.
        :param request: a Requests object
        :return: a list, containing PokédexObject(s)
        """
        if request.input_file:
            request.input_data = file_handler.FileHandler.open_file(request.input_file)
        else:
            request.input_data = [request.input_data]

        cleaned_input_data = self.clean_input_data(request.input_data)
        raw_json_data = self.get_raw_pokedex_info(request.query_type, cleaned_input_data)

        if request.query_type == "pokemon":
            pokedex_objects = self.create_pokemon(raw_json_data, request.expanded)
        elif request.query_type == "ability":
            pokedex_objects = self.create_ability(raw_json_data)
        else:
            pokedex_objects = self.create_move(raw_json_data)

        return pokedex_objects

    def clean_input_data(self, input_data: list) -> list:
        """
        Cleans the user's input data by replacing spaces or underscores with hyphens and ensures there are no capital
        letters.
        :return: a list, of the user's cleaned input
        """
        cleaned_input_data = []
        for data in input_data:
            cleaned_input_data.append(data.replace(" ", "-").replace("_", "-").lower())

        return cleaned_input_data

    def create_pokemon(self, data: list, expanded: bool) -> pokemon:
        """
        Creates a Pokémon, or list of Pokémon, objects given the attributes of a Pokémon.
        :param data: a list, containing the dictionary of Pokémon attributes
        :param expanded: a boolean, indicating whether or not to include additional information
        :return: a list, of Pokémon objects
        """
        if type(data) is not list:
            data: list = [data]

        pokemon_list = []
        for pokemon_data in data:
            name = pokemon_data["name"]
            pkm_id = pokemon_data["id"]
            height = pokemon_data["height"]
            weight = pokemon_data["weight"]

            stats = self.get_pokemon_stats(pokemon_data["stats"], expanded)
            types = self.get_pokemon_types(pokemon_data["types"])
            abilities = self.get_pokemon_abilities(pokemon_data["abilities"], expanded)
            moves = self.get_pokemon_moves(pokemon_data["moves"], expanded)

            pokemon_list.append(pokemon.Pokemon(name, pkm_id, height, weight, stats, types, abilities, moves))

        return pokemon_list

    def create_ability(self, data: list) -> ability:
        """
        Creates a Ability object, that contains the information of the specified Ability.
        :param data: a list, containing the dictionary of Ability attributes
        :return: a list, of Ability objects
        """
        abilities = []
        if type(data) is not list:
            data: list = [data]

        for ability_data in data:
            name = ability_data["name"]
            ability_id = ability_data["id"]
            generation = ability_data["generation"]["name"]

            for effect_desc in ability_data["effect_entries"]:
                if effect_desc["language"]["name"] == "en":
                    effect = effect_desc["effect"]
                    break

            for effect_desc in ability_data["flavor_text_entries"]:
                if effect_desc["language"]["name"] == "en":
                    effect_short = effect_desc["flavor_text"].replace("\n", " ")
                    break

            pkm_list = []
            for pkm in ability_data["pokemon"]:
                pkm_list.append(pkm["pokemon"]["name"])

            abilities.append(ability.Ability(name, ability_id, generation, effect, effect_short, pkm_list))

        return abilities

    def create_move(self, data: list) -> move:
        """
        Creates a Move object, that contains the information of the specified Move.
        :param data: a list, containing the dictionary of Move attributes
        :return: a list, of Moves
        """
        moves = []
        if type(data) is not list:
            data: list = [data]

        for move_data in data:
            name = move_data["name"]
            move_id = move_data["id"]
            generation = move_data["generation"]["name"]
            accuracy = move_data["accuracy"]
            pp = move_data["pp"]
            power = move_data["power"]
            move_type = move_data["type"]["name"]
            damage_class = move_data["damage_class"]["name"]

            for flavor_text in move_data["flavor_text_entries"]:
                if flavor_text["language"]["name"] == "en":
                    effect_short = flavor_text["flavor_text"].replace("\n", " ")
                    break

            moves.append(move.Move(name, move_id, generation, accuracy, pp, power, move_type, damage_class,
                                   effect_short))

        return moves

    def get_pokemon_types(self, pokemon_type_data: list) -> list:
        """
        Extracts the specified type attributes for the Pokémon and returns a list of the information.
        :param pokemon_type_data: a list, of the unprocessed information of the Pokémon's type
        :return: a list, containing the Pokémon's type information
        """
        types = []
        for pkm_type in pokemon_type_data:
            types.append(pkm_type["type"]["name"])
        return types

    def get_pokemon_stats(self, pokemon_stats_data: list, expanded: bool) -> list:
        """
        Extracts the specified stat attributes for the Pokémon and returns a list of the information.
        :param pokemon_stats_data: a list, of the unprocessed information of the Pokémon's stats
        :param expanded: a boolean, if expanded information has been requested
        :return: a list, containing the Pokémon's stat information
        """
        stats = []
        for stat in pokemon_stats_data:
            temp_dict = {"name": stat["stat"]["name"], "base_stat": stat["base_stat"], "url": stat["stat"]["url"]}

            if expanded:
                expanded_url = temp_dict["url"]
                expanded_data = asyncio.run(api_handler.APIHandler.process_single_request_task(expanded_url))
                expanded_temp_dict = {"name": expanded_data["name"], "id": expanded_data["id"],
                                      "is_battle_only": expanded_data["is_battle_only"]}
                temp_dict.update({"expanded": expanded_temp_dict})

            stats.append(temp_dict)
        return stats

    def get_pokemon_abilities(self, pokemon_abilities_data: list, expanded: bool) -> list:
        """
        Extracts the specified ability attributes for the Pokémon and returns a list of the information.
        :param pokemon_abilities_data: a list, containing the unprocessed information of the Pokémon's abilities
        :param expanded: a boolean, if expanded information has been requested
        :return: a list, containing the Pokémon abilities
        """
        abilities = []
        for ability in pokemon_abilities_data:
            temp_dict = {"name": ability["ability"]["name"], "url": ability["ability"]["url"]}

            if expanded:
                expanded_url = temp_dict["url"]
                expanded_data = asyncio.run(api_handler.APIHandler.process_single_request_task(expanded_url))
                expanded_ability = self.create_ability(expanded_data)[0]
                temp_dict.update({"expanded": expanded_ability})

            abilities.append(temp_dict)
        return abilities

    def get_pokemon_moves(self, pokemon_move_data: list, expanded: bool) -> list:
        """
        Gets the moves that the specified Pokémon can learn through asynchronous HTTP Get get_pokedex_entry, extracts
        key move attributes and returns a list of these attributes for each move that the Pokémon can learn.
        :param pokemon_move_data: a list, containing the unprocessed information about the moves of a Pokémon
        :param expanded: a boolean, if expanded information has been requested
        :return: a list, containing the Pokémon moves
        """
        expanded_move_urls = []
        moves = []
        for move in pokemon_move_data:
            temp_dict = {"name": move["move"]["name"],
                         "level_learned_at": move["version_group_details"][0]["level_learned_at"],
                         "url": move["move"]["url"]}

            if expanded:
                expanded_move_urls.append(temp_dict["url"])

            moves.append(temp_dict)

        api_handler_obj = api_handler.APIHandler("move", expanded_move_urls)
        data_json = api_handler_obj.handle_api_requests()

        if expanded:
            for index in range(0, len(moves)):
                moves[index].update({"expanded": self.create_move(data_json[index])[0]})

        return moves
