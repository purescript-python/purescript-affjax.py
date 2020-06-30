module Main where

import Prelude
import Affjax as AX
import Affjax.ResponseFormat as ResponseFormat
import Data.Argonaut.Core as J
import Data.Either (Either(..))
import Data.HTTP.Method (Method(..))
import Effect.Aff (launchAff)
import Effect.Class (liftEffect)
import Effect.Class.Console (log)

main =
  void $ launchAff
    $ do
        let
          r = AX.defaultRequest { url = "http://ip.jsontest.com/", method = Left GET, responseFormat = ResponseFormat.json }
        result <- AX.request r
        case result of
          Left err -> log $ "GET  response failed to decode: " <> AX.printError err
          Right response -> log $ "GET /api response: " <> J.stringify response.body
