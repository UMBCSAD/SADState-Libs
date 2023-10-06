package club.umbcsad.sadstate.responses;

import java.net.http.HttpResponse;

public class InvalidInputResponse extends ErrorResponse {
    public InvalidInputResponse(HttpResponse<byte[]> response) {
        super(response);
    }
}
