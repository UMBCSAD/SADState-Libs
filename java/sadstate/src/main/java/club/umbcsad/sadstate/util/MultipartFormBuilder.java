package club.umbcsad.sadstate.util;

import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

//https://everything.curl.dev/http/multipart
//https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST

public class MultipartFormBuilder {
    public static final String BOUNDARY_PREFIX = "------------------------";
    public static final String BOUNDARY_POSTFIX = "--";

    private String boundary;
    private List<byte[]> data;

    public MultipartFormBuilder() {
        data = new ArrayList<byte[]>();
        boundary  = ((Integer)hashCode()).toString();
    }

    public MultipartFormBuilder addPart(String key, String value) {
        boundary += ((Integer)value.length()).toString();
        String element = "Content-Disposition: form-data; name=\":"+key+"\"\n\n"+value;
        data.add(element.getBytes(StandardCharsets.UTF_8));
        return this;
    }

    public MultipartFormBuilder addPart(String key, byte[] value) {
        boundary += ((Integer)value.length).toString();
        byte[] contentDispos = ("Content-Disposition: form-data; name=\":"+key+"\"\n\n").getBytes(StandardCharsets.UTF_8);
        byte[] element = new byte[contentDispos.length + value.length];
        System.arraycopy(contentDispos, 0, element, 0, contentDispos.length);
        System.arraycopy(value, 0, element, contentDispos.length, value.length);
        data.add(element);
        return this;
    }

    public MultipartFormBuilder addPart(String key, Object value) {
        return addPart(key, value.toString());
    }

    private int buildCopy(byte[] result, byte[] part, int currentLength) {
        System.arraycopy(part, 0, result, currentLength, part.length);
        return currentLength + part.length;
    }

    public byte[] build() {
        if (data.isEmpty()) return new byte[0];

        int totalLength = 0;
        for (byte[] b : data)
            totalLength += b.length;
        final byte[] boundaryBytes = ("\n"+boundary+"\n").getBytes(StandardCharsets.UTF_8);
        byte[] result = new byte[totalLength + data.size() * 2 + boundary.length() * (data.size() + 1) + BOUNDARY_POSTFIX.length()];
        
        //first boundary
        int currentLength = buildCopy(result, (boundary+"\n").getBytes(StandardCharsets.UTF_8), 0);

        for (int i = 0; i < data.size()-1; i++) {
            //copy part into result
            byte[] part = data.get(i);
            currentLength = buildCopy(result, part, currentLength);
            //copy boundary into result
            currentLength = buildCopy(result, boundaryBytes, currentLength);
        }

        //copy last part
        currentLength = buildCopy(result, data.get(data.size()-1), currentLength);
        //last boundary
        currentLength = buildCopy(result, ("\n"+boundary+BOUNDARY_POSTFIX).getBytes(StandardCharsets.UTF_8), currentLength);

        return result;
    }

}
