import asyncio
import aiohttp
import sys


class APIHandler:
    """
    Encompasses the methods for making Asynchronous HTTP GET request(s) to the API, and returns the data.
    """

    def __init__(self, query_type: str, target_urls: list):
        self.query_type = query_type
        self.target_urls = target_urls

    @staticmethod
    def generate_api_urls(query_type: str, input_data: list):
        """
        Given the list of input data, the appropriate API URLs are generated and returned as a list
        :param query_type: a string, of the type of data to be queried
        :param input_data: a list, of the input data
        :return: a list, containing the API URLs
        """
        base_url = "https://pokeapi.co/api/v2/{0}/{1}"
        target_urls = []

        for data in input_data:
            target_urls.append(base_url.format(query_type, data))

        return target_urls

    @staticmethod
    async def process_single_request_task(api_url: str) -> dict:
        """
        Handles a single Async task and returns the response as a JSON.
        :param api_url: a string, of the URL of the API to get data from
        :return: a dictionary
        """
        async with aiohttp.ClientSession() as session:
            response_dict = await APIHandler.get_api_response(api_url, session)

            return response_dict

    @staticmethod
    async def get_api_response(api_url: str, session: aiohttp.ClientSession) -> dict:
        """
        An Async coroutine that performs a GET HTTP request to the API, converts the response to a JSON, and returns
        the JSON.
        :param api_url: a string, of the target URL to make the API request to
        :param session: an HTTP session
        :return: a dictionary
        """
        try:
            response = await session.request(method="GET", url=api_url)
            response_dict = await response.json()

            return response_dict

        except aiohttp.ContentTypeError:
            print("ERROR: No results found, check your spelling and query type (Pokémon/Ability/Move).")
            sys.exit(1)

    def handle_api_requests(self):
        """
        Handles the API get_pokedex_entry and responses by initiating the Asynchronous method call.
        :return: a dictionary, or a list of dictionaries
        """
        return asyncio.run(self.process_multiple_requests())

    async def process_multiple_requests(self) -> tuple:
        """
        Handles processing multiple HTTP GET request through Asynchronous coroutine calls.
        :return: a list, of dictionaries of the requestd data from the API
        """
        async with aiohttp.ClientSession() as session:
            async_coroutines = [self.get_api_response(url, session) for url in self.target_urls]
            responses = await asyncio.gather(*async_coroutines)

            return responses
