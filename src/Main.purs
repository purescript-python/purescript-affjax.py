module Main where

import Prelude
import Affjax as AX
import Affjax.ResponseFormat as ResponseFormat
import Data.Argonaut.Core as J
import Data.Either (Either(..))
import Data.HTTP.Method (Method(..))
import Effect.Aff (launchAff)
import Effect.Class.Console (log)

main =
  void $ launchAff
    $ do
        result <- AX.request (AX.defaultRequest { url = "/api", method = Left GET, responseFormat = ResponseFormat.json })
        case result of
          Left err -> log $ "GET /api response failed to decode: " <> AX.printError err
          Right response -> log $ "GET /api response: " <> J.stringify response.body
