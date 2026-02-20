using System.Collections.Generic;

namespace ASTRYX.Dashboard.Models
{
    public class AstryxSnapshot
    {
        public string agent_name { get; set; }
        public string identity_reason { get; set; }
        public string user_input { get; set; }
        public Dictionary<string, object> perception { get; set; }
        public string goal { get; set; }
        public Dictionary<string, object> plan { get; set; }
        public string reply { get; set; }
        public StateSnapshot state_snapshot { get; set; }
    }

    public class StateSnapshot
    {
        public double mood { get; set; }
        public Dictionary<string, double> traits { get; set; }
    }
}