import logging

from requests import get
from requests.exceptions import ConnectTimeout
from slugify import slugify

logger = logging.getLogger(__name__)


def get_cod_levels(itos_url, itos_ps_url):
    try:
        itos_datasets = get(itos_url).json()
    except ConnectTimeout:
        logger.error("Could not connect to ITOS API")
        return

    itos_levels = {}
    for dataset in itos_datasets:
        location = dataset["Location"]
        theme = dataset["Theme"]
        if theme == "COD_AB" and (location == ["MMR"] or location == ["mmr"]):
            name = slugify(dataset["DatasetTitle"])
        else:
            name = slugify(f"{theme} {' '.join(location)}")
        level = dataset["is_enhanced_cod"]
        if level:
            itos_levels[name] = "cod-enhanced"
        else:
            itos_levels[name] = "cod-standard"

    try:
        itos_ps_datasets = get(itos_ps_url).json()
    except ConnectTimeout:
        logger.error("Could not connect to ITOS API")
        return

    for dataset in itos_ps_datasets["LocationCODPSs"]:
        name = f"cod-ps-{dataset['location_iso'.lower()]}"
        itos_levels[name] = "cod-enhanced"

    return itos_levels

