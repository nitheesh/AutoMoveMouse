#!/bin/bash

####### Bash script to change mouse position while screen goes idle. ######
### _author : Nitheesh .CS (nitheesh.cs007@gmail.com) ###
### _version : 0.1 ####

function MoveMouse () {
    xx=$[ 150 + $[ RANDOM % 10 ]]
    yy=$[ 150 + $[ RANDOM % 10 ]]
    xte "mousermove $xx $yy"
    sleep 1
    xx=$[ 130 + $[ RANDOM % 10 ]]
    yy=$[ 130 + $[ RANDOM % 10 ]]
    xte "mousermove -$xx -$yy"
    
    echo "Changing window"
    xte 'keydown Alt_L' 'key Tab' && sleep 2 && xte 'keyup Alt_L'
    sleep 2
    echo "Reverting to terminal window"
    xte 'keydown Alt_L' 'key Tab' && sleep 2 && xte 'keyup Alt_L'
}  

while true;
  do
    idle=`expr $(xprintidle) / 1000`
    echo "$idle seconds idle";
    if [ $idle -gt "20" ]; then
      echo "Starting mouse change"
      MoveMouse
    fi
    sleep 5
  done  
