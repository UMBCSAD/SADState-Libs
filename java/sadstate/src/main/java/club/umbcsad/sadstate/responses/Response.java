package club.umbcsad.sadstate.responses;

import java.net.http.HttpResponse;

public class Response {
    protected HttpResponse<byte[]> response;

    public Response(HttpResponse<byte[]> response) {
        this.response = response;
    }

    public HttpResponse<byte[]> getHttpResponse() { return response; }
    public int getCode() { return response.statusCode(); }
    public boolean isOk() { return response.statusCode() < 400; }
    public byte[] getContent() { return response.body(); }
}
