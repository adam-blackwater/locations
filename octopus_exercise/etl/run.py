import os

from typing import Any, Dict, List

from octopus_exercise.etl.load import load_locations_into_db
from octopus_exercise.etl.extract import extract
from octopus_exercise.etl.transform import LocationETLModel, transform

DEFAULT_INTEGRATED_DATA_LOCATION = "../data/integrated.json"


def main():
    print("################### STARTING ETL PIPELINE ######################")

    data: Dict[str, Any] = extract(
        os.getenv("INTEGRATED_DATA_LOCATION", DEFAULT_INTEGRATED_DATA_LOCATION)
    )
    ###########################################################################
    # The below commented out line is part of my effort to merge existing     #
    # locations but I didn't have time to complete it                         #
    ###########################################################################
    # existing:List[LocationETLModel] = load_locations_into_memory()

    transformed_data: List[LocationETLModel] = transform(data)
    load_locations_into_db(transformed_data)

    print("################### FINNISHED ETL PIPLINE ######################")


if __name__ == "__main__":
    main()
