from . import permissions as permissions_, profiles, projects, responses
import base64
import json
import requests
import urllib.parse


def _param(val:str):
    return urllib.parse.quote(val, safe="")

def _b64_id(id:str):
    return int.from_bytes(base64.b64decode(id.encode("utf-8")), "little")

class Session:
    "Carries out standalone API calls and handles all requested resources."

    def __init__(self, host:str):
        self.host = host
        self.auth_id:int = None
        self._s = requests.Session()
        self._cached:dict[int, projects.Project|profiles.Profile] = {}

    def clear_cache(self):
        "Clears the cache of all constructed objects."
        self._cached.clear()

    def new_auth(self, password:str):
        "Creates a new Auth ID given a password."
        r = self._s.post(f"{self.host}/auth/new", data={"password":password})
        if r.status_code == 200:
            id = int(r.text)
            if id != self.auth_id:
                self._cached.clear()
            self.auth_id = id
            return responses.AuthResponse(r, self.auth_id)
        elif r.status_code == 400:
            return responses.InvalidInputResponse(r)
        else:
            return responses.UnexpectedErrorResponse(r)

    def authenticate(self, id:int, password:str):
        "Authenticates the session given an Auth ID and password."
        r = self._s.post(f"{self.host}/auth/set", data={"id":id, "password":password})
        if r.status_code == 200:
            if id != self.auth_id:
                self._cached.clear()
            self.auth_id = id
            return responses.SuccessResponse(r)
        elif r.status_code == 401:
            return responses.InvalidAuthResponse(r)
        else:
            return responses.UnexpectedErrorResponse(r)
        
    def get_project(self, name:str):
        "Gets a Project with the given name."
        r = self._s.get(f"{self.host}/project/get?name={_param(name)}")
        if r.status_code == 200:
            data = r.json()
            id = _b64_id(data["id"])
            if id in self._cached:
                proj = self._cached[id]
                proj._from_data(data)
            else:
                proj = self._cached[id] = projects.Project.from_data(data, self)
            return responses.ProjectResponse(r, proj)
        elif r.status_code == 403:
            return responses.InvalidPermissionResponse(r, permissions_.ProjectPermissions.VIEW)
        elif r.status_code == 404:
            return responses.NotFoundResponse(r)
        else:
            return responses.UnexpectedErrorResponse(r)

    def register_project(self, name:str, permissions:dict[int, permissions_.ProjectPermissions]=None, **fields):
        "Registers a new Project."
        fields["permissions"] = None if permissions is None else {auth_id:perm.value for auth_id, perm in permissions.items()}
        r = self._s.post(f"{self.host}/project/register", data={
            "name":name,
            "fields":json.dumps(fields)
        })
        if r.status_code == 200:
            return responses.SuccessResponse(r)
        elif r.status_code == 400:
            return responses.InvalidInputResponse(r)
        elif r.status_code == 401:
            return responses.InvalidAuthResponse(r)
        elif r.status_code == 403:
            if r.text.startswith("Already a Project"):
                return responses.AlreadyExistsResponse(r)
            else:
                return responses.InvalidInputResponse(r)
        else:
            return responses.UnexpectedErrorResponse(r)

