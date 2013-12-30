import sublime
import sublime_plugin
from os.path import join, exists
from os import makedirs
import shutil

ST3 = int(sublime.version()) >= 3000

MENU = '''[
    { "caption": "-" },
    {
        "caption": "Sort Tabs By...",
        "children":
        [
%(items)s
        ]
    },
    { "caption": "-" }
]
'''

MENU_ITEM = '''            {
                "caption": "%(caption)s",
                "command": "%(command)s"
            }'''


class SortTabsUninstallMenuCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		menu_path = join(sublime.packages_path(), "User", "SortTabs")
		try:
			if exists(menu_path):
				shutil.rmtree(menu_path)
		except:
			print("SortTabs: Failed to remove Tab Context Menu")



class SortTabsInstallMenuCommand(sublime_plugin.ApplicationCommand):
	def run(self, install=False):
		menu_path = join(sublime.packages_path(), "User", "SortTabs")
		menu = join(menu_path, "Tab Context.sublime-menu")

		# Ensure there isn't an accidental install (not likely)
		if not install and (not exists(menu_path) or not exists(menu)):
			return

		# Create directory if needed
		if not exists(menu_path):
			makedirs(menu_path)

		# Build up menu item list
		menu_items = []
		items = settings.get("tab_context_sort_menu", [])
		for i in items:
			menu_items.append(MENU_ITEM % {"caption": i["caption"], "command": i["command"]})

		# Generate Menu
		try:
			if len(menu_items):
				with open(menu, "w") as f:
					f.write(MENU % {"items": ',\n'.join(menu_items)})
			else:
				with open(menu, "w") as f:
					f.write("[\n]\n")
		except:
			print("SortTabs: Failed to update Tab Context Menu")


def refresh_menu():
	sublime.run_command("sort_tabs_install_menu")
	settings.clear_on_change('refresh_menu')
	settings.add_on_change('refresh_menu', refresh_menu)


def plugin_loaded():
	global settings
	settings = sublime.load_settings('SortTabs.sublime-settings')
	settings.clear_on_change('refresh_menu')
	settings.add_on_change('refresh_menu', refresh_menu)


if not ST3:
	plugin_loaded()
