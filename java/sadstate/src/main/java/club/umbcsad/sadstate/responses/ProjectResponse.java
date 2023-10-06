package club.umbcsad.sadstate.responses;

import java.net.http.HttpResponse;

import club.umbcsad.sadstate.Project;

public class ProjectResponse extends SuccessResponse {

    private Project project;

    public ProjectResponse(HttpResponse<byte[]> response, Project project) {
        super(response);
        this.project = project;
    }

    public Project getProject() { return project; }
}
