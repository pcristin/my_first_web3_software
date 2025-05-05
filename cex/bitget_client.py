import time
import hmac
import base64
import hashlib
import json
from urllib.parse import urlencode
import aiohttp
import logging
from config import BITGET_API_KEY, BITGET_API_SECRET, BITGET_API_BASE_URL, BITGET_API_PASSPHRASE


class BitgetClient:
    """
    A client for interacting with the Bitget API.
    Provides functionality to:
    1. Make POST withdrawals of funds to specified wallet addresses
    2. Get deposit addresses for receiving funds
    """
    
    def __init__(self):
        """Initialize the Bitget API client with API credentials from config."""
        self.api_key = BITGET_API_KEY
        self.api_secret = BITGET_API_SECRET
        self.api_passphrase = BITGET_API_PASSPHRASE
        self.base_url = BITGET_API_BASE_URL
        self.logger = logging.getLogger('bitget_arbitrum')

    def _generate_signature(self, request_path: str, method: str, timestamp: str, data: dict = None) -> str:
        """
        Generate a signature for API authentication.
        
        Args:
            request_path: The API endpoint path
            method: HTTP method (GET, POST, etc.)
            timestamp: Current timestamp in milliseconds
            data: Request payload for POST requests
            
        Returns:
            str: Base64 encoded signature
        """
        body = ""
        if data:
            body = json.dumps(data)
            
        message = str(timestamp) + str.upper(method) + request_path + body
            
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        return base64.b64encode(signature).decode('utf-8')

    def _parse_params_to_str(self, params: dict) -> str:
        """
        Convert params to sorted URL query string.
        
        Args:
            params: Dictionary of parameters
            
        Returns:
            str: URL query string
        """
        if not params:
            return ''
            
        # Sort params by key
        param_list = [(key, val) for key, val in params.items()]
        param_list.sort(key=lambda x: x[0])
        
        # Convert to URL query string without encoding
        url = '?'
        for key, value in param_list:
            url = url + str(key) + '=' + str(value) + '&'
        
        # Remove trailing '&'
        return url[:-1]

    def _get_headers(self, path: str, method: str, params: dict = None, data: dict = None) -> dict:
        """
        Generate headers required for API requests.
        
        Args:
            path: API endpoint path
            method: HTTP method
            params: URL parameters for GET requests
            data: Request payload for POST requests
            
        Returns:
            dict: Headers for API request
        """
        timestamp = str(int(time.time() * 1000))
        
        # For GET requests with params, we need to include them in the signature
        if method == "GET" and params:
            # Add sorted params to path for signature
            query_string = self._parse_params_to_str(params)
            signature_path = path + query_string
            signature = self._generate_signature(signature_path, method, timestamp)
        else:
            signature = self._generate_signature(path, method, timestamp, data)
        
        headers = {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": signature,
            "ACCESS-PASSPHRASE": self.api_passphrase,
            "ACCESS-TIMESTAMP": timestamp,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        return headers

    async def _make_request(self, method: str, path: str, params: dict = None, data: dict = None) -> dict:
        """
        Make an API request to Bitget.
        
        Args:
            method: HTTP method
            path: API endpoint path
            params: URL parameters for GET requests
            data: Request payload for POST requests
            
        Returns:
            dict: API response
        """
        url = f"{self.base_url}{path}"
        
        if params:
            url += f"?{urlencode(params)}"
        
        self.logger.debug(f"Making {method} request to {url}")
        if data:
            self.logger.debug(f"Request data: {json.dumps(data)}")
            
        headers = self._get_headers(path, method, params, data)
        
        async with aiohttp.ClientSession() as session:
            if method == "GET":
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        self.logger.error(f"API Error: {method} {url} - Status {response.status} - {error_text}")
                        raise Exception(f"Error {response.status}: {error_text}")
            elif method == "POST":
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        self.logger.error(f"API Error: {method} {url} - Status {response.status} - {error_text}")
                        raise Exception(f"Error {response.status}: {error_text}")

    async def withdraw(self, coin: str, chain: str, amount: str, to_address: str, client_oid: str = None) -> dict:
        """
        Withdraw funds from Bitget to an external wallet.
        
        Args:
            coin: Currency code (e.g., BTC, ETH, USDT)
            chain: Blockchain network (e.g., BTC, ETH, TRX)
            amount: Amount to withdraw
            to_address: Recipient address
            client_oid: Optional client-defined order ID
            
        Returns:
            dict: Withdrawal response data
        """
        
        path = "/api/v2/spot/wallet/withdrawal"
        
        # Validate inputs
        if not coin or not chain or not amount or not to_address:
            raise ValueError("Missing required parameters for withdrawal")
            
        # Check if we have API credentials
        if not self.api_key or not self.api_secret:
            raise ValueError("Missing API credentials")
        
        data = {
            "coin": coin,
            "transferType": "on_chain",
            "chain": chain,
            "size": amount,
            "address": to_address,
        }
        
        if client_oid:
            data["clientOid"] = client_oid
        
        # First check if withdrawal is possible by checking the balance
        try:
            assets = await self.get_account_assets(coin=coin)
            self.logger.debug(f"Current assets: {json.dumps(assets)}")
            
            # Make sure we have sufficient balance
            if assets.get('code') == '00000' and assets.get('data'):
                for asset in assets.get('data', []):
                    if asset.get('coin') == coin:
                        available = float(asset.get('available', '0'))
                        if available < float(amount):
                            raise ValueError(f"Insufficient balance: {available} {coin} available, trying to withdraw {amount}")
            
            return await self._make_request("POST", path, data=data)
        except Exception as e:
            raise

    async def get_deposit_address(self, coin: str, chain: str = None) -> dict:
        """
        Get a deposit address for receiving funds.
        
        Args:
            coin: Currency code (e.g., BTC, ETH, USDT)
            chain: Optional blockchain network (e.g., BTC, ETH, TRX)
            
        Returns:
            dict: Deposit address information
        """
        path = "/api/v2/spot/wallet/deposit-address"
        timestamp = str(int(time.time() * 1000))
        params = {"coin": coin}
        
        if chain:
            params["chain"] = chain
        
        # Sort params alphabetically
        sorted_params = sorted(params.items())
        query_string = "&".join([f"{key}={value}" for key, value in sorted_params])
        
        # Build the message to sign - format: timestamp + method + requestPath + body(if post)
        signature_path = path + "?" + query_string
        message = timestamp + "GET" + signature_path
        
        # Generate signature
        signature = base64.b64encode(
            hmac.new(
                self.api_secret.encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).digest()
        ).decode('utf-8')
        
        # Prepare headers
        headers = {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.api_passphrase,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Build URL
        url = f"{self.base_url}{path}?{query_string}"
        
        self.logger.debug(f"Making request to: {url}")
        self.logger.debug(f"Headers: {headers}")
        self.logger.debug(f"Message to sign: {message}")
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response_text = await response.text()
                self.logger.debug(f"Response status: {response.status}")
                self.logger.debug(f"Response body: {response_text}")
                
                if response.status == 200:
                    return json.loads(response_text)
                else:
                    self.logger.error(f"API Error: GET {url} - Status {response.status} - {response_text}")
                    raise Exception(f"Error {response.status}: {response_text}")

    async def get_account_assets(self, coin: str = None) -> dict:
        """
        Get account asset information.
        
        Args:
            coin: Optional currency code to filter results
            
        Returns:
            dict: Account asset information
        """
        try:
            # Use v2 endpoint
            path = "/api/v2/spot/account/assets"
            params = {}
            
            if coin:
                params["coin"] = coin
                
            response = await self._make_request("GET", path, params=params)
            self.logger.debug(f"Response: {json.dumps(response)}")
            return response
        except Exception as e:
            raise

    async def get_withdrawal_history(self, coin: str = None, start_time: str = None, 
                                     end_time: str = None, page_size: int = 20, 
                                     client_oid: str = None) -> dict:
        """
        Get withdrawal history.
        
        Args:
            coin: Optional currency code
            start_time: Optional start time (milliseconds timestamp)
            end_time: Optional end time (milliseconds timestamp)
            page_size: Number of records per page (default 20)
            client_oid: Optional client-defined order ID
            
        Returns:
            dict: Withdrawal history
        """
        path = "/api/v2/spot/wallet/withdraw-list"
        params = {"pageSize": page_size}
        
        if coin:
            params["coin"] = coin
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        if client_oid:
            params["clientOid"] = client_oid
            
        return await self._make_request("GET", path, params=params)

    async def get_deposit_history(self, coin: str = None, start_time: str = None, 
                                  end_time: str = None, page_size: int = 20) -> dict:
        """
        Get deposit history.
        
        Args:
            coin: Optional currency code
            start_time: Optional start time (milliseconds timestamp)
            end_time: Optional end time (milliseconds timestamp)
            page_size: Number of records per page (default 20)
            
        Returns:
            dict: Deposit history
        """
        path = "/api/v2/spot/wallet/deposit-list"
        params = {"pageSize": page_size}
        
        if coin:
            params["coin"] = coin
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
            
        return await self._make_request("GET", path, params=params)
