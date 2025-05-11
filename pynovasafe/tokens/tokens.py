from tokens.tokens_metadata import TokensMetaData
from tokens.tokens_prices import TokensPricesData


class Tokens:
    def get_tokens_data(self):

        tokens_metadata = TokensMetaData()
        tokens_prices = TokensPricesData()

        metadata = tokens_metadata.setup_data()
        prices = tokens_prices.setup_data()

        results = {}
        for token in metadata:
            price = next(
                (
                    price["price"]
                    for price in prices
                    if price["address"] == token["address"]
                ),
                None,
            )
            if not price:
                continue
            results[token["address"]] = {
                "symbol": token["symbol"],
                "price": price,
                "decimals": token["decimals"],
            }
        return results
