from . import responses

def resolve(response:"responses.Response", fail_value=None):
    "If response is successful, returns the response object. Otherwise, the given fail_value will be returned (None by default)."

    if isinstance(response, responses.SuccessResponse):
        return response
    else:
        return fail_value
