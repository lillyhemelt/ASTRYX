package astryx.spine;

public class AstryxIdentity {
    private final String name;
    private final String originReason;
    private final String purpose;

    public AstryxIdentity(String name, String originReason, String purpose) {
        this.name = name;
        this.originReason = originReason;
        this.purpose = purpose;
    }

    public String getName() {
        return name;
    }

    public String getOriginReason() {
        return originReason;
    }

    public String getPurpose() {
        return purpose;
    }
}