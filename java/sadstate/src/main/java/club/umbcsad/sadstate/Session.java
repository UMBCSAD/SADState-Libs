package club.umbcsad.sadstate;

import java.net.CookieManager;
import java.net.CookiePolicy;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpClient.Redirect;
import java.nio.charset.StandardCharsets;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.HashMap;
import java.util.Map;

import com.fasterxml.jackson.databind.ObjectMapper;

import club.umbcsad.sadstate.permissions.ProjectPermissions;
import club.umbcsad.sadstate.responses.*;
import club.umbcsad.sadstate.util.IDParser;
import club.umbcsad.sadstate.util.MultipartFormBuilder;

class Session {

    private String host;
    private long authID;
    private HttpClient client;
    private Map<Long, Project> projectCache;
    private Map<Long, Profile> profileCache;
    private ObjectMapper jsonParser;


    public Session(String host) {
        this.host = host;
        authID = 0; //0 == null in this case
        client = HttpClient.newBuilder()
                           .cookieHandler(new CookieManager(null, CookiePolicy.ACCEPT_ORIGINAL_SERVER))
                           .followRedirects(Redirect.NORMAL)
                           .build();
        projectCache = new HashMap<Long, Project>();
        profileCache = new HashMap<Long, Profile>();
        jsonParser = new ObjectMapper();
    }

    public HttpClient getClient() { return client; }
    public String getHost() { return host; }
    public long getAuthID() { return authID; }
    public boolean isAuthenticated() { return authID != 0; }
    public ObjectMapper getJsonParser() { return jsonParser; }
    public Map<Long, Project> getProjectCache() { return projectCache; }
    public Map<Long, Profile> getProfileCache() { return profileCache; }

    public void clearCache() {
        projectCache.clear();
        profileCache.clear();

    }

    public Response newAuth(String password) {
        HttpResponse<byte[]> r;
        try {
            MultipartFormBuilder builder = new MultipartFormBuilder().addPart("password", password);
            r = client.send(
                HttpRequest.newBuilder()
                           .uri(new URI(host + "/auth/new"))
                           .headers("Content-Type", "multipart/form-data")
                           .POST(HttpRequest.BodyPublishers.ofByteArray(builder.build()))
                           .build(),
                HttpResponse.BodyHandlers.ofByteArray()
            );
        }
        catch (Exception e) {
            return new ExceptionResponse(e);
        }

        if (r.statusCode() == 200) {
            AuthResponse resp = AuthResponse.fromHttpResponse(r);
            if (resp.getAuthID() != authID)
                clearCache();
            authID = resp.getAuthID();
            return resp;
        }
        else if (r.statusCode() == 400)
            return new InvalidInputResponse(r);
        else
            return new UnexpectedErrorResponse(r);
    }

    public Response authenticate(int id, String password) {
        //TODO
        return null;
    }

    @SuppressWarnings("unchecked")
    public Response getProject(String name) {
        HttpResponse<byte[]> r;
        try {
            r = client.send(
                HttpRequest.newBuilder()
                           .uri(new URI(host + "/project/get/name?name="+URLEncoder.encode(name, StandardCharsets.UTF_8)))
                           .GET()
                           .build(),
                HttpResponse.BodyHandlers.ofByteArray()
            );
        }
        catch (Exception e) {
            return new ExceptionResponse(e);
        }

        if (r.statusCode() == 200) {
            HashMap<String, Object> data;
            try {
                data = jsonParser.readValue(r.body(), HashMap.class);
            }
            catch (Exception e) {
                return new ExceptionResponse(r, e);
            }

            Project project;
            long id = IDParser.parseLong((String)data.get("id"));
            if (projectCache.containsKey(id)) {
                project = projectCache.get(id);
                project.updateData(data);
            }
            else {
                project = Project.fromData(data);
                projectCache.put(id, project);
            }
            return new ProjectResponse(r, project);
        }
        else if (r.statusCode() == 403)
            return new InvalidPermissionResponse(r, new ProjectPermissions(ProjectPermissions.VIEW));
        else if (r.statusCode() == 404)
            return new NotFoundResponse(r);
        else
            return new UnexpectedErrorResponse(r);
    }

    public Response registerProject(String name, Map<String, Object> fields) {
        //TODO
        return null;
    }

}