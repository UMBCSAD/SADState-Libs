package club.umbcsad.sadstate.responses;

import java.net.http.HttpResponse;

public class SuccessResponse extends Response {
    public SuccessResponse(HttpResponse<byte[]> response) {
        super(response);
    }
}
