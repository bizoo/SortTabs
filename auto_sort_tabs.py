import sublime, sublime_plugin


settings = sublime.load_settings('SortTabs.sublime-settings')


class AutoSortTabsListener(sublime_plugin.EventListener):
	def on_load(self, view):
		if settings.get('sort_on_load_save'):
			if view.window():
				self._run_sort(view)

	def on_post_save(self, view):
		if settings.get('sort_on_load_save'):
			if view.window():
				self._run_sort(view)

	def _run_sort(self, view):
		cmd = settings.get('sort_on_load_save_command')
		if cmd:
			view.window().run_command(cmd)
