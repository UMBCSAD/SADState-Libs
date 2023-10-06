package club.umbcsad.sadstate.permissions;

public class ProjectPermissions implements Permission {
    public static final int EDIT            = 0b000001;
    public static final int DELETE          = 0b000010;
    public static final int VIEW            = 0b000100;
    public static final int ADD_PROFILE     = 0b001000;
    public static final int EDIT_PROFILE    = 0b010000;
    public static final int REMOVE_PROFILE  = 0b100000;

    public static final String[] names = {"EDIT", "DELETE", "VIEW", "ADD_PROFILE", "EDIT_PROFILE", "REMOVE_PROFILE"};
    public static final int[] values = {EDIT, DELETE, VIEW, ADD_PROFILE, EDIT_PROFILE, REMOVE_PROFILE};

    private static String generateName(int value) {
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < names.length; i++)
            if ((value & values[i]) != 0)
                builder.append(names[i]);

        return String.join(" | ", builder);
        
    }

    private final int value;
    private final String name;

    public ProjectPermissions(int value) {
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

    public ProjectPermissions OR(ProjectPermissions other) {
        return new ProjectPermissions(value | other.value);
    }

    public ProjectPermissions AND(ProjectPermissions other) {
        return new ProjectPermissions(value & other.value);
    }

    public ProjectPermissions XOR(ProjectPermissions other) {
        return new ProjectPermissions(value ^ other.value);
    }

}
