from typing import Any, Tuple, Dict
import requests
from loguru import logger
import json


class HTTPAPI:
    """AsyncHTTPAPI is an Async web wrapper based on aiohttp.

    This can be used in any module that needs to build a client side HTTP API for both
    sync and async APIs. This class shouldn't be used directly but inherited to help build
    more specific client HTTPAPIs for applications that NetZeus CLI will interact with.

    Args:
        base_url:       Base URL to build API requests from
        headers:        Dictionary of any headers to inject in all requests
        bearer_token:   Bearer Token if API uses an API token
        timeout:        Time to wait until raising an error if no response
    """

    def __init__(
        self,
        base_url: str = "https://localhost",
        headers: dict = {"Content-Type": "application/json"},
        bearer_token: str = "",
        timeout: int = 20,
        verify_ssl: bool = False,
    ) -> None:
        self.url = base_url
        self.headers = headers
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if bearer_token:
            self.headers.update({"Authorization": bearer_token})

    def get(
        self, endpoint: str, params: dict = {}
    ) -> Tuple[int, Dict[str, Any], bytes]:
        """GET HTTP Operation

        Args:
            endpoint:       Endpoint (eg. "/api/v1/myendpoint")
        """
        url = self.url + endpoint
        logger.debug(f"GET: {url}")
        response = requests.get(
            url=url,
            headers=self.headers,
            timeout=self.timeout,
            params=params,
            verify=self.verify_ssl,
        )

        try:
            response_json = response.json()
        except json.decoder.JSONDecodeError as e:
            pass

        return response.status_code, response_json

    def post(self, endpoint: str, body: dict) -> Tuple[int, Dict[str, Any], bytes]:
        """POST HTTP Operation

        Args:
            endpoint:       Endpoint (eg. "/api/v1/myendpoint")
            body:           JSON body to send in POST message
        """
        url = self.url + endpoint
        logger.debug(f"POST: {url}")
        response = requests.post(
            url=url,
            json=body,
            headers=self.headers,
            timeout=self.timeout,
            verify=self.verify_ssl,
        )

        if response.status_code >= 400 and response.status_code <= 500:
            response.raise_for_status()

        response_json = None
        try:
            response_json = response.json()
        except json.decoder.JSONDecodeError as e:
            # Need to implement better error handling here
            pass

        return response.status_code, response_json

    def build_params(self, params: dict) -> dict:
        """Builds parameters and normalizes them so you can use it with aiohttp

        Args:
            params:     Dict of parameters
        """
        return {k: v for k, v in params.items() if v is not None}
