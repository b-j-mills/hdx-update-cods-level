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
    parser.add_argument("-hk", "--hdx_key", default=None, help="HDX api key")
    parser.add_argument("-ua", "--user_agent", default=None, help="user agent")
    parser.add_argument("-pp", "--preprefix", default=None, help="preprefix")
    parser.add_argument("-hs", "--hdx_site", default=None, help="HDX site to use")
    parser.add_argument("-sy", "--sync", default=None, help="Sync with ITOS system?")
    parser.add_argument("-cs", "--cod_standard", default=None, help="Which datasets should be standard")
    parser.add_argument("-ce", "--cod_enhanced", default=None, help="Which datasets should be enhanced")
    args = parser.parse_args()
    return args


def main(
    sync,
    cod_standard,
    cod_enhanced,
    **ignore,
):
    configuration = Configuration.read()
    cod_levels = dict()
    if sync:
        cod_levels = get_cod_levels(configuration["itos_url"], configuration["itos_ps_url"])

    for dataset in cod_standard:
        cod_levels[dataset] = "cod-standard"
    for dataset in cod_enhanced:
        cod_levels[dataset] = "cod-enhanced"

    for name in cod_levels:
        if name[-3:] == "xxx":
            continue
        new_cod_level = cod_levels[name]
        dataset = Dataset.read_from_hdx(name)
        if not dataset:
            logger.error(f"Could not find HDX dataset {name}!")
            continue
        old_cod_level = dataset.get("cod_level")

        if old_cod_level and old_cod_level != new_cod_level:
            continue

        logger.info(f"Updating {dataset['title']}")
        dataset["cod_level"] = new_cod_level
        try:
            dataset.update_in_hdx(
                update_resources=False,
                hxl_update=False,
                operation="patch",
                batch_mode="KEEP_OLD",
                skip_validation=True,
                ignore_check=True,
            )
        except HDXError:
            logger.exception(f"Could not update {dataset['name']}")


if __name__ == "__main__":
    args = parse_args()
    hdx_key = args.hdx_key
    if hdx_key is None:
        hdx_key = getenv("HDX_KEY")
    user_agent = args.user_agent
    if user_agent is None:
        user_agent = getenv("USER_AGENT")
    preprefix = args.preprefix
    if preprefix is None:
        preprefix = getenv("PREPREFIX")
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
    facade(
        main,
        hdx_key=hdx_key,
        hdx_site="prod",
        user_agent=user_agent,
        user_agent_config_yaml=join(expanduser("~"), ".useragents.yml"),
        user_agent_lookup=lookup,
        preprefix=preprefix,
        project_config_yaml=join("config", "project_configuration.yml"),
        sync=sync,
        cod_standard=cod_standard,
        cod_enhanced=cod_enhanced,
    )
