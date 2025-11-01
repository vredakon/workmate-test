import csv
import argparse
from types import FunctionType
from typing import Any
from tabulate import tabulate
from .functions import average
from .parser import parser


report_types: list[str] = ["average-rating"]


def group_by(entries: list[dict[Any, Any]], field_name: str, field_to_agregate: str, function: FunctionType):
    result = {}
    for entry in entries:
        
        if entry[field_name] in result.keys():
            result[entry[field_name]].append(entry[field_to_agregate])
        
        else:
            result.update({entry[field_name]: [entry[field_to_agregate]]})
            
    for entry in result:
        result.update({entry: function(tuple(map(float, result[entry])))})

    print(result)    
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


def main() -> None:
    args: argparse.Namespace = parser.parse_args()

    if args.report not in report_types:
        print("Unknown report name")
        raise Exception
    
    report_name = args.report.split("-")
    entries = process_files(args.files)        
    report = group_by(entries, "brand", report_name[1], eval(report_name[0]))
    data = list([[key, report[key]] for key in report])
    data.sort(key=lambda x: x[1], reverse=True)
    print(tabulate(data, headers=["brand", report_name[1]], tablefmt="grid"))
    
    
if __name__ == "__main__":
    main()