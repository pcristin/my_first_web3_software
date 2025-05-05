from config.networks import Network
from config.config import *
from config.interfaces import *

Arbitrum = Network(
    name="Arbitrum",
    rpcs=["https://arbitrum.llamarpc.com"],
    chain_id=42161,
    eip1559_support=True,
    token="ETH",
    explorer="https://arbiscan.io",
    bitget_chain="ArbitrumOne"
)

Networks = [
    Arbitrum
]