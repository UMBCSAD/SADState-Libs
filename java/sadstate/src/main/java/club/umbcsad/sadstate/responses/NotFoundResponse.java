package club.umbcsad.sadstate.responses;

import java.net.http.HttpResponse;

public class NotFoundResponse extends ErrorResponse {
    public NotFoundResponse(HttpResponse<byte[]> response) {
        super(response);
    }
}
