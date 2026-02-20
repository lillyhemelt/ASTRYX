-module(router).
-export([main/0]).

main() ->
    {ok, Bin} = file:read_file("snapshot.json"),
    {ok, Snapshot} = jsx:decode(Bin),
    Mood = proplists:get_value(<<"mood">>, proplists:get_value(<<"state_snapshot">>, Snapshot)),
    Warnings = if Mood < -0.8 -> [<<"shutdown_risk">>]; true -> [] end,
    io:format("~s", [jsx:encode([{warnings, Warnings}])]).