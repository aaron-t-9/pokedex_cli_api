import argparse
import file_handler
import pokedex_interface
import requests


class QueryHandler:
    """
    Encompasses the methods to read the arguments passed into the program, and handles querying and outputting the
    information.
    """

    def __init__(self):
        """
        Initializer method.
        """
        self.pokedex_interface = pokedex_interface.PokedexInterface()

    def handle_query(self, args: argparse.Namespace):
        """
        Handles query by routing the query to the appropriate class (Pokémon, Ability, or Move), whether or not expanded
        information should be provided, and the mode that the information should be reported in.
        """
        query_type = args.query.lower()
        input_file = args.inputfile
        input_data = args.inputdata
        expanded = args.expanded
        output = args.output

        if input_file is None and input_data is None:
            print("ERROR: Missing argument after --inputdata or --inputfile")
            return

        request = requests.Requests(query_type, input_file, input_data, expanded, output)
        pokedex_objects = self.pokedex_interface.execute_request(request)

        if output:
            file_handler.FileHandler.write_file(output, pokedex_objects)
        else:
            for entry in pokedex_objects:
                print(entry)


def parse_args() -> argparse.Namespace:
    """
    Handles parsing the arguments that are specified when running this program. Returns the Namespace object
    of the argparse move_type that contains the argument specified when running this program.
    :return: argparse.Namespace object
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("query", help="Provides info about specified topic", choices=("pokemon", "ability", "move"))

    input_type_group = parser.add_mutually_exclusive_group()
    input_type_group.add_argument("--inputfile", help="Specify text file to read", nargs="?")
    input_type_group.add_argument("--inputdata", help="Name/ID of Pokemon/Ability/Move", nargs="?")

    parser.add_argument("--expanded", help="Provides additional information about the queried attribute.",
                        action="store_true")
    parser.add_argument("--output", help="Outputs the results to a text file of the specified file name.")

    return parser.parse_args()


def main():
    """
    Main method responsible for calling lower level methods to run the program.
    """
    args = parse_args()
    query_handler = QueryHandler()
    query_handler.handle_query(args)


if __name__ == '__main__':
    main()
