import argparse


parser: argparse.ArgumentParser = argparse.ArgumentParser()
parser.add_argument("--files", "-f", type=str, required=True, nargs="+")
parser.add_argument("--report", "-r", type=str, required=True)