from . import exceptions, permissions as permissions_, projects, responses, sessions
import io
import json
import weakref

class Profile:
    "Allows for making API calls having to do with an individual Profile."

    __slots__ = "id", "name", "permissions", "_project", "_session", "__weakref__"

    @classmethod
    def from_data(cls, data:dict[str], project:"projects.Project", session:"sessions.Session"):
        "Construct a new Profile object from response data."
        instance = cls.__new__(cls)
        instance._project = weakref.ref(project)
        instance._session = weakref.ref(session)
        instance._from_data(data)
        return instance

    def _from_data(self, data:dict[str]):
        self.id = sessions._b64_id(data["id"])
        self.name = data["name"]
        self.permissions = {
            int(auth_id): permissions_.ProfilePermissions(value)
            for auth_id, value in data.get("permissions", {}).items()
        }


    def __init__(self, id:int, name:str, permissions:"dict[int, permissions_.ProfilePermissions]", project:"projects.Project", session:"sessions.Session"):
        self.id = id
        self.name = name
        self.permissions = permissions
        self._project = weakref.ref(project)
        self._session = weakref.ref(session)

    def __eq__(self, other):
        if isinstance(other, Profile):
            return other.name == self.name
        return super().__eq__(other)

    @property
    def project(self):
        return self._project()
    
    @property
    def session(self):
        return self._session()
    
    def update(self):
        "Update this Profile object with the latest data on the server."
        r = self.session._s.get(f"{self.session.host}/project/profile/get?name={sessions._param(self.project.name)}&profile_name={sessions._param(self.name)}")
        if r.status_code == 200:
            data = r.json()
            if data["id"] != self.id:
                self.session._cached.pop(self.id)
                raise exceptions.OutOfDateException(f"Project {self.name} has changed its name.")
            self._from_data()
            return responses.SuccessResponse(r)
        elif r.status_code == 403:
            return responses.InvalidPermissionResponse(r, permissions_.ProjectPermissions.VIEW)
        elif r.status_code == 404 and "Profile" in r.text:
            return responses.NotFoundResponse(r)
        else:
            return responses.UnexpectedErrorResponse(r)
        
    def remove(self):
        "Delete this Profile and remove it from its Project."
        resp = self.project.remove_profile(self.name)
        if isinstance(resp, (responses.SuccessResponse, responses.NotFoundResponse)):
            self.session._cached.pop(self.id, None)
        return resp
    
    def edit(self, name:str=None, permissions:dict[int, permissions_.ProfilePermissions]=None, **fields):
        "Edit this Profile's attributes (e.g. name, permissions)."

        fields["name"] = name
        fields["permissions"] = {id:perm.value for id, perm in permissions.items()}
        r = self.session._s.post(f"{self.session.host}/project/edit", data={
            "name":self.project.name,
            "profile_name":self.name,
            "fields":json.dumps(fields)
        })
        if r.status_code == 200:
            name = fields.get("name")
            if name is not None:
                self.name = name
            if permissions is not None:
                for auth_id, perm in permissions.items():
                    self.permissions[auth_id] = perm
            return responses.SuccessResponse(r)
        elif r.status_code == 400:
            return responses.InvalidInputResponse(r)
        elif r.status_code == 403:
            if r.text.startswith("Already a Profile"):
                return responses.AlreadyExistsResponse(r)
            elif r.text.startswith("Cannot give permissions"):
                for each in permissions_.ProjectPermissions:
                    if each.name in r.text:
                        return responses.InvalidPermissionResponse(r, each)
                #shouldn't ever reach here
                return responses.InvalidPermissionResponse(r, permissions_.ProjectPermissions(0))
            else:
                return responses.InvalidPermissionResponse(r, permissions_.ProjectPermissions(0))
        else:
            return responses.UnexpectedErrorResponse(r)

    def read(self):
        "Read this Profile's contents."
        r = self.session._s.get(f"{self.session.host}/project/profile/read?name={sessions._param(self.project.name)}&profile_name={sessions._param(self.name)}")
        if r.status_code == 200:
            return responses.ProfileContentResponse(r)
        elif r.status_code == 403:
            return responses.InvalidPermissionResponse(r, permissions_.ProfilePermissions.READ)
        elif r.status_code == 404 and "Profile" in r.text:
            return responses.NotFoundResponse(r)
        else:
            return responses.UnexpectedErrorResponse(r)
    
    def write(self, b:bytes|io.IOBase):
        "Write to this Profile's contents."
        return _profile_write(self, b, f"{self.session.host}/project/profile/write")

    def append(self, b:bytes|io.IOBase):
        "Append to this Profile's contents."
        return _profile_write(self, b, f"{self.session.host}/project/profile/append")



def _profile_write(p, b, url):
    if isinstance(b, io.IOBase) and not b.readable():
        raise TypeError("Given IO object must be readable.")
    r = p.session._s.post(url, data={
        "name":p.project.name,
        "profile_name":p.name
    }, files={"data":io.BytesIO(b) if isinstance(b, bytes) else b})
    if r.status_code == 200:
        return responses.RemainingSpaceResponse(r, int(r.text))
    elif r.status_code == 403:
        return responses.InvalidPermissionResponse(r, permissions_.ProfilePermissions.WRITE)
    elif r.status_code == 400 and "Profile" in r.text:
        return responses.NotFoundResponse(r)
    else:
        return responses.UnexpectedErrorResponse(r)

