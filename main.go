package main

import (
	"encoding/json"
	"log"
	"net/http"
	"sync"
)

type StateSnapshot struct {
	Mood   float64            `json:"mood"`
	Traits map[string]float64 `json:"traits"`
}

type AstryxSnapshot struct {
	AgentName     string         `json:"agent_name"`
	IdentityReason string        `json:"identity_reason"`
	UserInput     string         `json:"user_input"`
	Perception    any            `json:"perception"`
	Goal          string         `json:"goal"`
	Plan          any            `json:"plan"`
	Reply         string         `json:"reply"`
	StateSnapshot StateSnapshot  `json:"state_snapshot"`
}

var (
	mu        sync.Mutex
	history   []AstryxSnapshot
)

func ingestHandler(w http.ResponseWriter, r *http.Request) {
	var snap AstryxSnapshot
	if err := json.NewDecoder(r.Body).Decode(&snap); err != nil {
		http.Error(w, "bad json", http.StatusBadRequest)
		return
	}
	mu.Lock()
	history = append(history, snap)
	mu.Unlock()
	w.WriteHeader(http.StatusNoContent)
}

func summaryHandler(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()

	type Summary struct {
		Count      int                `json:"count"`
		AvgMood    float64            `json:"avg_mood"`
		GoalCounts map[string]int     `json:"goal_counts"`
	}
	s := Summary{
		Count:      len(history),
		GoalCounts: map[string]int{},
	}

	if len(history) > 0 {
		var moodSum float64
		for _, h := range history {
			moodSum += h.StateSnapshot.Mood
			s.GoalCounts[h.Goal]++
		}
		s.AvgMood = moodSum / float64(len(history))
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(s)
}

func main() {
	http.HandleFunc("/ingest", ingestHandler)
	http.HandleFunc("/summary", summaryHandler)

	log.Println("Go hub listening on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}