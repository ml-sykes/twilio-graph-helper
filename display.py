#!/usr/bin/env python3

import pydot

from graph import DirectedGraph


class GraphicalDisplay:
	def __init__(self, graph):
		self.graph = graph


	def save(self, filepath):
		dot_graph = pydot.Dot("Twilio path", graph_type="digraph", bgcolor="lightgrey")

		for node in self.graph.get_nodes():
			dot_widget = pydot.Node(node)
			dot_graph.add_node(dot_widget)
			for child in self.graph.get_edges(node):
				dot_edge = pydot.Edge(node, child)
				dot_graph.add_edge(dot_edge)

		dot_graph.write_png(filepath)


	def display(self):
		pass
