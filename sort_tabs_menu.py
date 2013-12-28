import sublime
from os.path import join, exists
from os import makedirs

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

MENU_ITEM = '''        {
            "caption": "%(caption)s",
            "command": "%(command)s"
        }'''


def update_menu():
	menu_path = join(sublime.packages_path(), "User", "SortTabs")
	menu = join(menu_path, "Tab Context.sublime-menu")
	if not exists(menu_path):
		makedirs(menu_path)
	menu_items = []
	items = settings.get("tab_context_sort_menu", [])
	for i in items:
		menu_items.append(MENU_ITEM % {"caption": i["caption"], "command": i["command"]})
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
	update_menu()
	settings.clear_on_change('reload_menu')
	settings.add_on_change('reload_menu', refresh_menu)


def plugin_loaded():
	global settings
	settings = sublime.load_settings('SortTabs.sublime-settings')
	refresh_menu()


if not ST3:
	plugin_loaded()
