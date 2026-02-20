using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using ASTRYX.Dashboard.Models;

namespace ASTRYX.Dashboard
{
    public static class LogReader
    {
        public static List<AstryxSnapshot> LoadSnapshots(string path)
        {
            var list = new List<AstryxSnapshot>();

            if (!File.Exists(path))
                return list;

            foreach (var line in File.ReadLines(path))
            {
                try
                {
                    var snap = JsonSerializer.Deserialize<AstryxSnapshot>(line);
                    if (snap != null)
                        list.Add(snap);
                }
                catch { }
            }

            return list;
        }
    }
}