from . import permissions as permissions_, profiles, responses, sessions
import json
import weakref

class Project:
    "Allows for making API calls having to do with an individual Project."

    __slots__ = "id", "name", "permissions", "_session", "__weakref__"

    @classmethod
    def from_data(cls, data:dict[str], session:"sessions.Session"):
        "Construct a new Project object from response data."
        instance = cls.__new__(cls)
        instance._session = weakref.ref(session)
        instance._from_data(data)
        return instance

    def _from_data(self, data:dict[str]):
        self.id = sessions._b64_id(data["id"])
        self.name = data["name"]

        self.permissions = {
            int(auth_id): permissions_.ProjectPermissions(value)
            for auth_id, value in data.get("permissions", {}).items()
        }

    def __init__(self, id:int, name:str, permissions:"dict[int, permissions_.ProjectPermissions]", session:"sessions.Session"):
        self.id = id
        self.name = name
        self.permissions = permissions
        self._session = weakref.ref(session)

    @property
    def session(self):
        return self._session()

    def __eq__(self, other):
        if isinstance(other, Project):
            return other.name == self.name
        return super().__eq__(other)
    
    def update(self):
        "Update this Project object with the latest data on the server."
        r = self.session._s.get(f"{self.session.host}/project/get?name={sessions._param(self.name)}")
        if r.status_code == 200:
            data:dict[str] = r.json()
            self._from_data(data)
            return responses.SuccessResponse(r)
        elif r.status_code == 403:
            return responses.InvalidPermissionResponse(r, permissions_.ProjectPermissions.VIEW)
        elif r.status_code == 404:
            return responses.NotFoundResponse(r)
        else:
            return responses.UnexpectedErrorResponse(r)
    
    def edit(self, name:str=None, permissions:dict[int, permissions_.ProjectPermissions]=None, **fields):
        "Edit this Project's attributes (e.g. name, permissions)."
        fields["name"] = name
        fields["permissions"] = {id:perm.value for id, perm in permissions.items()}
        r = self.session._s.post(f"{self.session.host}/project/edit", data={
            "name":self.name,
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
            if r.text.startswith("Already a Project"):
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
        

    def delete(self):
        "Delete this Project and all of its Profiles."
        r = self.session._s.delete(f"{self.session.host}/project/delete?name={sessions._param(self.name)}")
        if r.status_code == 200:
            self.session._cached.pop(self.id, None)
            return responses.SuccessResponse(r)
        elif r.status_code == 403:
            return responses.InvalidPermissionResponse(r, permissions_.ProjectPermissions.DELETE)
        elif r.status_code == 404:
            return responses.NotFoundResponse(r)
        else:
            return responses.UnexpectedErrorResponse(r)
        

    def get_profile(self, name:str):
        "Get a Profile belonging to this Project."
        r = self.session._s.get(f"{self.session.host}/project/profile/get?name={sessions._param(self.name)}&profile_name={sessions._param(name)}")
        if r.status_code == 200:
            data = r.json()
            id = sessions._b64_id(data["id"])
            if id in self.session._cached:
                prof = self.session._cached[id]
                prof._from_data(data)
            else:
                prof = self.session._cached[id] = profiles.Profile.from_data(data, self, self.session)
            return responses.ProfileResponse(r, [prof])
        elif r.status_code == 403:
            return responses.InvalidPermissionResponse(r, permissions_.ProjectPermissions.VIEW)
        elif r.status_code == 404 and "Profile" in r.text:
            return responses.NotFoundResponse(r)
        else:
            return responses.UnexpectedErrorResponse(r)
        
    def get_all_profiles(self):
        "Get all Profiles belonging to this Project."
        r = self.session._s.get(f"{self.session.host}/project/profile/all?name={sessions._param(self.name)}")
        if r.status_code == 200:
            return responses.ProfileResponse(r, [profiles.Profile.from_data(data, self, self.session) for data in r.json()])
        elif r.status_code == 403:
            return responses.InvalidPermissionResponse(r, permissions_.ProjectPermissions.VIEW)
        else:
            return responses.UnexpectedErrorResponse(r)
        
    def add_profile(self, name:str, permissions:dict[int, permissions_.ProfilePermissions]=None, **fields):
        "Add a Profile to this Project."
        fields["permissions"] = None if permissions is None else {auth_id:perm for auth_id, perm in permissions.items()}
        r = self.session._s.post(f"{self.session.host}/project/profile/add", data={
            "name":self.name,
            "profile_name":name,
            "fields":json.dumps(fields)
        })
        if r.status_code == 200:
            return responses.SuccessResponse(r)
        elif r.status_code == 400:
            return responses.InvalidInputResponse(r)
        elif r.status_code == 401:
            return responses.InvalidAuthResponse(r)
        elif r.status_code == 403:
            if r.text.startswith("Already a Profile"):
                return responses.AlreadyExistsResponse(r)
            else:
                return responses.InvalidInputResponse(r)
        else:
            return responses.UnexpectedErrorResponse(r)
        
    def remove_profile(self, name:str):
        "Remove the Profile with the given name from this Project."
        r = self.session._s.post(f"{self.session.host}/project/profile/remove?name={sessions._param(self.name)}&profile_name={sessions._param(name)}")
        if r.status_code == 200:
            return responses.SuccessResponse(r)
        elif r.status_code == 403:
            return responses.InvalidPermissionResponse(r, permissions_.ProjectPermissions.DELETE)
        elif r.status_code == 404 and "Profile" in r.text:
            return responses.NotFoundResponse(r)
        else:
            return responses.UnexpectedErrorResponse(r)