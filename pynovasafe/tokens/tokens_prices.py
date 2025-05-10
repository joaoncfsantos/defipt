import requests


class TokensPricesData:
    url = "https://api-v3.balancer.fi/graphql"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    payload = {
        "query": "{tokenGetCurrentPrices(chains: [GNOSIS]) {address price}}",
    }

    def setup_data(self):
        response = requests.post(self.url, headers=self.headers, json=self.payload)
        return response.json()["data"]["tokenGetCurrentPrices"]
