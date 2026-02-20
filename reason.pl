:- [facts].

% interaction(Id, Emotion, Goal).

comfort_bias :-
    findall(G, interaction(_, _, G), Goals),
    include(=(comfort), Goals, Comforts),
    length(Goals, Total),
    length(Comforts, CCount),
    Total > 0,
    Ratio is CCount / Total,
    Ratio > 0.6.

frequent_sad_user :-
    findall(E, interaction(_, E, _), Emotions),
    include(=(sad), Emotions, Sads),
    length(Emotions, Total),
    length(Sads, SCount),
    Total > 0,
    Ratio is SCount / Total,
    Ratio > 0.5.