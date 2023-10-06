package club.umbcsad.sadstate.responses;

import java.net.http.HttpResponse;

import club.umbcsad.sadstate.Profile;

public class ProfileResponse extends SuccessResponse {

    private Profile[] profiles;

    public ProfileResponse(HttpResponse<byte[]> response, Profile[] profiles) {
        super(response);
        this.profiles = profiles;
    }

    public Profile[] getProfiles() { return profiles; }
    public Profile getProfile() { return profiles.length > 0 ? profiles[0] : null; }

}
