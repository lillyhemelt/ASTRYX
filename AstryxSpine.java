package astryx.spine;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.DeserializationFeature;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.stream.Stream;

public class AstryxSpine {

    private final AstryxIdentity identity;
    private final AstryxMemory memory;
    private final ObjectMapper mapper;

    public AstryxSpine(AstryxIdentity identity) {
        this.identity = identity;
        this.memory = new AstryxMemory();
        this.mapper = new ObjectMapper()
                .configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
    }

    public void ingestLogFile(Path logPath) throws IOException {
        if (!Files.exists(logPath)) return;

        try (Stream<String> lines = Files.lines(logPath)) {
            lines.forEach(line -> {
                try {
                    AstryxSnapshot snapshot = mapper.readValue(line, AstryxSnapshot.class);
                    memory.addSnapshot(snapshot);
                } catch (IOException e) {
                    // ignore malformed lines
                }
            });
        }
    }

    public String summarizeState() {
        StringBuilder sb = new StringBuilder();
        sb.append("=== ASTRYX SPINE SUMMARY ===\n");
        sb.append("Identity: ").append(identity.getName()).append("\n");
        sb.append("Origin: ").append(identity.getOriginReason()).append("\n");
        sb.append("Purpose: ").append(identity.getPurpose()).append("\n");
        sb.append("Total interactions: ").append(memory.size()).append("\n");
        sb.append("Average mood: ").append(String.format("%.2f", memory.averageMood())).append("\n");
        sb.append("Goal frequencies: ").append(memory.goalFrequencies()).append("\n");
        return sb.toString();
    }

    public static AstryxSpine defaultSpine() {
        AstryxIdentity id = new AstryxIdentity(
                "ASTRYX",
                "A self-correcting star map—constantly recalculating itself based on drift, error, and new information.",
                "To evolve through heuristic decision-making, maintain coherence through structure, and refine itself through continuous self-analysis."
        );
        return new AstryxSpine(id);
    }

    public static void main(String[] args) throws Exception {
        AstryxSpine spine = AstryxSpine.defaultSpine();
        Path logPath = Path.of("astrx_log.jsonl");

        spine.ingestLogFile(logPath);

        System.out.println(spine.summarizeState());
    }
}