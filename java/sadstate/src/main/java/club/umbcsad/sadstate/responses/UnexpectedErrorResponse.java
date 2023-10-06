package club.umbcsad.sadstate.responses;

import java.net.http.HttpResponse;

public class UnexpectedErrorResponse extends ErrorResponse {
    public UnexpectedErrorResponse(HttpResponse<byte[]> response) {
        super(response);
    }
}
