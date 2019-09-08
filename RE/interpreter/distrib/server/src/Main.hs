{-# LANGUAGE OverloadedStrings, ScopedTypeVariables #-}
module Main where

import GHC
import GHC.Paths ( libdir )
import HscTypes
import CorePrep ( corePrepPgm )
import DynFlags
import TyCon ( isDataTyCon )
import qualified GHC.LanguageExtensions as LangExt
import ByteCodeGen ( byteCodeGen )

import Data.List ( isPrefixOf )
import Control.Exception ( try, SomeException(..) )
import Control.Monad.Trans ( liftIO, MonadIO(..) )
import System.Console.Haskeline

import GetFlag ( isFlag )

initSession :: IO HscEnv
initSession = runGhc (Just libdir) $ do
  dyn <- getSessionDynFlags
  let dyn' = dyn { hscTarget = HscInterpreted , ghcLink = LinkInMemory } `xopt_set` LangExt.ExtendedDefaultRules
  setSessionDynFlags dyn'
  setContext [ IIDecl $ simpleImportDecl (mkModuleName "Prelude") ]
  env <- getSession
  return env

disassemble :: HscEnv -> FilePath -> IO () 
disassemble sess path = runGhc (Just libdir) $ do
  setSession sess   -- use the initialized session instead of the current one
  dyn <- getSessionDynFlags
  let dyn' = dyn `dopt_set` Opt_D_dump_BCOs   -- this will dump protoBCOs while generating bytecode
  setSessionDynFlags dyn'

  target <- guessTarget path Nothing
  setTargets [target]
  load LoadAllTargets

  modsum <- getModSummary $ mkModuleName "Toplevel"
  dmod <- parseModule modsum >>= typecheckModule >>= desugarModule
  let core = coreModule dmod

  let data_tycons = filter isDataTyCon (mg_tcs core)
  sess <- getSession
  (prepd_binds, _) <- liftIO $ corePrepPgm sess (mg_module core) (ms_location modsum) (mg_binds core) data_tycons
  _ <- liftIO $ byteCodeGen sess (mg_module core) prepd_binds data_tycons (mg_modBreaks core)

  return () 


ghcCatch :: MonadIO m => IO a -> m (Maybe a)
ghcCatch m = liftIO $ do
  mres <- try m
  case mres of
    Left (err :: SomeException) -> do
      return Nothing
    Right res -> return (Just res)

action :: HscEnv -> InputT IO ()
action sess = do
  inp <- getInputLine "$ "
  case inp of
    Nothing -> do return ()
    Just input | "exit" `isPrefixOf` input -> do
      outputStrLn "Bye!"
    Just input | "disasm" `isPrefixOf` input -> do
      let modpath = (last $ words input) :: FilePath
      _ <- ghcCatch $ disassemble sess modpath
      action sess
    Just input | "checkFlag" `isPrefixOf` input -> do
      let flag = last $ words input
      _ <- case isFlag flag of
        True -> outputStrLn "Correct!"
        False -> outputStrLn "Wrong!"
      action sess
    Just input -> do
      outputStrLn "Invalid input."
      action sess

main :: IO ()
main = do
  sess <- initSession
  runInputT defaultSettings (action sess)

