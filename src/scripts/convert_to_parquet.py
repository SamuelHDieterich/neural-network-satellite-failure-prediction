#!/usr/bin/env python3

# Libraries
import argparse  # For parsing command-line arguments
import logging  # For logging messages
from concurrent.futures import (  # For concurrent processing when converting multiple files in a directory
    ThreadPoolExecutor,
    as_completed,
)
from pathlib import Path  # For handling file paths

import pandas as pd  # Read input pickled data
import polars as pl  # For writing output data in Parquet format (more efficient than pandas)


# Functions
def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert the downloaded ESA Anomaly Dataset to Parquet format."
    )
    parser.add_argument(
        "--input_path",
        type=Path,
        required=True,
        help="Path to the input pickled dataset.",
    )
    parser.add_argument(
        "--output_path",
        type=Path,
        required=True,
        help="Path to save the output Parquet dataset.",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=4,
        help="Number of concurrent jobs when converting a directory (default: 4).",
    )
    return parser.parse_args()


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configure logging settings.

    Parameters
    ----------
    level : int
        Logging level (e.g., logging.INFO, logging.DEBUG).

    Returns
    -------
    None
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def convert_to_parquet(input_path: Path, output_path: Path) -> None:
    """
    Convert the input dataset to Parquet format.

    Parameters
    ----------
    input_path : Path
        Path to the input dataset.
    output_path : Path
        Path to save the output Parquet dataset.

    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
        If the input dataset does not exist.
    ValueError
        If the input file format is unsupported.
    """
    logging.info(f"Reading input dataset from {input_path}...")

    # Check if the input dataset exists
    if not input_path.exists():
        msg = f"Input dataset not found at {input_path}."
        logging.error(msg)
        raise FileNotFoundError(msg)

    # Read the dataset:
    # .csv: Read with polars directly
    # .zip: Read with pandas and then convert to polars
    if input_path.suffix == ".csv":
        df = pl.read_csv(input_path)
    elif input_path.suffix == ".zip":
        df = pl.from_pandas(pd.read_pickle(input_path), include_index=True)
    else:
        msg = f"Unsupported file format: {input_path.suffix}. Only .csv and .zip are supported."
        logging.error(msg)
        raise ValueError(msg)

    logging.info(f"Writing output dataset to {output_path}...")
    output_path.parent.mkdir(
        parents=True, exist_ok=True
    )  # Ensure output directory exists
    df.write_parquet(output_path)


# Main execution
if __name__ == "__main__":
    # Setup
    args = parse_arguments()
    setup_logging()

    # If input_path is a directory, run conversion for all files in the directory
    if args.input_path.is_dir():
        if args.jobs < 1:
            msg = "--jobs must be greater than or equal to 1."
            logging.error(msg)
            raise ValueError(msg)

        logging.info(
            f"Input path {args.input_path} is a directory. Processing all .csv and .zip files in the directory..."
        )
        tasks: list[tuple[Path, Path]] = []
        for file in args.input_path.rglob("*"):
            if file.is_file() and file.suffix in [".csv", ".zip"]:
                relative_path = file.relative_to(args.input_path)
                output_file = args.output_path / relative_path.with_suffix(".parquet")
                if output_file.exists():
                    logging.warning(
                        f"Output file {output_file} already exists. Skipping conversion for {file}."
                    )
                else:
                    tasks.append((file, output_file))

        if not tasks:
            logging.info("No files to convert.")
        else:
            logging.info(
                f"Converting {len(tasks)} files with {args.jobs} concurrent job(s)..."
            )
            failures: list[Path] = []
            with ThreadPoolExecutor(max_workers=args.jobs) as executor:
                future_to_file = {
                    executor.submit(convert_to_parquet, file, output_file): file
                    for file, output_file in tasks
                }
                for future in as_completed(future_to_file):
                    file = future_to_file[future]
                    try:
                        future.result()
                    except Exception:
                        failures.append(file)
                        logging.exception(f"Failed to convert {file}")

            if failures:
                raise RuntimeError(
                    f"Failed to convert {len(failures)} file(s). Check logs for details."
                )
    # If input_path is a file, run conversion for that file
    else:
        logging.info(f"Input path {args.input_path} is a file. Processing the file...")
        if args.input_path.suffix not in [".csv", ".zip"]:
            msg = f"Unsupported file format: {args.input_path.suffix}. Only .csv and .zip are supported."
            logging.error(msg)
            raise ValueError(msg)
        elif args.output_path.exists():
            logging.warning(
                f"Output file {args.output_path} already exists. Skipping conversion for {args.input_path}."
            )
        else:
            convert_to_parquet(args.input_path, args.output_path)
