import sublime, sublime_plugin
import time

ST3 = int(sublime.version()) >= 3000

if ST3:
	import SortTabs.sort_tabs as sort_tabs
	from SortTabs.sort_tabs import settings, internal_settings
else:
	import sort_tabs
	from sort_tabs import settings, internal_settings


class AutoSortTabsListener(sublime_plugin.EventListener):
	def on_load(self, view):
		if settings().get('sort_on_load_save'):
			if not self._run_sort(view):
				view.settings().set('sorttabs_tosort', True)

	def on_post_save(self, view):
		if settings().get('sort_on_load_save'):
			self._run_sort(view)

	def on_activated(self, view):
		view.settings().set('sorttabs_lastactivated', time.time())
		if settings().get('sort_on_load_save'):
			if view.settings().get('sorttabs_tosort'):
				if self._run_sort(view):
					view.settings().erase('sorttabs_tosort')

	def _run_sort(self, view):
		if view.window() and view.window().get_view_index(view)[1] != -1:
			cmd = settings().get('sort_on_load_save_command')
			if not cmd:
				# Last used sort
				cmd = internal_settings().get('last_cmd')
			if cmd:
				view.window().run_command(cmd)
			return True
		return False
