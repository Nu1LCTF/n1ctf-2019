{-# LANGUAGE OverloadedStrings #-}
module GetFlag ( isFlag ) where

import Data.Bits ( testBit, shiftL )
import Data.Char ( ord )
import Data.List ( isInfixOf, isPrefixOf, isSuffixOf, transpose )
import Debug.Trace ( traceShow )

-- call to this function will check whether the flag is correct
isFlag :: String -> Bool
isFlag f = or [isFlag1 f, isFlag2 f]

-- decoy, don't be too harsh here.
isFlag1 :: String -> Bool
isFlag1 f = and [
  (length f) <= 40,
  and $ map (\x -> (ord x) <= 256) f,
  "FLAG" `isInfixOf` f,
  (sum $ map ord f) >= 23333
                ]

substr :: Int -> Int -> [a] -> [a]
substr from to list = drop from $ take to list 

reform :: [(Int, [Int])] -> [Int]
reform v = map sum $ transpose $ map lifted v
  where
    lifted (x, bits) = map (\bit -> shiftL bit x) bits

reformSeq :: [Int]
reformSeq = [0, 2, 7, 5, 3, 1, 4, 6]

-- real flag checker
isFlag2 :: String -> Bool
isFlag2 f = and $ map (\x -> x f) [check1, check2, check3, check4]
  where
    check1 f = (length f) == 39
    check2 f = "N1CTF{" `isPrefixOf` f
    check3 f = "}" `isSuffixOf` f
    flag_inner f = substr 6 38 f
    takeBits idx f = map (\x -> fromEnum $ testBit x idx) $ map ord f
    all_bits f = map (\x -> takeBits x (flag_inner f)) [0..7]
    reformed f = reform $ zip reformSeq $ all_bits f
    check4 f = (reformed f) == [42,147,146,43,19,14,147,43,143,142,10,19,139,10,42,147,23,22,15,10,143,147,43,43,15,11,138,143,147,43,43,19]

