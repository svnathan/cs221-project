#!/bin/bash

TotalTime="$(date +%s)"

red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

dataset_dir=$PWD"/dataset/"

Time="$(date +%s)"
python parser.py $dataset_dir
echo "${green}Parsing Time is $(($(date +%s)-Time)) seconds${reset}"

echo "${red}Completion Time is $(($(date +%s)-TotalTime)) seconds${reset}"
