"""Payment utilities."""

# Django
from asyncio.log import logger
from django.conf import settings

# Utils
import urllib
import requests
import json

# RESPONSE TYPES

BAD_JSON_ERROR = "BAD_JSON_ERROR"
TIMEOUT_ERROR = "TIMEOUT_ERROR"
HTTP_ERROR = "HTTP_ERROR"
CONNECTION_ERROR = "CONNECTION_ERROR"
UNKNOWN_ERROR = "UNKNOWN_ERROR"


class WompiPayment:
    """Wrapper Wompi payments."""

    def _get_resource(self, uri, **kwargs):
        """Get resource method."""
        if "id_transaction" not in kwargs:
            querystring = urllib.parse.urlencode(kwargs)
            url = f"{settings.API_WOMPI_URL}/{uri}?{querystring}"
        else:
            id_transaction = kwargs.pop("id_transaction")
            url = f"{settings.API_WOMPI_URL}/{uri}/{id_transaction}"
        logger.info(url)
        r = requests.get(url, timeout=10)
        logger.info(r.text)
        return r

    def _post_resource(self, uri, **kwargs):
        """Post resource method."""
        url = f"{settings.API_WOMPI_URL}/{uri}"
        if "key" in kwargs:
            kwargs.pop("key")
            headers = {"Authorization": f"Bearer {settings.WOMPI_PUB_KEY}"}
        else:
            headers = {"Authorization": f"Bearer {settings.WOMPI_PRIV_KEY}"}
        logger.info(kwargs)
        r = requests.post(url, headers=headers, data=json.dumps(kwargs), timeout=100)
        logger.info(r.text)
        return r

    def _get_json_resource(self, uri, **kwargs):
        try:
            response_json = {}
            method = kwargs.pop("method")
            if method == "get":
                response = self._get_resource(uri, **kwargs)
            else:
                response = self._post_resource(uri, **kwargs)
            response.raise_for_status()
            status_code = response.status_code
            success_response = status_code in [
                requests.codes.ok,
                requests.codes.created,
            ]
            response_json = {
                "status_code": status_code,
                f"{'response' if success_response else 'error'}": response.json(),
            }
        except requests.exceptions.RequestException as e:
            status_code = getattr(e.response, "status_code", None)
            reason = getattr(e.response, "text", None)
            response_json = {
                "status_code": status_code,
                "error": reason,
            }
        return response_json

    def credit_card_tokenization(self, data):
        """Credit Card Tokenization."""
        uri = "tokens/cards"
        method = "post"
        return self._get_json_resource(
            uri,
            method=method,
            key="priv",
            number=data["number"],
            cvc=data["cvc"],
            exp_month=data["exp_month"],
            exp_year=data["exp_year"],
            card_holder=data["card_holder"],
        )

    def create_payment_source(self, token, email):
        """Build payment source based on token for future payments.

        Args:
            token ([string]): [wompi pre signed token]
            email ([email]): [client email]
        """
        uri = "payment_sources"
        method = "post"
        # Get acceptance token
        acceptance_token = self.get_acceptance_token()
        response = self._get_json_resource(
            uri,
            method=method,
            acceptance_token=acceptance_token,
            token=token,
            customer_email=email,
            type="CARD",
        )
        response = response.get("response")
        return response.get("data").get("id")

    def transactions_read(self, id_transaction):
        """Read transactions information."""
        uri = "transactions"
        method = "get"
        return self._get_json_resource(
            uri,
            method=method,
            id_transaction=id_transaction,
        )

    def get_acceptance_token(self):
        """Create acceptance token."""
        uri = f"merchants/{settings.WOMPI_PUB_KEY}"
        method = "get"
        response = self._get_json_resource(uri, method=method)
        data = response.get("response").get("data")
        return data.get("presigned_acceptance").get("acceptance_token")

    def create_transaction(self, data):
        """Create transaction."""
        uri = "transactions"
        method = "post"

        return self._get_json_resource(uri, method=method, **data)
