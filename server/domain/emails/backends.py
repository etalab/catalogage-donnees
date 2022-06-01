from .entities import Email


class EmailBackend:
    @classmethod
    def options(self) -> dict:
        return {}

    async def send(self, email: Email, fail_silently: bool = False) -> bool:
        """
        Send an email.

        Raises
        ------
        EmailDeliveryFailed:
            If email failed to send and fail_silently is not set.

        Returns
        -------
        sent: bool
            True if the email was sent successfully, False otherwise.
        """
        raise NotImplementedError  # pragma: no cover
