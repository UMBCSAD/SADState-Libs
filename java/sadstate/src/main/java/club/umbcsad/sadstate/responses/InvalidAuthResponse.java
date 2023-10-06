package club.umbcsad.sadstate.responses;

import java.net.http.HttpResponse;

public class InvalidAuthResponse extends ErrorResponse {
    public InvalidAuthResponse(HttpResponse<byte[]> response) {
        super(response);
    }
}
