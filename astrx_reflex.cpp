#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "{\"error\": \"No input provided\"}" << std::endl;
        return 1;
    }

    std::string input = argv[1];
    std::string lower = input;
    std::transform(lower.begin(), lower.end(), lower.begin(), ::tolower);

    std::string emotion = "neutral";
    double intensity = 0.0;
    std::vector<std::string> keywords;

    if (lower.find("tired") != std::string::npos ||
        lower.find("alone") != std::string::npos ||
        lower.find("empty") != std::string::npos ||
        lower.find("sad") != std::string::npos) {
        emotion = "sad";
        intensity = 0.7;
    }

    if (lower.find("angry") != std::string::npos ||
        lower.find("mad") != std::string::npos ||
        lower.find("furious") != std::string::npos) {
        emotion = "angry";
        intensity = 0.8;
    }

    // Simple keyword extraction
    std::vector<std::string> possible = {"tired", "alone", "empty", "sad", "angry", "mad", "furious"};
    for (auto& w : possible) {
        if (lower.find(w) != std::string::npos) {
            keywords.push_back(w);
        }
    }

    json output;
    output["emotion"] = emotion;
    output["intensity"] = intensity;
    output["keywords"] = keywords;

    std::cout << output.dump() << std::endl;
    return 0;
}