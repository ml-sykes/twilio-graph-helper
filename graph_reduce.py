#!/usr/bin/env python3

import argparse

import graph
import display


def create_arg_parser():
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument("-f", "--flow", metavar="FILEPATH", required=True, help="Filepath to the flow to use")
	arg_parser.add_argument("-o", "--output", metavar="FILEPATH", required=True, help="Filepath to save the result")
	arg_parser.add_argument("-a", "--action", choices=["nop", "from_node", "to_node"], required=True,
			help="The action to take ")
	arg_parser.add_argument("-n", "--node", required=True, help="The target node of the action")
	return arg_parser


if __name__ == "__main__":
	arg_parser = create_arg_parser()
	args = arg_parser.parse_args()

	flow_graph = graph.DirectedGraph()
	flow_graph.create_from_flow_filepath(args.flow)

	if args.action == "nop":
		dsp = display.GraphicalDisplay(flow_graph)
		dsp.save(args.output)
	elif args.action == "from_node":
		subgraph = flow_graph.create_subgraph_from_node(args.node)
		dsp = display.GraphicalDisplay(subgraph)
		dsp.save(args.output)
		print("Result saved to " + args.output)
	elif args.action == "to_node":
		subgraph = flow_graph.create_subgraph_to_node("Trigger", args.node)
		dsp = display.GraphicalDisplay(subgraph)
		dsp.save(args.output)
		print("Result saved to " + args.output)
