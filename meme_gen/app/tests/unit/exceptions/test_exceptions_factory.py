from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from app.exceptions.factory import ExceptionsFactory
from django.test import TestCase
from django.http import Http404

class ExceptionsFactoryTestCase(TestCase):
    def test_transform_common_exceptions(self):
        common_exceptions = [
            (TypeError("Invalid type"), 400, "The given type is invalid"),
            (ValueError("Invalid value"), 400, "The given value is invalid"),
            (ValidationError("Invalid value"), 400, "The given value is invalid"),
            (AttributeError("Invalid attribute"), 400, "The given attribute is invalid"),
            (ObjectDoesNotExist("Object not found"), 404, "The requested model was not found"),
            (Http404("Resource not found"), 404, "The requested resource was not found"),
        ]

        for exception, expected_status, expected_message in common_exceptions:
            result = ExceptionsFactory.transform_exception(exception)
            self.assertEqual(result["object"], "error")
            self.assertEqual(result["message"], expected_message)
            self.assertEqual(result["custom_message"], str(exception))
            self.assertEqual(result["status_code"], expected_status)

    def test_transform_drf_validation_error(self):
        drf_error = DRFValidationError({"field1": ["Error 1"], "field2": ["Error 2"]})
        result = ExceptionsFactory.transform_exception(drf_error)

        self.assertEqual(result["object"], "error")
        self.assertEqual(result["message"], "Validation error")
        self.assertEqual(result["custom_message"], "field1: Error 1, field2: Error 2")
        self.assertEqual(result["status_code"], 400)

    def test_transform_generic_unexpected_exception(self):
        unknown_error = Exception("Unknown error")
        result = ExceptionsFactory.transform_exception(unknown_error)

        self.assertEqual(result["object"], "error")
        self.assertEqual(result["message"], "Something went wrong")
        self.assertEqual(result["custom_message"], "Unknown error")
        self.assertEqual(result["status_code"], 500)

    def test_handle_value_error(self):
        test_error = ValueError("Test error")
        response = ExceptionsFactory.handle(test_error)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), '{"object": "error", "message": "The given value is invalid", "custom_message": "Test error", "status_code": 400}')

    def test_handle_generic_unexpected_exception_while_generating_exception_object(self):
        def mock_transform_exception(e):
            raise Exception("Unexpected error")

        original_transform_exception = ExceptionsFactory.transform_exception
        ExceptionsFactory.transform_exception = mock_transform_exception

        try:
            test_error = ValueError("Test error")
            response = ExceptionsFactory.handle(test_error)

            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.content.decode(), '{"object": "error", "message": "Something went wrong", "custom_message": "Unexpected error while generating an exception object", "status_code": 500}')
        finally:
            ExceptionsFactory.transform_exception = original_transform_exception