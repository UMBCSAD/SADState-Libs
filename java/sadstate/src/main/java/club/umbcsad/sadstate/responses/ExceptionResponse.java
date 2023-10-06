package club.umbcsad.sadstate.responses;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.net.http.HttpResponse;

public class ExceptionResponse extends Response {

    private Exception exception;

    public ExceptionResponse(HttpResponse<byte[]> response, Exception exception) {
        super(response);
        this.exception = exception;
    }

    public ExceptionResponse(Exception exception) {
        this(null, exception);
    }

    @Override
    public int getCode() { return 600; }
    @Override
    public byte[] getContent() {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        exception.printStackTrace(new PrintStream(out));
        return out.toByteArray();
    }

}
