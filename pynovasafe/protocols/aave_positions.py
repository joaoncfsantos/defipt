import json
import requests
from web3 import Web3


class AavePositionsData:
    contract_address = "0xb50201558B00496A145fE76f7424749556E326D8"
    supply_apy_position = 2
    variable_apy_position = 4
    stable_apy_position = 5
    w3 = Web3(Web3.HTTPProvider("https://rpc.gnosischain.com"))

    def __init__(self, wallet_address, tokens_data):
        self.tokens_data = tokens_data
        self.wallet_address = wallet_address
        self.contract = self.w3.eth.contract(
            address=self.contract_address, abi=self.get_abi()
        )

    def get_abi(self):
        with open("abis/aave_abi.json", "r") as f:
            return json.load(f)

    def get_abi_lps(self):
        with open("abis/aave_lps.json", "r") as f:
            return json.load(f)

    def get_reserves_list(self) -> list:
        return self.contract.functions.getReservesList().call()

    def get_reserve_data(self, asset: str) -> dict:
        return self.contract.functions.getReserveData(asset).call()

    def get_user_configuration(self, asset: str) -> dict:
        return self.contract.functions.getUserConfiguration(self.wallet_address).call()

    def is_being_used_as_collateral(self, wallet_address: str, id) -> bool:
        user_configuration = self.get_user_configuration(self.wallet_address)[0]
        user_configuration = user_configuration >> (2 * id)
        return (user_configuration & 0b10) != 0

    def get_user_positions(self) -> int:
        user_balances = []
        reserves = self.get_reserves_list()
        for i, reserve in enumerate(reserves):
            reserve_data = self.get_reserve_data(reserve)
            decimals = float(self.tokens_data.get(reserve, {}).get("decimals", 18))
            supply_apy = reserve_data[self.supply_apy_position] / 1e27
            lp_token = reserve_data[8]
            lp_contract = self.w3.eth.contract(address=lp_token, abi=self.get_abi_lps())
            balance = lp_contract.functions.balanceOf(self.wallet_address).call()
            if not balance:
                continue
            if self.is_being_used_as_collateral(self.wallet_address, i):
                continue
            user_balances.append(
                {
                    "token": reserve,
                    "balance": float(balance) / 10**decimals,
                    "supply_apy": supply_apy,
                }
            )
        return user_balances
