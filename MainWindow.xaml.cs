using System.Windows;
using ASTRYX.Dashboard.Models;

namespace ASTRYX.Dashboard
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            LoadData();
        }

        private void LoadData()
        {
            var snapshots = LogReader.LoadSnapshots("astrx_log.jsonl");
            if (snapshots.Count == 0)
                return;

            var last = snapshots[^1];

            MoodBar.Value = last.state_snapshot.mood;

            TraitsPanel.Children.Clear();
            foreach (var trait in last.state_snapshot.traits)
            {
                TraitsPanel.Children.Add(
                    new TextBlock { Text = $"{trait.Key}: {trait.Value:F2}", FontSize = 16 }
                );
            }

            ThoughtBlock.Text = last.plan["intention"].ToString();
        }
    }
}