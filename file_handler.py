
class FileHandler:
    """
    Encompasses the methods for reading and writing files.
    """

    @staticmethod
    def open_file(file_name: str) -> list:
        """
        Handles the input file, and returns the data within the file as a list
        :param file_name: a string, of the file name
        :return: a list
        """
        input_data = []
        try:
            with open(file_name, mode="r", encoding="utf-8") as data:
                for line in data:
                    input_data.append(line.rstrip("\n").lower())

            return input_data

        except FileNotFoundError:
            print("File not found!")
            return

    @staticmethod
    def write_file(file_name: str, pokedex_data: list):
        """
        Writes the results from the user's query to the user's text file of the specified file name.
        :param file_name: a string, the file name
        :param pokedex_data: a list, containing the information of the user's query
        """
        with open(file_name, mode="w", encoding="utf-8") as data:
            for entry in pokedex_data:
                data.write(str(entry))
