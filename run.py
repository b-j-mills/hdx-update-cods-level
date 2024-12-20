import argparse
import logging
from os import getenv
from os.path import join, expanduser

from hdx.api.configuration import Configuration
from hdx.data.dataset import Dataset
from hdx.facades.keyword_arguments import facade
from hdx.data.hdxobject import HDXError

from cod_levels import *

logger = logging.getLogger(__name__)

lookup = "hdx-update-cods-level"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-hu", "--hdx_url", default=None, help="HDX site to use")
    parser.add_argument("-sy", "--sync", default=False, help="Sync with ITOS system?")
    parser.add_argument("-cs", "--cod_standard", default=None, help="Which datasets should be standard")
    parser.add_argument("-ce", "--cod_enhanced", default=None, help="Which datasets should be enhanced")
    parser.add_argument("-nc", "--not_cod", default=None, help="Which datasets should not be CODs")
    args = parser.parse_args()
    return args


def main(
    sync,
    cod_standard,
    cod_enhanced,
    not_cod,
    **ignore,
):
    configuration = Configuration.read()
    cod_levels = dict()
    if sync:
        cod_levels = get_cod_levels(configuration["itos_url"], configuration["itos_ps_url"])

    for dataset in cod_standard:
        if dataset[-3:] == "xxx" or dataset == "":
            continue
        cod_levels[dataset] = "cod-standard"
    for dataset in cod_enhanced:
        if dataset[-3:] == "xxx" or dataset == "":
            continue
        cod_levels[dataset] = "cod-enhanced"
    for dataset in not_cod:
        if dataset[-3:] == "xxx" or dataset == "":
            continue
        cod_levels[dataset] = ""

    for name in cod_levels:
        new_cod_level = cod_levels[name]
        dataset = Dataset.read_from_hdx(name)
        if not dataset:
            logger.error(f"Could not find HDX dataset {name}!")
            continue
        old_cod_level = dataset.get("cod_level")

        if old_cod_level and old_cod_level == new_cod_level:
            continue

        logger.info(f"Updating {dataset['title']}")
        dataset["cod_level"] = new_cod_level
        if "extras" in dataset:
            keys_to_delete = ["extras"]
        else:
            keys_to_delete = []
        try:
            dataset.update_in_hdx(
                update_resources=False,
                hxl_update=False,
                operation="patch",
                batch_mode="KEEP_OLD",
                skip_validation=True,
                ignore_check=True,
                keys_to_delete=keys_to_delete,
            )
        except HDXError:
            logger.exception(f"Could not update {dataset['name']}")


if __name__ == "__main__":
    args = parse_args()
    hdx_url = args.hdx_url
    if hdx_url is None:
        hdx_url = getenv("HDX_URL")
    sync = args.sync
    if sync is None:
        sync = getenv("SYNC")
    cod_standard = args.cod_standard
    if cod_standard is None:
        cod_standard = getenv("COD_STANDARD", "")
    cod_standard = cod_standard.replace(" ", "").split(",")
    cod_enhanced = args.cod_enhanced
    if cod_enhanced is None:
        cod_enhanced = getenv("COD_ENHANCED", "")
    cod_enhanced = cod_enhanced.replace(" ", "").split(",")
    not_cod = args.not_cod
    if not_cod is None:
        not_cod = getenv("NOT_COD", "")
    not_cod = not_cod.replace(" ", "").split(",")
    facade(
        main,
        user_agent_config_yaml=join(expanduser("~"), ".useragents.yaml"),
        user_agent_lookup=lookup,
        project_config_yaml=join("config", "project_configuration.yaml"),
        sync=sync,
        cod_standard=cod_standard,
        cod_enhanced=cod_enhanced,
        not_cod=not_cod,
    )
