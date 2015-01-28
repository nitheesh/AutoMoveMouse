#!/bin/bash

####### Bash script to change mouse position while screen goes idle. ######
### _author : Nitheesh .CS (nitheesh.cs007@gmail.com) ###
### _version : 0.1 ####

function MoveMouse () {
    xx=$[ 150 + $[ RANDOM % 10 ]]
    yy=$[ 150 + $[ RANDOM % 10 ]]
    xte "mousermove $xx $yy"
    sleep 0.5
    xx=$[ 130 + $[ RANDOM % 10 ]]
    yy=$[ 130 + $[ RANDOM % 10 ]]
    xte "mousermove -$xx -$yy"
    
    #Generate a random number b/w 1 - 10 and sleep.
    randm=`echo $RANDOM % 10 + 1 | bc`
    echo "sleeping for " $randm
    sleep $randm
    echo "Changing to another window"
    #Get a random window
    _randWindw=`echo $RANDOM % 10 + 1 | bc`
    echo "random windw " $_randWindw
    xte 'keydown Alt_L' && for i in $(seq 1 $_randWindw); do sleep 0.5; xte 'key Tab'; done && xte 'keyup Alt_L'
}  

while true;
  do
    if [ ! -f /tmp/automove-stopped.do ]; then  
      idle=`expr $(xprintidle) / 1000`
      echo "$idle seconds idle";
      if [ $idle -gt "20" ]; then
        echo "Starting mouse movement and window change."
        MoveMouse
      fi
    else
      echo "Mouse move stopped..."  
    fi  
    sleep 5
  done  
