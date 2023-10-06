package club.umbcsad.sadstate.util;

import java.math.BigInteger;
import java.util.Base64;

public final class IDParser {

    public static byte[] decode(String value) {
        return Base64.getDecoder().decode(value);
    }

    public static long parseLong(byte[] value) {
        byte[] reversed = new byte[value.length];
        for (int i = 0; i < reversed.length; i++)
            reversed[i] = value[value.length - 1 - i];
        return new BigInteger(value).longValue();
    }

    public static long parseLong(String value) {
        return parseLong(decode(value));
    }
}