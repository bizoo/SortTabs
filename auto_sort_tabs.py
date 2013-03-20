import sublime, sublime_plugin
import time

ST3 = int(sublime.version()) >= 3000

if ST3:
	import SortTabs.sort_tabs
else:
	import sort_tabs


class AutoSortTabsListener(sublime_plugin.EventListener):
	def on_load(self, view):
		if settings.get('sort_on_load_save'):
			if not self._run_sort(view):
				view.settings().set('sorttabs_tosort', True)

	def on_post_save(self, view):
		if settings.get('sort_on_load_save'):
			self._run_sort(view)

	def on_activated(self, view):
		view.settings().set('sorttabs_lastactivated', time.time())
		if settings.get('sort_on_load_save'):
			if view.settings().get('sorttabs_tosort'):
				if self._run_sort(view):
					view.settings().erase('sorttabs_tosort')

	def _run_sort(self, view):
		if view.window() and view.window().get_view_index(view)[1] != -1:
			cmd = settings.get('sort_on_load_save_command')
			if not cmd:
				# Last used sort
				cmd = sort_tabs.INTERNAL_SETTINGS.get('last_cmd')
			if cmd:
				view.window().run_command(cmd)
			return True
		return False


def plugin_loaded():
	global settings
	settings = sublime.load_settings('SortTabs.sublime-settings')


if not ST3:
	plugin_loaded()
