#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import frida
import sys

def on_message(message, data):
	if message['type'] == 'error':
		print('[!] ' + message['stack'])
	elif message['type'] == 'send':
		print('[i] ' + message['payload'])
	else:
		print(message)

def main(target_process):
	try:
		session = frida.attach(target_process)
	except:
		sys.exit('The process does not exist')
	script = session.create_script("""
	pointer = Module.findExportByName(null, "printf");
	dir = Memory.allocUtf8String("buenos dias numero %d");
	Interceptor.attach(ptr(pointer), {
		onEnter: function(args) {
			//send(Memory.readCString(args[0]))
			//send(args[1].toInt32().toString())
			//args[0] = dir;
			//args[1] = ptr("1337");
		},
		onLeave: function(retval) {
		}
	});
	""")
	script.on('message', on_message)
	script.load()
	input('[!] press <Enter> to detach from instrumented program.\n\n')
	session.detach()

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Usage: {} <process name or PID>'.format(__file__))
		sys.exit(1)

	if sys.argv[1].isdigit():
		target_process = int(sys.argv[1])
	else:
		target_process = sys.argv[1]
	
	main(target_process)
