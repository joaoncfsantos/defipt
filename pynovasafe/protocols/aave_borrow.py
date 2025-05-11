import json
import requests
from web3 import Web3


class AaveBorrowPositionsData:
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

    def get_user_configuration(self) -> dict:
        return self.contract.functions.getUserConfiguration(self.wallet_address).call()

    def get_user_account_data(self) -> dict:
        return self.contract.functions.getUserAccountData(self.wallet_address).call()

    def is_being_used_as_collateral(self, id) -> bool:
        user_configuration = self.get_user_configuration()[0]
        user_configuration = user_configuration >> (2 * id)
        return (user_configuration & 0b10) != 0

    def get_supply_rate(self, data: dict) -> float:
        return data[self.supply_apy_position] / 1e27

    def get_variable_rate(self, data: dict) -> float:
        return data[self.variable_apy_position] / 1e27

    def get_stable_rate(self, data: dict) -> float:
        return data[self.stable_apy_position] / 1e27

    def get_user_positions(self) -> int:
        user_balances = []
        reserves = self.get_reserves_list()
        for i, reserve in enumerate(reserves):
            reserve_data = self.get_reserve_data(reserve)
            supply_apy = self.get_supply_rate(reserve_data)
            variable_apy = self.get_variable_rate(reserve_data)
            stable_apy = self.get_stable_rate(reserve_data)
            lp_contract = self.w3.eth.contract(
                address=reserve_data[8], abi=self.get_abi_lps()
            )
            balance = lp_contract.functions.balanceOf(self.wallet_address).call()

            s_contract = self.w3.eth.contract(
                address=reserve_data[9], abi=self.get_abi_lps()
            )
            v_contract = self.w3.eth.contract(
                address=reserve_data[10], abi=self.get_abi_lps()
            )
            balance_variable = v_contract.functions.balanceOf(
                self.wallet_address
            ).call()
            balance_stable = s_contract.functions.balanceOf(self.wallet_address).call()
            if not balance_stable:
                balance_stable = 0
            decimals = float(self.tokens_data.get(reserve, {}).get("decimals", 18))
            liq_t = self.get_user_account_data()[3] / 10000

            if balance and self.is_being_used_as_collateral(i):
                user_balances.append(
                    {
                        "type": "supply as collateral",
                        "token": reserve,
                        "balance": float(balance) / 10**decimals,
                        "supply_apy": supply_apy,
                    }
                )
            if balance_variable or balance_stable:
                user_balances.append(
                    {
                        "type": "borrow",
                        "token": reserve,
                        "balance": (float(balance_variable) + float(balance_stable))
                        / 10**decimals,
                        "user_interest_rate": stable_apy + variable_apy,
                        "user_liquidation_threshold": liq_t,
                    }
                )

        return user_balances
