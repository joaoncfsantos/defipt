import requests


class TokensMetaData:
    url = "https://api-v3.balancer.fi/graphql"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    payload = {
        "query": "{tokenGetTokens(chains: [GNOSIS]) {address symbol decimals}}",
    }

    def setup_data(self):
        response = requests.post(self.url, headers=self.headers, json=self.payload)
        return response.json()["data"]["tokenGetTokens"]
