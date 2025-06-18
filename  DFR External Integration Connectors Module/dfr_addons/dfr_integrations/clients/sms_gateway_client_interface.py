from abc import ABC, abstractmethod
from odoo.addons.dfr_integrations.dtos import SmsSendRequest, SmsSendResponse, SmsProviderConfig

class SmsGatewayClientInterface(ABC):
    """
    Abstract Base Class (ABC) defining the interface for an SMS gateway client.
    This allows for different SMS gateway providers to be implemented and used
    interchangeably by the SmsDispatchService.
    """

    def __init__(self, config: SmsProviderConfig, timeout_seconds: int = 10):
        """
        Initializes the SMS gateway client.

        :param config: An SmsProviderConfig DTO containing provider-specific configuration
                       (e.g., API key, secret, URL).
        :param timeout_seconds: Timeout for API requests in seconds.
        """
        self.config = config
        self.timeout_seconds = timeout_seconds
        super().__init__()

    @abstractmethod
    def send_sms(self, request_dto: SmsSendRequest) -> SmsSendResponse:
        """
        Sends an SMS message.

        This method must be implemented by concrete subclasses.

        :param request_dto: An SmsSendRequest DTO containing the details of the SMS
                            to be sent (recipient, message body, sender ID).
        :return: An SmsSendResponse DTO indicating the result of the send operation
                 (message SID, status, error details if any).
        """
        pass