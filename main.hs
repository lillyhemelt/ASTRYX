{-# LANGUAGE OverloadedStrings #-}

import Data.Aeson
import qualified Data.ByteString.Lazy as B
import qualified Data.HashMap.Strict as HM
import qualified Data.Text as T
import System.Environment (getArgs)

data Snapshot = Snapshot
  { mood :: Double
  , traits :: HM.HashMap T.Text Double
  , goal :: T.Text
  } deriving Show

instance FromJSON Snapshot where
  parseJSON = withObject "Snapshot" $ \o -> do
    state <- o .: "state_snapshot"
    mood <- state .: "mood"
    traits <- state .: "traits"
    goal <- o .: "goal"
    return $ Snapshot mood traits goal

data Result = Result
  { warnings :: [T.Text]
  , suggestions :: HM.HashMap T.Text Double
  }

instance ToJSON Result where
  toJSON (Result w s) =
    object [ "warnings" .= w
           , "suggestions" .= s
           ]

main :: IO ()
main = do
  args <- getArgs
  case args of
    [path] -> do
      content <- B.readFile path
      let snap = decode content :: Maybe Snapshot
      case snap of
        Nothing -> putStrLn "{\"error\": \"bad json\"}"
        Just s  -> B.putStr $ encode $ analyze s
    _ -> putStrLn "{\"error\": \"usage: astryx-logic <file.json>\"}"

analyze :: Snapshot -> Result
analyze (Snapshot mood traits goal) =
  let warns = concat
        [ if mood < -0.6 then ["Mood too low"] else []
        , if goal == "comfort" && mood > 0.5 then ["Comfort used while mood high"] else []
        ]
      suggs = HM.fromList
        [ ("caution", 0.7) | mood < -0.6 ]
  in Result warns suggs