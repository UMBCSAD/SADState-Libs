from . import permissions, profiles, projects
from dataclasses import dataclass
import requests

@dataclass(slots=True)
class Response:
    "Base class for API responses."
    response:requests.Response

    @property
    def response_name(self):
        return type(self).__name__

    @property
    def code(self):
        return self.response.status_code
    
    @property
    def ok(self):
        return self.response.ok

    def __repr__(self):
        return f"<{self.response_name} [{self.code}] at {hex(id(self))}>"
    
    def __bool__(self):
        return isinstance(self, SuccessResponse)
    

#ok responses

class SuccessResponse(Response):
    "A successful response."

@dataclass(slots=True)
class AuthResponse(SuccessResponse):
    "A response containing an Auth ID."
    id:int

@dataclass(slots=True)
class ProjectResponse(SuccessResponse):
    "A response containing a Project."
    project:"projects.Project"

@dataclass(slots=True)
class ProfileResponse(SuccessResponse):
    "A response containing one or more Profiles."
    profiles:"list[profiles.Profile]"

    @property
    def profile(self):
        return self.profiles[0] if self.profiles else None
    
@dataclass(slots=True)
class RemainingSpaceResponse(SuccessResponse):
    "A response containing the number of bytes left unused in a Profile."

    num_bytes:int

    
class ProfileContentResponse(SuccessResponse):
    "A response containing the contents of a Profile."

    @property
    def content(self):
        return self.response.content


#not ok responses
class ErrorResponse(Response):
    "An unsuccessful response."

    @property
    def reason(self):
        return self.response.text

class UnexpectedErrorResponse(ErrorResponse):
    "A response indicating that an unexpected error occured."

class NotFoundResponse(ErrorResponse):
    "A response indicating that the requested resource could not be found."

class AlreadyExistsResponse(ErrorResponse):
    "A response indicating that the provided resource already exists on the server."

@dataclass(slots=True)
class InvalidPermissionResponse(ErrorResponse):
    "A containing the permissions needed to carry out the attempted action."
    value:"permissions.ProjectPermissions|permissions.ProfilePermissions"

class InvalidInputResponse(ErrorResponse):
    "A response indicating that the proper values were not used when creating the request."
    
class InvalidAuthResponse(ErrorResponse):
    "A response indicating that the session has not been authenticated."
