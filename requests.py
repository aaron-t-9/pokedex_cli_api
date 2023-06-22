
class Requests:
    """
    Stores the user's arguments in a Requests object.
    """

    def __init__(self, query_type: str, input_file, input_data, expanded: bool, output):
        self.query_type = query_type
        self.input_file = input_file
        self.input_data = input_data
        self.expanded = expanded
        self.output = output
