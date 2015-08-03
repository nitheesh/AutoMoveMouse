#!/bin/bash

####### Bash script to change mouse position and automate apps while screen goes idle ###
### _author : Nitheesh .CS (nitheesh.cs007@gmail.com) ###
### _version : 0.1 ####

## Note : Please disable "Show desktop" option in Unity Alt+Tab switcher
## -- http://askubuntu.com/questions/167263/how-can-i-remove-show-desktop-from-the-alt-tab-application-switcher

Browsers="Firefox | Google-chrome-stable | Google-chrome | Google-chrome-unstable | Google-chrome-beta"
gedit="Gedit"
sublm="Sublime_text"
Max_Idle="5"

lockFile="/tmp/automouse.lck"

function MoveMouse () {
    # xx=$[ 150 + $[ RANDOM % 10 ]]
    # yy=$[ 150 + $[ RANDOM % 10 ]]
    # xte "mousermove $xx $yy"
    # sleep 0.5
    # xx=$[ 130 + $[ RANDOM % 10 ]]
    # yy=$[ 130 + $[ RANDOM % 10 ]]
    # xte "mousermove -$xx -$yy"
    
    #Generate a random number b/w 1 - 10 and sleep.
    randm=`echo $RANDOM % 10 + 1 | bc`
    echo "sleeping for " $randm
    sleep $randm
    echo "Changing to another window"
    #Get a random window
    _randWindw=`echo $RANDOM % 10 + 1 | bc`
    echo "random windw " $_randWindw
    xte 'keydown Alt_L' && for i in $(seq 1 $_randWindw); do sleep 0.5; xte 'key Tab'; done && xte 'keyup Alt_L'
    sleep 3;
    _curWindow=$(xprop -id $(xprop -root -f _NET_ACTIVE_WINDOW 0x " \$0\\n" _NET_ACTIVE_WINDOW | awk "{print \$2}") | awk '/WM_CLASS/{print $4}')
    echo $_curWindow
    _curWindow=`echo $_curWindow | tr -d '"'`

    _rand_Tab=$(shuf -i 3-8 -n 1)

    if ! GetIdle $1; then
      if grep -q $_curWindow <<<$Browsers; then
        if ! GetIdle $1; then
          xte 'keydown Control_L' && for i in $(seq 1 $_rand_Tab); do sleep 0.5; 
          xte 'key Tab'; done && xte 'keyup Control_L'
        fi  

      elif grep -q $_curWindow <<<$gedit; then
        for i in $(seq 1 $_rand_Tab); do sleep 1; 
        xte 'key Page_Down'; done

      elif grep -q $_curWindow <<<$sublm; then
        xte 'keydown Control_L' && for i in $(seq 1 $_rand_Tab); do sleep 0.8; 
        xte 'key Page_Down'; done && xte 'keyup Control_L'
        sleep 2
        _rand_Tab=$(shuf -i 10-20 -n 1)
        xte 'keydown Control_L' && for i in $(seq 1 $_rand_Tab); do sleep 1; 
        xte 'key Down'; done && xte 'keyup Control_L'
      fi
    fi
}

function GetIdle() {
  idle=`expr $(xprintidle) / 1000`;
  # echo $idle;
  if [ $idle -gt $Max_Idle ]; then
    # echo "System goes idle";
    return 0
  else
    # echo "System active"
    return 1
  fi  
}

MoveMouse
echo "Releasing the lock file.."
rm -rf /tmp/automouse.lck
exit
