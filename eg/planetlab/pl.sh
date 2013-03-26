#!/bin/bash
# 
# Manages the PlanetLab deployment
#
# Copyright (c) 2013 by Michael Luckeneder
#


export MQ_NODES='./nodes.txt';
export MQ_SLICE='unimelb_barker';

start (){
    for n in $(cat nodes.txt); do
            /usr/bin/ssh -n -T unimelb_barker@$n ". cs4098/bin/activate && python server.py > ~/output.log "&
    done
}

stop() {
	ps aux | grep .*unimelb_barker.* | awk '{print $2}' | xargs kill
	for n in $(cat nodes.txt); do
		/usr/bin/ssh -n -T unimelb_barker@$n "/sbin/pidof python server.py | xargs kill" &
	done
}

deploy(){
	for l in `cat nodes.txt`; do
		echo $l;
		scp -i ~/.ssh/planetlab_rsa -r cs4098/server.py unimelb_barker@$l:~/server.py

	done
}

install(){
	for n in $(cat nodes.txt); do
			echo $n
            /usr/bin/ssh -n -T unimelb_barker@$n ". ./cs4098/bin/activate && pip install pil tornado"
    done
}


case $1 in
	start)
	start
	;;

	stop)
	stop
	;;

	deploy)
	deploy
	;;

	install)
	install
	;;
esac
