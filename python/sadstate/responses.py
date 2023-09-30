from . import permissions, profiles, projects
from dataclasses import dataclass
import requests

@dataclass(slots=True)
class Response:
    ""
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
    ""

@dataclass(slots=True)
class AuthResponse(SuccessResponse):
    ""
    id:int

@dataclass(slots=True)
class ProjectResponse(SuccessResponse):
    ""
    project:"projects.Project"

@dataclass(slots=True)
class ProfileResponse(SuccessResponse):
    ""
    profiles:"list[profiles.Profile]"

    @property
    def profile(self):
        return self.profiles[0] if self.profiles else None
    
@dataclass(slots=True)
class RemainingSpaceResponse(SuccessResponse):
    ""

    num_bytes:int

    
class ProfileContentResponse(SuccessResponse):
    ""

    @property
    def content(self):
        return self.response.content


#not ok responses
class ErrorResponse(Response):
    ""

    @property
    def reason(self):
        return self.response.text

class UnexpectedErrorResponse(ErrorResponse):
    ""

class NotFoundResponse(ErrorResponse):
    ""

class AlreadyExistsResponse(ErrorResponse):
    ""

@dataclass(slots=True)
class InvalidPermissionResponse(ErrorResponse):
    ""
    value:"permissions.ProjectPermissions|permissions.ProfilePermissions"

class InvalidInputResponse(ErrorResponse):
    ""
    
class InvalidAuthResponse(ErrorResponse):
    ""
