git pull origin master
nohup python telegram_bot_test.py > my.log 2>&1 &
echo $! > save_pid.txt