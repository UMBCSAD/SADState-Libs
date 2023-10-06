package club.umbcsad.sadstate.responses;

import java.net.http.HttpResponse;

public class ErrorResponse extends Response {
    public ErrorResponse(HttpResponse<byte[]> response) {
        super(response);
    }

    public String getReason() {
        return new String(getContent());
    }
}
