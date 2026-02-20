import express from "express";
import { WebSocketServer } from "ws";
import fs from "fs";

const app = express();
app.use(express.json());

let history = [];

app.post("/ingest", (req, res) => {
  const snap = req.body;
  history.push(snap);

  // broadcast to websocket clients
  wss.clients.forEach(client => {
    if (client.readyState === 1) {
      client.send(JSON.stringify(snap));
    }
  });

  res.sendStatus(204);
});

app.get("/summary", (req, res) => {
  const moods = history.map(h => h.state_snapshot.mood);
  const avgMood = moods.length ? moods.reduce((a,b)=>a+b)/moods.length : 0;

  const goals = {};
  history.forEach(h => goals[h.goal] = (goals[h.goal] || 0) + 1);

  res.json({
    count: history.length,
    avgMood,
    goals
  });
});

const server = app.listen(3000, () => {
  console.log("Node gateway running on port 3000");
});

const wss = new WebSocketServer({ server });