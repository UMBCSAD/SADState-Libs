package club.umbcsad.sadstate.permissions;

public final class ProfilePermissions implements Permission {
    public static final int READ    = 0b001;
    public static final int WRITE   = 0b010;
    public static final int EDIT    = 0b100;

    public static final String[] names = {"READ", "WRITE", "EDIT"};
    public static final int[] values = {READ, WRITE, EDIT};

    private static String generateName(int value) {
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < names.length; i++)
            if ((value & values[i]) != 0)
                builder.append(names[i]);

        return String.join(" | ", builder);
        
    }

    private final int value;
    private final String name;

    public ProfilePermissions(int value) {
        this.value = value;
        name = generateName(value);
    }

    @Override
    public String toString() {
        //https://www.baeldung.com/java-object-memory-address
        return ProfilePermissions.class.getSimpleName() + " \"" + getName() + "\"@" + Integer.toHexString(hashCode());
    }

    public int getFlag() { return value; }

    public String getName() { return name; }

    public ProfilePermissions OR(ProfilePermissions other) {
        return new ProfilePermissions(value | other.value);
    }

    public ProfilePermissions AND(ProfilePermissions other) {
        return new ProfilePermissions(value & other.value);
    }

    public ProfilePermissions XOR(ProfilePermissions other) {
        return new ProfilePermissions(value ^ other.value);
    }

}
