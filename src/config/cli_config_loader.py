import argparse
import os
import yaml

class CLIConfigLoader:
    def __init__(self):
        self.cli_args = self.parse_arguments()
        self.config = self.load_config(self.cli_args.config_file)
        self.override_config()

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description="Backtesting CLI Configuration Loader")
        parser.add_argument(
            "--config-file",
            type=str,
            default="config.yaml",
            help="Path to the YAML configuration file."
        )
        parser.add_argument(
            "--sim-param",
            type=float,
            help="Override the simulation parameter (e.g., risk factor, drift, etc.)."
        )
        parser.add_argument(
            "--data-dir",
            type=str,
            help="Override the data directory path."
        )
        parser.add_argument(
            "--logging-level",
            type=str,
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            help="Set the logging level."
        )
        return parser.parse_args()

    def load_config(self, file_path):
        if not os.path.exists(file_path):
            print(f"Configuration file '{file_path}' not found. Using empty configuration.")
            return {}
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        if not config:
            config = {}
        return config

    def override_config(self):
        # Override simulation parameter if provided
        if self.cli_args.sim_param is not None:
            if "simulation" not in self.config:
                self.config["simulation"] = {}
            self.config["simulation"]["parameter"] = self.cli_args.sim_param

        # Override data directory if provided
        if self.cli_args.data_dir:
            if "file_paths" not in self.config:
                self.config["file_paths"] = {}
            self.config["file_paths"]["data_dir"] = self.cli_args.data_dir

        # Override logging level if provided
        if self.cli_args.logging_level:
            if "logging" not in self.config:
                self.config["logging"] = {}
            self.config["logging"]["level"] = self.cli_args.logging_level

    def get_config(self):
        return self.config
