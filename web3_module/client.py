from config import Network
import random
from web3 import AsyncWeb3, AsyncHTTPProvider
import aiohttp
from config import TOKENS_PER_CHAIN, ERC20_ABI
from web3.contract import Contract
from settings import UNLIMITED_APPROVE, GAS_PRICE_MULTIPLIER
import asyncio
from web3.types import TxParams, HexStr
from web3.exceptions import TransactionNotFound


from config.interfaces import BlockchainException

class Web3Client:
    def __init__(self, account_name: str, network: Network, private_key: str, proxy: str = None):
        
        self.network = network
        self.eip1559_support = network.eip1559_support
        self.token = network.token
        self.explorer = network.explorer
        self.chain_id = network.chain_id
        self.bitget_chain = network.bitget_chain
        
        self.proxy = proxy
        self.request_kwargs = {"proxy": f"http://{proxy}", "ssl": False} if proxy else {"ssl": False}

        self.account_name = account_name
        self.rpc = random.choice(network.rpcs)
        self.w3 = AsyncWeb3(AsyncHTTPProvider(self.rpc, request_kwargs=self.request_kwargs))
        self.private_key = private_key
        self.address = AsyncWeb3.to_checksum_address(self.w3.eth.account.from_key(private_key).address)
        self.user_agent: str = self.get_user_agent()


    @staticmethod
    def get_user_agent() -> str:
        random_version = f"{random.uniform(520, 540):.2f}"
        return (
		    f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random_version} (KHTML, like Gecko)'
            f' Chrome/126.0.0.0 Safari/{random_version} Edg/126.0.0.0'
        )

    async def make_request(self, method: str = "GET", url: str = None, headers: dict = None, json: dict = None, params: dict = None) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.request(method = method, url = url, headers = headers, json = json, params = params) as response:
                if response.status in [200, 201]:
                    if response.headers.get("Content-Type") == "text/plain":
                        text = await response.text()
                        data = json.loads(text)
                    elif response.headers.get("Content-Type") == "application/json":
                        data = await response.json()
                    else:
                        raise Exception(f"Unexpected content type: {response.headers.get('Content-Type')}")
                else:
                    raise Exception(f"Request failed with status code {response.status}")
                return data
    
    async def get_decimals(self, token_name: str = None, token_address: str = None) -> int:
        contract_address = token_address if token_address else TOKENS_PER_CHAIN[self.network.name][token_name]
        contract = self.get_contract(contract_address)
        return await contract.functions.decimals().call()

    def get_contract(self, contract_address: str, abi: dict = ERC20_ABI) -> Contract:
        return self.w3.eth.contract(address = AsyncWeb3.to_checksum_address(contract_address), abi = abi)
    
    async def get_erc20_balance(self, token_name: str = None, token_address: str = None) -> int:
        contract_address = token_address if token_address else TOKENS_PER_CHAIN[self.network.name][token_name]
        contract = self.get_contract(contract_address)
        return await contract.functions.balanceOf(self.address).call()
    
    async def get_token_name(self, token_address: str = None) -> str:
        contract = self.get_contract(token_address)
        return await contract.functions.symbol().call()
    
    async def get_allowance(self, token_address: str = None, spender_address: str = None) -> int:
        contract = self.get_contract(token_address)
        return await contract.functions.allowance(self.address, spender_address).call()
    
    def to_wei(self, number: int | float | str, decimals: int = 18) -> int:
        unit_name = {
            18: "ether",
            6: "mwei"
        }[decimals]
        
        return self.w3.to_wei(number=int(number), unit=unit_name)
    
    def from_wei(self, number: int | float | str, decimals: int = 18) -> int:
        unit_name = {
            18: "ether",
            6: "mwei"
        }[decimals]
        return self.w3.from_wei(number=number, unit=unit_name)
    
    async def check_for_approved(self, token_address: str = None, spender_address: str = None,
                                 amount_in_wei: int = None, unlimited_approve: bool = UNLIMITED_APPROVE) -> bool:
        try:
            contract = self.get_contract(token_address)
            symbol = await self.get_token_name(token_address)

            print(f"Check for approval of {symbol}")

            approved_amount_in_wei = await self.get_allowance(token_address, spender_address)
            if approved_amount_in_wei >= amount_in_wei:
                print(f"Already approved {symbol} for {spender_address}")
                return False
            
            result = await self.make_approve()

            await asyncio.sleep(random.randint(4, 10))

            return result
        except Exception as e:
            raise BlockchainException(f"{e}")

    async def make_approve(self, token_address: str, spender_address: str, amount_in_wei: int, unlimited_approve: bool) -> bool:
        transction = await self.get_contract(token_address).functions.approve(spender_address, amount=2**256-1 if unlimited_approve else amount_in_wei).build_transaction(
            await self.prepare_transaction()
        )
        return await self.send_transaction(transction)
    
    async def prepare_transaction(self, value: int = 0) -> dict: 
        try:
            tx_params = TxParams(
                chainId = self.chain_id,
                nonce = await self.w3.eth.get_transaction_count(self.address),
                value = value,
            )

            if self.eip1559_support:

                base_fee = await self.w3.eth.gas_price
                max_priority_fee_per_gas = await self.get_priority_fee()
                max_fee_per_gas = int(base_fee + max_priority_fee_per_gas * 1.05 * GAS_PRICE_MULTIPLIER)

                if max_priority_fee_per_gas > max_fee_per_gas:
                    max_priority_fee_per_gas = int(max_fee_per_gas * 0.95)
                
                tx_params["maxFeePerGas"] = max_fee_per_gas
                tx_params["maxPriorityFeePerGas"] = max_priority_fee_per_gas
                tx_params["type"] = 2
            else:
                gas_price = await self.w3.eth.gas_price
                tx_params["gasPrice"] = int(gas_price * 1.2 * GAS_PRICE_MULTIPLIER)
                tx_params["type"] = 1
            
            return tx_params
        except Exception as e:
            raise BlockchainException(f"{e}")


    async def get_priority_fee(self) -> int:
        fee_history = await self.w3.eth.fee_history(block_count = 5, newest_block = 'latest', reward_percentiles = [20.0])
        non_empty_block_priority_fees = [fee[0] for fee in fee_history['reward'] if fee[0] != 0]

        divisor_priority = max(len(non_empty_block_priority_fees), 1)

        priority_fee = int(round(sum(non_empty_block_priority_fees) / divisor_priority, 0))
        return priority_fee
    
    async def send_transaction(self, transaction: dict = None, poll_latency: int = 10, timeout: int = 360, signed_tx: dict = None) -> bool | HexStr:
        try:
            signed_tx = self.w3.eth.account.sign_transaction(transaction, self.private_key).raw_transaction
            tx_hash = await self.w3.eth.send_raw_transaction(signed_tx)
        
        except Exception as e:
            raise BlockchainException(f"{e}")

        total_time = 0
        while True:
            try:
                receipts = await self.w3.eth.get_transaction_receipt(tx_hash)
                status = receipts.get('status')
                if status == 1:
                    message = f"Transaction successful: {self.explorer}/tx/{tx_hash}"
                    print(message)
                    return True
                elif status is None:
                    await asyncio.sleep(poll_latency)
                else:
                    raise BlockchainException(f"Transaction failed: {self.explorer}/tx/{tx_hash}")
            except TransactionNotFound:
                if total_time > timeout:
                    raise BlockchainException(f"Transaction failed: {self.explorer}/tx/{tx_hash}")
                total_time += poll_latency
                await asyncio.sleep(poll_latency)
            except Exception as e:
                if "Transaction failed" in str(e):
                    raise BlockchainException(f"Transaction failed: {self.explorer}/tx/{tx_hash}")
                print(f"Something went wrong. Error: {e}")
                total_time += poll_latency
                await asyncio.sleep(poll_latency)
        
    async def get_native_balance(self,) -> float:
        wei_balance = await self.w3.eth.get_balance(self.address)
        return self.from_wei(wei_balance)
