package club.umbcsad.sadstate.responses;

import java.net.http.HttpResponse;

public class RemainingSpaceResponse extends SuccessResponse {

    public static RemainingSpaceResponse fromHttpResponse(HttpResponse<byte[]> response) {
        String toParse = new String(response.body());
        int parsed = Integer.parseInt(toParse);
        return new RemainingSpaceResponse(response, parsed);
    }

    private int numBytes;

    public RemainingSpaceResponse(HttpResponse<byte[]> response, int numBytes) {
        super(response);
        this.numBytes = numBytes;
    }

    public int getNumBytes() { return numBytes; }
}
