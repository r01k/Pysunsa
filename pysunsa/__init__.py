

import aiohttp
import json
import logging

from .exceptions import PysunsaError

_LOGGER = logging.getLogger(__name__)

RESPONSE_STATUS = "status"
RESPONSE_STATUSTEXT = "statustext"
RESPONSE_ERRORSTATUS = "Error"
GET = "get"
POST = "put"


class Pysunsa:
    """Sunsa REST API client"""
    def __init__(self, session, userid: int, apikey: str):
        self._rh = _RequestsHandler(session, userid, apikey)
        self._devices = None

    async def send_command(self, request, api_method, **data):
        data = await self._rh.query(request=request, method=api_method, data=data)
        if RESPONSE_STATUS in data and data[RESPONSE_STATUS] == RESPONSE_ERRORSTATUS:
            raise PysunsaError(RESPONSE_ERRORSTATUS, data[RESPONSE_STATUSTEXT])
        return data

    async def get_devices(self):
        result = await self.send_command(GET, "devices")
        self._devices = result["devices"]
        return self._devices

    async def get_device_info(self, device_id):
        for device in await self.get_devices():
            if device["idDevice"] == device_id:
                return device

    @property
    def devices(self):
        return self._devices

    async def update_device(self, device_id, position: int):
        """
        Set the blinds position.
        :param int device_id:
        :param int position: The position of the blinds, can be increments of 10 \
        from -100 to 100, where 0 is open, -100 is closed in one direction and 100 is \
        closed in the other direction.
        """
        await self.send_command(
            request=POST,
            api_method=f"devices/{device_id}",
            position=position
        )


class _RequestsHandler:
    """Internal class to handle Sunsa API requests"""

    def __init__(self, session: aiohttp.ClientSession, userid, apikey):
        self.headers = {"Accept": "application/json"}
        self.params = {"publicApiKey": apikey}
        self.session = session
        self.userid = userid

    async def query(self, request: str, method: str, params=None, data=None) -> dict:
        """
        :param str request: The HTTP request type: 'get', 'put'.
        :param str method: Sunsa API method name.
        :param dict params: Method parameters. The 'publicApiKey' parameter is set \
        automatically.
        :param dict data: Data required (request JSON).
        """
        url = f"https://sunsahomes.com/api/public/{self.userid}/{method}"
        if params is None:
            params = dict()
        params.update(self.params)
        kwargs = {
            "url": url,
            "params": params,
            "headers": self.headers,
        }
        if request == POST:
            kwargs["json"] = data

        session_method = getattr(self.session, request)

        _LOGGER.debug("Sending %s request against \"%s\" endpoint",
                      request.upper(), method)
        _LOGGER.debug("Parameters: %s", kwargs)
        async with session_method(**kwargs) as response:
            if response.status != 200:
                _LOGGER.warning(
                    "Error response from Sunsa API: %s",
                    response.status
                )
                raise PysunsaError(response.status, await response.text())

            try:
                data = await response.json()
            except aiohttp.client_exceptions.ContentTypeError:
                data = await response.json(content_type="text/html")

            _LOGGER.debug(json.dumps(data))
            return data
