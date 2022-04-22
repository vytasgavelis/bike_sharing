from django.http import JsonResponse


class ResponseHelper:
    @staticmethod
    def get_sucess_response() -> JsonResponse:
        return JsonResponse({'success': True}, safe=False)

    @staticmethod
    def get_failed_response(message: str = 'Error') -> JsonResponse:
        return JsonResponse({'success': False, 'message': message}, safe=False)