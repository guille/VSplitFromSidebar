import sublime
import sublime_plugin


class VsplitCommand(sublime_plugin.WindowCommand):

	def __init__(self, window):
		self.window = window
		super().__init__(window)

	def create_vsplit(self):
		# Get layout
		layout = self.window.get_layout()
		cells, rows, cols = layout["cells"], layout["rows"], layout["cols"]

		# Add new equally sized column
		new_cols = list()
		for x in range(len(cols)):
			new_cols.append(round(x * 1/len(cols), 2))
		new_cols.append(1)

		# Add new cell with increased x1 and x2
		# cell is [x1, y1, x2, y2]
		last_cell = cells[-1]
		new_cell = last_cell.copy()
		new_cell[0] += 1
		new_cell[2] += 1
		cells.append(new_cell)

		# Save layout
		layout = {"cells": cells, "rows": rows, "cols": new_cols}
		self.window.run_command('set_layout', layout)

	def run(self, clone_file=False):
		view = self.window.active_view()
		if clone_file:
			self.window.run_command("clone_file")
		self.create_vsplit()
		# Move file and focus to the new vsplit. Lines below from the "Origami" package.
		active_group = self.window.active_group()
		views_in_group = self.window.views_in_group(active_group)
		self.window.set_view_index(view, active_group, len(views_in_group))
