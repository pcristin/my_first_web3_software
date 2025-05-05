from web3_module.client import Web3Client
import aiohttp
from config import TOKENS_PER_CHAIN, ZERO_ADDRESS
from config import BlockchainException

class OdosClient:
    def __init__(self, client: Web3Client):
        self.client = client
        self.base_url = "https://api.odos.xyz/sor"
        self.token = self.client.network.token

    async def get_quote(self, input_token: str, output_token: str, input_amount: int, slippage: str = "0.5") -> dict:
        quote_url = f"{self.base_url}/quote/v2"
        quote_request_body = {
            "chainId": self.client.network.chain_id,
            "inputTokens": [
                {
                    "tokenAddress": input_token,
                    "amount": input_amount
                }
            ],
            "outputTokens": [
                {
                    "proportion": 1,
                    "tokenAddress": output_token
                }
            ],
            "slippageLimitPercent": slippage,
            "userAddr": self.client.address,
        }

        headers = {
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(quote_url, json=quote_request_body, headers=headers) as response:
                response_json = await response.json()
                return response_json["pathId"]


    async def assemble(self, path_id: str) -> dict:
        assemble_url = f"{self.base_url}/assemble"
        assemble_request_body = {
            "pathId": path_id,
            "userAddr": self.client.address,
        }
        return await self.client.make_request(method="POST", url=assemble_url, json=assemble_request_body)

    async def swap(self, input_token: str, input_token_name: str, output_token: str, output_token_name: str, input_amount: int, slippage: str = "0.5") -> dict:
        native_token = TOKENS_PER_CHAIN[self.client.network.name][self.client.network.token]

        decimals_input_token = self.client.get_decimals(token_address=input_token)
        input_amount_wei = self.client.to_wei(number=input_amount, decimals=decimals_input_token)

        if input_token == native_token:
            input_token = ZERO_ADDRESS
        if output_token == native_token:
            output_token = ZERO_ADDRESS

        path_id = await self.get_quote(input_token=input_token, output_token=output_token, input_amount=input_amount_wei, slippage=slippage)
        odos_tx = await self.assemble(path_id=path_id)

        output_value_wei = odos_tx["outputTokens"][0]["amount"]
        decimals_output_token = self.client.get_decimals(token_address=output_token)
        out_amount_ether = self.client.from_wei(number=output_value_wei, decimals=decimals_output_token)

        print(f"Starting swap on ODOS: {input_amount:.6f} {input_token_name} -> {out_amount_ether:.6f} {output_token_name}")

        value = int(odos_tx["transaction"]["value"])
        spender_odos_contract = odos_tx["transaction"]["to"]
        call_data = odos_tx["transaction"]["data"]

        if input_token != ZERO_ADDRESS:
            await self.client.check_for_approved(token_address=input_token, spender_address=spender_odos_contract, amount_in_wei=input_amount_wei)
        
        try:
            tx_params = (await self.client.prepare_transaction(value=value)) | {
                         'to': spender_odos_contract,
                         'data': call_data,
                         'value': value,
            }
            
            return await self.client.send_transaction(tx_params=tx_params)
        except Exception as e:
            if "transfer amount exceeds balance" in str(e):
                raise RuntimeError(f"Insufficient balance of {input_token_name} for swap on ODOS")
            else: 
                raise e

        return odos_tx


        
        