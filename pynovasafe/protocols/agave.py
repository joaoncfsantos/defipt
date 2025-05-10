import json
import requests
from web3 import Web3


class AgaveData:
    contract_address = "0x5E15d5E33d318dCEd84Bfe3F4EACe07909bE6d9c"
    supply_apy_position = 2
    variable_apy_position = 4
    stable_apy_position = 5
    w3 = Web3(Web3.HTTPProvider("https://rpc.gnosischain.com"))

    def __init__(self):
        self.contract = self.w3.eth.contract(
            address=self.contract_address, abi=self.get_abi()
        )

    def get_abi(self):
        with open("abis/agave_abi.json", "r") as f:
            return json.load(f)

    def get_reserves_list(self) -> list:
        return self.contract.functions.getReservesList().call()

    def get_reserve_data(self, asset: str) -> dict:
        return self.contract.functions.getReserveData(asset).call()

    def get_supply_rate(self, data: dict) -> float:
        return data[self.supply_apy_position] / 1e27

    def get_variable_rate(self, data: dict) -> float:
        return data[self.variable_apy_position] / 1e27

    def get_stable_rate(self, data: dict) -> float:
        return data[self.stable_apy_position] / 1e27

    def setup_data(self):
        reserves = self.get_reserves_list()
        data = []
        for asset in reserves:
            reserve_data = self.get_reserve_data(asset)
            asset_data = {
                "token": asset,
                "supply_rate": self.get_supply_rate(reserve_data),
                "borrow_rate": self.get_variable_rate(reserve_data)
                + self.get_stable_rate(reserve_data),
            }
            data.append(asset_data)
        return data
