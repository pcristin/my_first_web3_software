class Network:
    def __init__(self,
                 name: str,
                 rpcs: list,
                 chain_id: int,
                 eip1559_support: bool,
                 token: str,
                 explorer: str,
                 decimals: int = 18,
                 bitget_chain: str = None):
        self.name = name
        self.rpcs = rpcs
        self.chain_id = chain_id
        self.eip1559_support = eip1559_support
        self.token = token
        self.explorer = explorer
        self.decimals = decimals
        self.bitget_chain = bitget_chain
    
    """
    Network is a class that contains the information for a network.

    Arguments:
        name: str - The name of the network.
        rpcs: list - The list of RPCs for the network.
        chain_id: int - The chain ID of the network.
        eip1559_support: bool - Whether the network supports EIP-1559.
        token: str - The token of the network.
        explorer: str - The explorer of the network.
    """
    