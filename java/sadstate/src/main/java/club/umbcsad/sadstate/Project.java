package club.umbcsad.sadstate;

import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

import club.umbcsad.sadstate.exceptions.OutOfDateException;
import club.umbcsad.sadstate.permissions.ProjectPermissions;
import club.umbcsad.sadstate.responses.ExceptionResponse;
import club.umbcsad.sadstate.responses.InvalidPermissionResponse;
import club.umbcsad.sadstate.responses.NotFoundResponse;
import club.umbcsad.sadstate.responses.Response;
import club.umbcsad.sadstate.responses.SuccessResponse;
import club.umbcsad.sadstate.responses.UnexpectedErrorResponse;
import club.umbcsad.sadstate.util.IDParser;


public class Project {
    
    public static Project fromData(Map<String, Object> data) {
        Project project = new Project(0, null, null, null);
        project.id = IDParser.parseLong((String)data.get("id"));
        project.updateData(data);
        return project;
    }

    private long id;
    private String name;
    private Map<Long, ProjectPermissions> permissions;
    private Session session;

    public Project(long id, String name, Map<Long, ProjectPermissions> permissions, Session session) {
        this.id = id;
        this.name = name;
        this.permissions = permissions;
        this.session = session;
    }

    public Project(long id, String name, Session session) {
        this(id, name, new HashMap<Long, ProjectPermissions>(), session);
    }

    @SuppressWarnings("unchecked")
     public void updateData(Map<String, Object> data) {
        name = (String)data.get("name");

        permissions = new HashMap<Long, ProjectPermissions>();
        Map<String, Object> gotPermissions = (Map<String, Object>)data.get("permissions");
        if (gotPermissions != null) {
            for (String key : gotPermissions.keySet())
                permissions.put(Long.parseLong(key), new ProjectPermissions((int)gotPermissions.get(key)));
        }
    }

    public long getId() { return id; }
    public String getName() { return name; }
    public Map<Long, ProjectPermissions> getPermissions() { return permissions; }
    public Session getSession() { return session; }

    @SuppressWarnings("unchecked")
    public Response update() throws OutOfDateException {
        HttpResponse<byte[]> r;
        try {
            r = session.getClient().send(
                HttpRequest.newBuilder()
                           .uri(new URI(session.getHost()+"/project/get?name="+URLEncoder.encode(name, StandardCharsets.UTF_8)))
                           .GET()
                           .build(),
                HttpResponse.BodyHandlers.ofByteArray()
            );
        }
        catch (Exception e) {
            return new ExceptionResponse(e);
        }

        if (r.statusCode() == 200) {
            Map<String, Object> data;
            try {
                data = session.getJsonParser().readValue(r.body(), HashMap.class);
            }
            catch (Exception e) {
                return new ExceptionResponse(r, e);
            }
            long id = IDParser.parseLong((String)data.get("id"));
            //name has changed
            if (id != this.id) {
                if (session.getProjectCache().containsKey(this.id))
                    session.getProjectCache().remove(this.id);
                throw new OutOfDateException("Project \""+name+"\" has changed its name.");
            }
            updateData(data);
            return new SuccessResponse(r);
        }
        else if (r.statusCode() == 403)
            return new InvalidPermissionResponse(r, new ProjectPermissions(ProjectPermissions.VIEW));
        else if (r.statusCode() == 404)
            return new NotFoundResponse(r);
        else
            return new UnexpectedErrorResponse(r);
    }
}
