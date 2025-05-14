import json
import logging
import os
import sys
import traceback
import zipfile
from typing import Dict, Any

from my_proof.proof import Proof

INPUT_DIR, OUTPUT_DIR = '/input', '/output'

logging.basicConfig(level=logging.INFO, format='%(message)s')


def load_config() -> Dict[str, Any]:
    """Load proof configuration from environment variables."""
    config = {
        'dlp_id': 50,  # Set your own DLP ID here
        'input_dir': INPUT_DIR
    }
    logging.info(f"Using config: {json.dumps(config, indent=2)}")
    return config


def run() -> None:
    """Generate proofs for all input files."""
    logging.info(f"Running proof generation")
    config = load_config()
    input_files_exist = os.path.isdir(INPUT_DIR) and bool(os.listdir(INPUT_DIR))

    if not input_files_exist:
        raise FileNotFoundError(f"No input files found in {INPUT_DIR}")
    extract_input()


    proof = Proof(config)
    proof_response = proof.generate()

    output_path = os.path.join(OUTPUT_DIR, "results.json")
    with open(output_path, 'w') as f:
        json.dump(proof_response.model_dump(), f, indent=2)
    logging.info(f"Proof generation complete: {proof_response}")


def extract_input() -> None:
    """
    If the input directory contains any zip files, extract them
    :return:
    """

    logging.info(f"Extracting input files from {INPUT_DIR} due to ZIP files")
    for input_filename in os.listdir(INPUT_DIR):
        input_file = os.path.join(INPUT_DIR, input_filename)

        # Try both methods to detect ZIP files
        is_zip = input_filename.lower().endswith('.zip') or zipfile.is_zipfile(input_file)
        
        logging.info(f"Checking if {input_filename} is a zip file (is_zip={is_zip})")
        if is_zip:
            logging.info(f"Extracting {input_filename}")
            try:
                with zipfile.ZipFile(input_file, 'r') as zip_ref:
                    zip_ref.extractall(INPUT_DIR)
                logging.info(f"Extracted {input_filename}")
            except zipfile.BadZipFile:
                logging.error(f"Failed to extract {input_filename} - not a valid ZIP file")


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        logging.error(f"Error during proof generation: {e}")
        traceback.print_exc()
        sys.exit(1)
