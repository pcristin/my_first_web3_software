import asyncio
import logging
from config import PRIVATE_KEY, PROXY, TOKENS_PER_CHAIN
from cex.bitget_client import BitgetClient
from web3_module.client import Web3Client
from web3_module.defi.odos_client import OdosClient
from settings import WORKING_NETWORK

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('arbitrum_pipeline')

async def main():
    # Initialize clients
    bitget_client = BitgetClient()
    web3_client = Web3Client(account_name="arbitrum_wallet", network=WORKING_NETWORK, private_key=PRIVATE_KEY, proxy=PROXY)
    odos_client = OdosClient(client=web3_client)
    
    # Step 1: Get wallet address from private key
    wallet_address = web3_client.address
    logger.info(f"Using wallet address: {wallet_address}")
    
    # Step 2: Withdraw USDC from Bitget to our wallet
    usdc_amount = "11"  # Adjust amount as needed
    logger.info(f"Withdrawing {usdc_amount} USDC from Bitget to {wallet_address}")
    withdrawal_result = await bitget_client.withdraw(
        coin="USDC", 
        chain=WORKING_NETWORK.bitget_chain.upper(), 
        amount=usdc_amount, 
        to_address=wallet_address
    )
    logger.info(f"Withdrawal result: {withdrawal_result}")
    
    # Wait for transaction to be confirmed (adjust time as needed)
    logger.info("Waiting for funds to arrive in wallet...")
    await asyncio.sleep(60)  # Wait 1 minute for funds to arrive
    
    # Step 3: Check USDC balance in wallet
    usdc_token_address = TOKENS_PER_CHAIN[WORKING_NETWORK.name]["USDC"]
    usdc_balance = await web3_client.get_erc20_balance(token_address=usdc_token_address)
    usdc_decimals = await web3_client.get_decimals(token_address=usdc_token_address)
    usdc_balance_formatted = web3_client.from_wei(usdc_balance, usdc_decimals)
    logger.info(f"USDC balance in wallet: {usdc_balance_formatted}")
    
    # Step 4: Swap USDC for ETH on ODOS
    eth_token_address = TOKENS_PER_CHAIN[WORKING_NETWORK.name]["ETH"]
    logger.info(f"Swapping USDC for ETH on ODOS")
    
    # We'll swap all our USDC balance
    swap_result = await odos_client.swap(
        input_token=usdc_token_address,
        input_token_name="USDC",
        output_token=eth_token_address,
        output_token_name="ETH",
        input_amount=usdc_balance_formatted,
        slippage="0.5"  # 0.5% slippage
    )
    logger.info(f"Swap completed: {swap_result}")
    
    # Get ETH balance after swap
    eth_balance = await web3_client.get_native_balance()
    logger.info(f"ETH balance after swap: {eth_balance}")
    
    # Step 5: Get deposit address for ETH on Bitget
    deposit_address_info = await bitget_client.get_deposit_address(coin="ETH", chain=WORKING_NETWORK.bitget_chain.upper())
    deposit_address = deposit_address_info.get('data', {}).get('address')
    logger.info(f"Bitget ETH deposit address: {deposit_address}")
    
    # Step 6: Send ETH back to Bitget (keeping some for gas)
    # Keep 0.001 ETH for future gas fees
    eth_to_send = float(eth_balance) - 0.001
    if eth_to_send <= 0:
        logger.error("Not enough ETH to transfer back to Bitget")
        return
    
    logger.info(f"Sending {eth_to_send} ETH back to Bitget")
    
    # Prepare and send transaction
    tx_params = await web3_client.prepare_transaction(value=web3_client.to_wei(eth_to_send))
    tx_params["to"] = deposit_address
    
    send_result = await web3_client.send_transaction(tx_params)
    logger.info(f"ETH deposit transaction result: {send_result}")
    
    logger.info("Pipeline completed successfully!")

if __name__ == '__main__':
    asyncio.run(main())