package astryx.spine;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class AstryxMemory {

    private final List<AstryxSnapshot> history = new ArrayList<>();

    public void addSnapshot(AstryxSnapshot snapshot) {
        history.add(snapshot);
    }

    public List<AstryxSnapshot> getHistory() {
        return history;
    }

    public int size() {
        return history.size();
    }

    public Map<String, Long> goalFrequencies() {
        return history.stream()
                .collect(Collectors.groupingBy(
                        s -> s.goal,
                        Collectors.counting()
                ));
    }

    public double averageMood() {
        if (history.isEmpty()) return 0.0;
        return history.stream()
                .mapToDouble(s -> s.state_snapshot != null ? s.state_snapshot.mood : 0.0)
                .average()
                .orElse(0.0);
    }
}