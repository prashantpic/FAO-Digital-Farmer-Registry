from abc import ABC, abstractmethod
from odoo.addons.dfr_integrations.dtos import EmailSendRequest, EmailSendResponse, EmailProviderConfig

class EmailGatewayClientInterface(ABC):
    """
    Abstract Base Class (ABC) defining the interface for an Email gateway client.
    This allows for different Email gateway providers to be implemented and used
    interchangeably by the EmailDispatchService.
    """

    def __init__(self, config: EmailProviderConfig, timeout_seconds: int = 15):
        """
        Initializes the Email gateway client.

        :param config: An EmailProviderConfig DTO containing provider-specific configuration
                       (e.g., API key, URL).
        :param timeout_seconds: Timeout for API requests in seconds.
        """
        self.config = config
        self.timeout_seconds = timeout_seconds
        super().__init__()

    @abstractmethod
    def send_email(self, request_dto: EmailSendRequest) -> EmailSendResponse:
        """
        Sends an email message.

        This method must be implemented by concrete subclasses.

        :param request_dto: An EmailSendRequest DTO containing the details of the email
                            to be sent (to, from, subject, body, attachments).
        :return: An EmailSendResponse DTO indicating the result of the send operation
                 (message ID, status, error details if any).
        """
        pass