import os, sys, shlex
from p4python.P4 import P4

p4 = P4()

def get_textmate_file_list():
	# shlex.split parses the bash argument string into a list
	return shlex.split(os.environ['TM_SELECTED_FILES']) \
		if os.environ.has_key('TM_SELECTED_FILES') \
		else [os.environ['TM_FILEPATH']]


def get_files_in_p4_workspace(file_list):
	'''
	Returns a new list that only contains files from file_list that are inside
	the P4 current workspace.
	'''
	
	if not p4.connected():
		p4.connect()
		
	p4_info = p4.run('info')[0]
	
	return [file for file in file_list if file.startswith(p4_info['clientRoot'])]


def prepare_file_list_for_p4(file_and_directory_list):
	'''
	Returns a new list that
	 - adds /... to the ends of directory paths
	 - filters out files that are children of a supplied directory
	'''
	
	file_list = []
	directory_list = []
	
	for file_or_directory in file_and_directory_list:
		if os.path.isdir(file_or_directory):
			directory_list.append(file_or_directory)
		else:
			file_list.append(file_or_directory)
			
	result = [directory + '/...' for directory in directory_list]
	
	for file in file_list:
		file_in_directory = False
		
		for directory in directory_list:
			if file.startswith(directory):
				file_in_directory = True
				break
				
		if not file_in_directory:
			result.append(file)
			
	return result
	
	
def run_p4_command_on_selected_textmate_files(*args, **kwargs):
	file_list = prepare_file_list_for_p4(
					get_files_in_p4_workspace(
						get_textmate_file_list()
					)
				)

	if not file_list:
		return ["These files are not in the P4 workspace."]
		
	else:
		kwargs['file_list'] = file_list
		return run_p4_command(*args, **kwargs)
		

def run_p4_command(command, file_list = [], fallback_command = None, fallback_silently = True):
	p4_response = []
	
	#if command is 'sync':
	#	return file_list
	
	
	if not p4.connected():
		p4.connect()
	
	# This makes P4's output human-readible instead of dict-y
	p4.tagged = False
	
	def run_command(command, fallback_command = None):
		p4_response = []

		try:
			'''
			When you submit or shelve a changeset without a hardcoded
			description, p4 will give you the opportunity to create one in
			the app specified by $EDITOR.
			
			'mate -w' spawns TextMate and tells it to wait until you close
			the window to send its contents to stdin.
			'''
			if not os.environ.has_key('EDITOR'):
				os.environ['EDITOR'] = 'mate -w'
			
			p4_response = p4.run(command, file_list)
			p4.disconnect()
			
			return p4_response
			
		except Exception:
			'''
			- I tried typing this as a P4Exception, but failed miserably
		
			- Another method to consider would be setting exception_level to 0
			and printing the warnings straight from p4.warnings instead of
			catching them as exceptions.
			'''

			if fallback_command: 
				p4_response = run_command(fallback_command)

			if not fallback_silently or (fallback_silently and not fallback_command):
				if p4.warnings:
					print('<h2>Warnings:</h2>')
					for message in p4.warnings:
						print(message)

				if p4.errors:
					print('<h2>Errors:</h2>')
					for message in p4.errors:
						print(message)
			
			return p4_response
	
	return run_command(command, fallback_command)


def stdout_to_html(lines, line_delimiter = '\n'):
	html = line_delimiter.join(lines)
	html = html.replace('&', '&amp;').replace('<', '&lt;')
	return '<pre>' + html + '</pre>'