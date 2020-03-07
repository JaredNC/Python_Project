nohup gunicorn -- bind=0:9999 api:app > my.log 2>&1 &
echo $! > save_pid_2.txt