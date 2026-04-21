from __future__ import annotations

from bt_api_base.error import ErrorTranslator, UnifiedErrorCode


class BitmartErrorTranslator(ErrorTranslator):
    @staticmethod
    def translate(error_data) -> UnifiedErrorCode:
        if error_data is None:
            return UnifiedErrorCode.NO_DATA

        if isinstance(error_data, dict):
            code = error_data.get("code")
            message = error_data.get("message", "")

            if code is not None and code != 1000:
                if "balance" in message.lower() or "insufficient" in message.lower():
                    return UnifiedErrorCode.INSUFFICIENT_BALANCE
                if "order" in message.lower():
                    if "not found" in message.lower():
                        return UnifiedErrorCode.ORDER_NOT_FOUND
                    if "duplicate" in message.lower():
                        return UnifiedErrorCode.DUPLICATE_ORDER
                    return UnifiedErrorCode.ORDER_REJECTED
                if "rate" in message.lower() or "limit" in message.lower():
                    return UnifiedErrorCode.RATE_LIMIT
                if "auth" in message.lower() or "key" in message.lower() or "signature" in message.lower():
                    return UnifiedErrorCode.AUTH_ERROR
                return UnifiedErrorCode.UNKNOWN_ERROR

        return UnifiedErrorCode.NO_ERROR
