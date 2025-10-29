import argparse
import csv
from types import FunctionType
from typing import Any
from tabulate import tabulate

report_types = ["average-rating"]


parser: argparse.ArgumentParser = argparse.ArgumentParser()
parser.add_argument("--files", "-f", type=str, required=True, nargs="+")
parser.add_argument("--report", "-r", type=str, required=True)
args: argparse.Namespace = parser.parse_args()


def average(values: list[int | float]) -> float: 
    return (sum(values) / len(values)).__round__(2)


def group_by(entries: list[dict[Any, Any]], field_name: str, field_to_agregate: str, agregate_function: FunctionType):
    result = {}
    for entry in entries:
        
        if entry[field_name] in result.keys():
            result[entry[field_name]].append(entry[field_to_agregate])
        
        else:
            result.update({entry[field_name]: [entry[field_to_agregate]]})
            
    for entry in result:
        result.update({entry: agregate_function(tuple(map(float, result[entry])))})
        
    return result


def process_files(directories: list[str]):
    
    entries = []
    
    for directory in directories:
        
        if not directory.endswith(".csv"):
            print("Incorrect file type")
            raise Exception
        
        with open(directory) as file:
            dict_reader = csv.DictReader(file)
            for entry in dict_reader:
                entries.append(entry)
    
    return entries


def main(args: argparse.Namespace) -> None:
    entries = process_files(args.files)
    report_name = args.report.split("-")
    report = group_by(entries, "brand", report_name[1], eval(report_name[0]))
    data = list([[key, report[key]] for key in report])
    data.sort(key=lambda x: x[1], reverse=True)
    print(tabulate(data, headers=["brand", report_name[1]], tablefmt="grid"))
    
    
if __name__ == "__main__":
    main(args)