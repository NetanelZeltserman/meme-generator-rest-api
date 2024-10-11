from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import ObjectDoesNotExist as ModelObjectDoesNotExist
from django.http import Http404, JsonResponse
from typing import Dict, Tuple

class ExceptionsFactory:
    COMMON_EXCEPTION_MAPPING: Dict[type, Tuple[int, str]] = {
        TypeError: (400, "The given type is invalid"),
        ValueError: (400, "The given value is invalid"),
        ValidationError: (400, "The given value is invalid"),
        DRFValidationError: (400, "The given value is invalid"),
        AttributeError: (400, "The given attribute is invalid"),
        ObjectDoesNotExist: (404, "The requested model was not found"),
        ModelObjectDoesNotExist: (404, "The requested model was not found"),
        Http404: (404, "The requested resource was not found"),
    }

    @staticmethod
    def transform_exception(e: Exception) -> dict:
        """Transform the given exception to an error object."""
        if isinstance(e, DRFValidationError):
            return ExceptionsFactory._handle_drf_validation_error(e)

        status_code, message = ExceptionsFactory.COMMON_EXCEPTION_MAPPING.get(
            type(e), (500, "Something went wrong")
        )

        return {
            "object": "error",
            "message": message,
            "custom_message": str(e),
            "status_code": status_code,
        }

    @staticmethod
    def _handle_drf_validation_error(e: DRFValidationError) -> dict:
        custom_message = ", ".join(f"{field}: {errors[0]}" for field, errors in e.detail.items())
        return {
            "object": "error",
            "message": "Validation error",
            "custom_message": custom_message,
            "status_code": 400,
        }

    @staticmethod
    def handle(e: Exception) -> JsonResponse:
        """Handle the given exception and return an appropriate response."""
        try:
            error_object = ExceptionsFactory.transform_exception(e)
            return JsonResponse(error_object, status=error_object["status_code"])
        except Exception:
            return JsonResponse(
                {
                    "object": "error",
                    "message": "Something went wrong",
                    "custom_message": "Unexpected error while generating an exception object",
                    "status_code": 500,
                },
                status=500
            )