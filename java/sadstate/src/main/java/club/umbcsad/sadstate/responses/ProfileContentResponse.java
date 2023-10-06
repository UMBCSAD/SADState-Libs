package club.umbcsad.sadstate.responses;

import java.net.http.HttpResponse;

public class ProfileContentResponse extends SuccessResponse {

    public ProfileContentResponse(HttpResponse<byte[]> response) {
        super(response);
    }
    
}
