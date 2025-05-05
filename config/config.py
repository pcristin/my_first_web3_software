import os

from dotenv import load_dotenv

# Environment variables
load_dotenv()

# Bitget API
BITGET_API_BASE_URL = 'https://api.bitget.com'
BITGET_API_KEY = os.getenv("BITGET_API_KEY")
BITGET_API_SECRET = os.getenv("BITGET_API_SECRET")
BITGET_API_PASSPHRASE = os.getenv("BITGET_API_PASSPHRASE")

# Private key and proxy
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PROXY = os.getenv("PROXY")

# ABI
ERC20_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "_name", "type": "string"},
            {"internalType": "string", "name": "_symbol", "type": "string"},
            {"internalType": "uint256", "name": "_initialSupply", "type": "uint256"},
        ],
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "spender",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256",
            },
        ],
        "name": "Approval",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256",
            },
        ],
        "name": "Transfer",
        "type": "event",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "address", "name": "spender", "type": "address"},
        ],
        "name": "allowance",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "subtractedValue", "type": "uint256"},
        ],
        "name": "decreaseAllowance",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "addedValue", "type": "uint256"},
        ],
        "name": "increaseAllowance",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint8", "name": "decimals_", "type": "uint8"}],
        "name": "setupDecimals",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "recipient", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "sender", "type": "address"},
            {"internalType": "address", "name": "recipient", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "transferFrom",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]

ODOS_ROUTER_V2_ABI = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"sender","type":"address"},{"indexed":False,"internalType":"uint256","name":"inputAmount","type":"uint256"},{"indexed":False,"internalType":"address","name":"inputToken","type":"address"},{"indexed":False,"internalType":"uint256","name":"amountOut","type":"uint256"},{"indexed":False,"internalType":"address","name":"outputToken","type":"address"},{"indexed":False,"internalType":"int256","name":"slippage","type":"int256"},{"indexed":False,"internalType":"uint32","name":"referralCode","type":"uint32"}],"name":"Swap","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"sender","type":"address"},{"indexed":False,"internalType":"uint256[]","name":"amountsIn","type":"uint256[]"},{"indexed":False,"internalType":"address[]","name":"tokensIn","type":"address[]"},{"indexed":False,"internalType":"uint256[]","name":"amountsOut","type":"uint256[]"},{"indexed":False,"internalType":"address[]","name":"tokensOut","type":"address[]"},{"indexed":False,"internalType":"uint32","name":"referralCode","type":"uint32"}],"name":"SwapMulti","type":"event"},{"inputs":[],"name":"FEE_DENOM","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"REFERRAL_WITH_FEE_THRESHOLD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"addressList","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"","type":"uint32"}],"name":"referralLookup","outputs":[{"internalType":"uint64","name":"referralFee","type":"uint64"},{"internalType":"address","name":"beneficiary","type":"address"},{"internalType":"bool","name":"registered","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"_referralCode","type":"uint32"},{"internalType":"uint64","name":"_referralFee","type":"uint64"},{"internalType":"address","name":"_beneficiary","type":"address"}],"name":"registerReferralCode","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_swapMultiFee","type":"uint256"}],"name":"setSwapMultiFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"inputToken","type":"address"},{"internalType":"uint256","name":"inputAmount","type":"uint256"},{"internalType":"address","name":"inputReceiver","type":"address"},{"internalType":"address","name":"outputToken","type":"address"},{"internalType":"uint256","name":"outputQuote","type":"uint256"},{"internalType":"uint256","name":"outputMin","type":"uint256"},{"internalType":"address","name":"outputReceiver","type":"address"}],"internalType":"struct OdosRouterV2.swapTokenInfo","name":"tokenInfo","type":"tuple"},{"internalType":"bytes","name":"pathDefinition","type":"bytes"},{"internalType":"address","name":"executor","type":"address"},{"internalType":"uint32","name":"referralCode","type":"uint32"}],"name":"swap","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"swapCompact","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"}],"internalType":"struct OdosRouterV2.inputTokenInfo[]","name":"inputs","type":"tuple[]"},{"components":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"uint256","name":"relativeValue","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"}],"internalType":"struct OdosRouterV2.outputTokenInfo[]","name":"outputs","type":"tuple[]"},{"internalType":"uint256","name":"valueOutMin","type":"uint256"},{"internalType":"bytes","name":"pathDefinition","type":"bytes"},{"internalType":"address","name":"executor","type":"address"},{"internalType":"uint32","name":"referralCode","type":"uint32"}],"name":"swapMulti","outputs":[{"internalType":"uint256[]","name":"amountsOut","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"swapMultiCompact","outputs":[{"internalType":"uint256[]","name":"amountsOut","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"swapMultiFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"contractAddress","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bytes","name":"signature","type":"bytes"}],"internalType":"struct OdosRouterV2.permit2Info","name":"permit2","type":"tuple"},{"components":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"}],"internalType":"struct OdosRouterV2.inputTokenInfo[]","name":"inputs","type":"tuple[]"},{"components":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"uint256","name":"relativeValue","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"}],"internalType":"struct OdosRouterV2.outputTokenInfo[]","name":"outputs","type":"tuple[]"},{"internalType":"uint256","name":"valueOutMin","type":"uint256"},{"internalType":"bytes","name":"pathDefinition","type":"bytes"},{"internalType":"address","name":"executor","type":"address"},{"internalType":"uint32","name":"referralCode","type":"uint32"}],"name":"swapMultiPermit2","outputs":[{"internalType":"uint256[]","name":"amountsOut","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"contractAddress","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bytes","name":"signature","type":"bytes"}],"internalType":"struct OdosRouterV2.permit2Info","name":"permit2","type":"tuple"},{"components":[{"internalType":"address","name":"inputToken","type":"address"},{"internalType":"uint256","name":"inputAmount","type":"uint256"},{"internalType":"address","name":"inputReceiver","type":"address"},{"internalType":"address","name":"outputToken","type":"address"},{"internalType":"uint256","name":"outputQuote","type":"uint256"},{"internalType":"uint256","name":"outputMin","type":"uint256"},{"internalType":"address","name":"outputReceiver","type":"address"}],"internalType":"struct OdosRouterV2.swapTokenInfo","name":"tokenInfo","type":"tuple"},{"internalType":"bytes","name":"pathDefinition","type":"bytes"},{"internalType":"address","name":"executor","type":"address"},{"internalType":"uint32","name":"referralCode","type":"uint32"}],"name":"swapPermit2","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"}],"internalType":"struct OdosRouterV2.inputTokenInfo[]","name":"inputs","type":"tuple[]"},{"components":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"uint256","name":"relativeValue","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"}],"internalType":"struct OdosRouterV2.outputTokenInfo[]","name":"outputs","type":"tuple[]"},{"internalType":"uint256","name":"valueOutMin","type":"uint256"},{"internalType":"bytes","name":"pathDefinition","type":"bytes"},{"internalType":"address","name":"executor","type":"address"}],"name":"swapRouterFunds","outputs":[{"internalType":"uint256[]","name":"amountsOut","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"tokens","type":"address[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"address","name":"dest","type":"address"}],"name":"transferRouterFunds","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"addresses","type":"address[]"}],"name":"writeAddressList","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]

# Tokens data per chain
TOKENS_PER_CHAIN = {
    "Arbitrum": {
        "ETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        "USDC": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
        "USDT": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
        "DAI": "0xDA10009cBd5D07dd0CeCc6eCea36FFB46FFb9021"
    }
}

# Zero address
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"