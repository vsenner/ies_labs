import json
import requests
from typing import List

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url: str):
        """Initialize the StoreApiAdapter with the base URL for the API."""
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]) -> bool:
        """
        Sends a batch of processed agent data to the store API.

        Args:
            processed_agent_data_batch: A list of ProcessedAgentData instances to be saved.

        Returns:
            True if the data is successfully saved, False otherwise.
        """

        # Convert processed data objects to dictionaries for JSON serialization.
        serialized_data = [item.dict() for item in processed_agent_data_batch]  # Using .dict() method if it's a Pydantic model, replace with the correct serialization if otherwise

        # Make a POST request to the store API.
        response = requests.post(
            url=f"{self.api_base_url}/processed_agent_data/",
            json=serialized_data  # Send the serialized data as JSON
        )

        # Check if the request was successful (status code 200 OK)
        return response.status_code == 200  # Using literal status code for clarity
