package astryx.spine;

import java.util.Map;

public class AstryxSnapshot {
    public String agent_name;
    public String identity_reason;
    public String user_input;
    public Map<String, Object> perception;
    public String goal;
    public Map<String, Object> plan;
    public String reply;
    public StateSnapshot state_snapshot;

    public static class StateSnapshot {
        public double mood;
        public Map<String, Double> traits;
    }
}