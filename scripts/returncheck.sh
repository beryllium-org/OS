if [ $?!=123 ];then
    echo -e "\nBlack run correctly."
else
    echo "\nBlack formatting failed."
    exit 1
fi
exit 0 
