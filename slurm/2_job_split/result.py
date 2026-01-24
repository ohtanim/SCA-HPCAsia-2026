"""A PrimitiveResult parser"""

import json
import argparse
from qiskit_ibm_runtime.utils.result_decoder import ResultDecoder

parser = argparse.ArgumentParser(
    description="A tool to generate PrimitiveResult from the given primitive output"
)
parser.add_argument("input", help="input file")
args = parser.parse_args()

with open(args.input, encoding="utf-8") as input_file:
    result_str = json.dumps(json.load(input_file))

result = ResultDecoder.decode(result_str)

# Get results for the first (and only) PUB
pub_result = result[0]
print(f"Counts for the 'meas' output register: {pub_result.data.meas.get_counts()}")
