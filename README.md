# Web3 Integration: Bitget ↔ Arbitrum

A comprehensive solution for automated cross-platform DeFi operations, integrating centralized exchange (Bitget) functionality with decentralized finance protocols on the Arbitrum network.

## Features

- **CEX Integration**: Withdraw and deposit funds to/from Bitget exchange
- **Arbitrum Blockchain**: Direct interaction with the Arbitrum Layer 2 network
- **DEX Swapping**: Token swapping via Odos DEX with optimal routing
- **Automated Pipeline**: Complete workflow for USDC → ETH → deposit operations
- **Configurable**: Easily adaptable for different tokens and networks

## Prerequisites

- Python 3.11+ (tested on 3.11.12)
- Bitget API credentials
- Ethereum private key with funds for gas on Arbitrum
- Basic understanding of DeFi operations

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/my_first_web3_software.git
cd my_first_web3_software
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the project root with the following variables:
```
# Bitget API credentials
BITGET_API_KEY=your_bitget_api_key
BITGET_API_SECRET=your_bitget_api_secret
BITGET_API_PASSPHRASE=your_bitget_api_passphrase

# Ethereum wallet
PRIVATE_KEY=your_ethereum_private_key

# Optional proxy configuration
PROXY=http://your_proxy_if_needed
```

2. Review and adjust settings in `settings.py` and network configurations in `config/networks.py` if needed.

## Usage

Run the main script to execute the complete pipeline:

```bash
python main.py
```

The script will:
1. Withdraw USDC from your Bitget account to your Ethereum wallet on Arbitrum
2. Swap USDC to ETH using Odos DEX on Arbitrum
3. Deposit the resulting ETH back to your Bitget account

## Architecture

### Core Components

- **CEX Module**
  - `BitgetClient`: Handles API interactions with Bitget exchange

- **Web3 Module**
  - `Web3Client`: Core interaction with Arbitrum blockchain
  - `OdosClient`: Interface for Odos DEX swaps

- **Config**
  - Network definitions
  - Token addresses
  - API credentials

## Project Structure

```
my_first_web3_software/
├── cex/
│   └── bitget_client.py        # Bitget exchange API integration
├── web3_module/
│   ├── client.py               # Core Web3 functionality
│   └── defi/
│       └── odos_client.py      # Odos DEX integration
├── config/
│   ├── __init__.py             # Configuration loading
│   └── networks.py             # Network definitions
│   └── config.py               # Configuration variables
│   └── networks.py             # Network definitions
├── main.py                     # Main execution script
├── settings.py                 # Application settings
└── requirements.txt            # Project dependencies
```

## License

MIT License

## Disclaimer

This software is for educational purposes only. Use at your own risk. Always verify the transactions before executing them with real funds.

## Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
