{-
Welcome to a Spago project!
You can edit this file as you like.
-}
{ name = "purescript-aff"
, dependencies = [ "aff", "console", "effect", "psci-support", "affjax" ]
, packages = ./packages.dhall
, sources = [ "src/**/*.purs"]
, backend = "pspy"
}
