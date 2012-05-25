import subprocess, os, sublime, sublime_plugin

def is_valid_test_file(filename):
	if not os.path.isfile(filename):
	    return False
	filename = os.path.splitext(filename)[0]
	if filename.endswith('Test'):
	    return True
	return False

class PhpunitCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		if not is_valid_test_file(self.view.file_name()):
			print 'This does not seem to be a valid test file'
			return

		folder_name, file_name = os.path.split(self.view.file_name())

		settings = sublime.load_settings('PHPUnitBasic.sublime-settings')
		folder_name_setting = settings.get('run_phpunit_in_folder', '')

		if (len(folder_name_setting) > 0):
			folder_name = folder_name_setting

		cmd = 'phpunit  '+self.view.file_name()

		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=folder_name, shell=True)
		result, err = p.communicate()

		if (len(result) > 0):
			lastline = result.splitlines()[-1]

			if "OK" in lastline:
				self.view.set_status('phpunit',"WIN! "+lastline)
				sublime.set_timeout(self.clear_status,5000)
			else:
				sublime.active_window().run_command("show_panel", {"panel": "console", "toggle": True})
				print result
				self.view.set_status('phpunit',"FAIL!")
				sublime.set_timeout(self.clear_status,5000)
		elif (len(err) > 0):
			sublime.active_window().run_command("show_panel", {"panel": "console", "toggle": True})
			print 'ERROR: '+err
		else:
			sublime.active_window().run_command("show_panel", {"panel": "console", "toggle": True})

	def clear_status(self):
		self.view.erase_status('phpunit')


class PhpunitEventListener(sublime_plugin.EventListener):

	def on_post_save(self, view):

		if not is_valid_test_file(view.file_name()):
			return

		settings = sublime.load_settings('PHPUnitBasic.sublime-settings')
		if settings.get('run_on_save', False) == False:
			return

		sublime.active_window().run_command("phpunit")
