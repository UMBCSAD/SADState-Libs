package club.umbcsad.sadstate.responses;

import java.net.http.HttpResponse;

public class AuthResponse extends SuccessResponse {

    public static AuthResponse fromHttpResponse(HttpResponse<byte[]> response) {
        String toParse = new String(response.body());
        long parsed = Long.parseLong(toParse);
        return new AuthResponse(response, parsed);
    }

    private long authID;
    
    public AuthResponse(HttpResponse<byte[]> response, long authID) {
        super(response);
        this.authID = authID;
    }

    public long getAuthID() { return authID; }

}
