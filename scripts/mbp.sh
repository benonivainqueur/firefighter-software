# take in a number.that number is the pi id we will be sshing into
# for $1 = 1

if [ "$1" == "0" ]; then
    ssh pi1@192.168.8.172
elif [ "$1" == "1" ]; then
    ssh pi1@192.168.8.197
elif [ "$1" == "2" ]; then
    ssh pi1@192.168.8.203
elif [ "$1" == "3" ]; then
    ssh pi@192.168.8.212
elif [ "$1" == "4" ]; then
    ssh pi@192.168.8.211
elif [ "$1" == "5" ]; then
    ssh pi@192.168.8.188
else 
    echo "Invalid pi id"
fi

