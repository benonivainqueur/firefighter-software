#!/bin/bash

# Ask the user to enter a number
read -p "Enter a number: " num

# Export the number as PI_ID in the .bashrc file
echo "export PI_ID=$num" >> ~/.bashrc

# Print a success message
echo "The number $num has been exported as PI_ID to .bashrc"