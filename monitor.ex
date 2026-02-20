defmodule Monitor do
  def analyze(snapshot) do
    mood = snapshot["state_snapshot"]["mood"]

    warnings =
      cond do
        mood < -0.7 -> ["critical_mood_drop"]
        true -> []
      end

    %{warnings: warnings}
  end

  def main do
    {:ok, input} = IO.read(:stdio, :all) |> Jason.decode()
    result = analyze(input)
    IO.puts(Jason.encode!(result))
  end
end