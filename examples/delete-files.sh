#!/bin/bash
echo "Do you wish to remove these files?"
find . -print | grep $1*

select yn in "Yes" "No"; do
  case $yn in
    Yes ) rm -rf $(find . -print | grep $1*) && echo "Files were removed" && exit;;
    No ) exit;;
  esac
done
