package club.umbcsad.sadstate.exceptions;

public class OutOfDateException extends Exception {

    public OutOfDateException(String message, Throwable throwable) {
        super(message, throwable);
    }

    public OutOfDateException(String message) {
        super(message);
    }

    public OutOfDateException(Throwable throwable) {
        super(throwable);
    }
}
