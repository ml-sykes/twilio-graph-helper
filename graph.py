#!/usr/bin/env python3

import json


class LoopDetected(Exception):
	pass


class DirectedGraph:
	def __init__(self):
		self._graph = {}


	def add_node(self, name):
		self._graph[name] = self._graph.get(name, set())


	def add_edge(self, from_node, to_node):
		edges = self._graph.get(from_node, set())
		edges.add(to_node)
		self._graph[from_node] = edges
		self.add_node(to_node)


	def remove_node(self, node):
		if self._graph.pop(node, None) != None:
			self._cleanup_edges(node)


	def remove_edge(self, from_node, to_node):
		self.get_edges(from_node).discard(to_node)


	def remove_disconnected_nodes(self):
		nodes = self.get_nodes()
		for i in range(len(nodes) - 1, -1, -1):
			if self.is_disconnected(nodes[i]):
				self.remove_node(nodes[i])


	def get_nodes(self):
		return self._graph.keys()


	def get_edges(self, node):
		return self._graph.get(node, set())


	def is_disconnected(self, target_node):
		has_connection = False

		if len(self.get_edges(target_node)) > 0:
			has_connection = True
		else:
			for node in self.get_nodes():
				if target_node in self.get_edges(node):
					has_connection = True
					break

		return not has_connection


	def copy(self):
		new_graph = DirectedGraph()
		for node in self.get_nodes():
			new_graph._graph[node] = self.get_edges(node).copy()
		return new_graph


	def create_from_flow_filepath(self, filepath):
		widgets_data = []
		with open(filepath, "r") as file:
			flow_json = json.loads(file.read())
			widgets_data = flow_json["states"]

			for data in widgets_data:
				name = data["name"]
				child_names = set(transition["next"] for transition in data["transitions"] if "next" in transition)
				self._graph[name] = child_names


	def create_subgraph_from_node(self, node, subgraph = None, current_path = []):
		if not subgraph:
			subgraph = DirectedGraph()

		if node in current_path:
			raise LoopDetected()

		subgraph.add_node(node)
		current_path.append(node)
		for child in self._graph[node]:
			subgraph.add_edge(node, child)
			try:
				self.create_subgraph_from_node(child, subgraph)
			except LoopDetected as e:
				subgraph.remove_edge(node, child)
		current_path.pop()

		return subgraph


	def create_subgraph_to_node(self, node, target_node, subgraph = None, current_path = []):
		# Implementation: Start from the leaf nodes and delete them until you
		# are only left with paths to the target node

		# TODO: this doesn't remove disconnected graphs
		if not subgraph:
			subgraph = self.copy()

		current_path.append(node)
		for child in subgraph.get_edges(node).copy():
			if child in current_path:
				subgraph.remove_edge(node, child)
			else:
				subgraph.create_subgraph_to_node(child, target_node, subgraph, current_path)
		current_path.pop()

		if len(subgraph.get_edges(node)) == 0 and node != target_node:
			subgraph.remove_node(node)

		return subgraph


	def _cleanup_edges(self, removed_node):
		for node in self.get_nodes():
			self.get_edges(node).discard(removed_node)


