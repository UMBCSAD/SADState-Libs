package club.umbcsad.sadstate.responses;

import java.net.http.HttpResponse;

public class AlreadyExistsResponse extends ErrorResponse {
    public AlreadyExistsResponse(HttpResponse<byte[]> response) {
        super(response);
    }
}
