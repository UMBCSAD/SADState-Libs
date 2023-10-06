package club.umbcsad.sadstate.responses;

import java.net.http.HttpResponse;

import club.umbcsad.sadstate.permissions.Permission;

public class InvalidPermissionResponse extends ErrorResponse {

    private Permission permission;

    public InvalidPermissionResponse(HttpResponse<byte[]> response, Permission permission) {
        super(response);
        this.permission = permission;
    }

    public Permission getPermission() { return permission; }
}
