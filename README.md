### Changing the cod-level attribute on HDX

This script collects the COD level (standard, enhanced) from the ITOS API and updates the HDX COD datasets. It can also override those levels with user-specified parameters.

If there are new datasets that need a cod-level assigned, or if an existing dataset needs to be changed, edit the [environment variables](https://github.com/b-j-mills/hdx-update-cods-level/settings/variables/actions) **COD_STANDARD** and **COD_ENHANCED**. Add HDX dataset names (last part of the url) to the appropriate lists. Datasets ending in "xxx" will not be run and are there as example dataset names.

If the levels on HDX need to be synced with the ITOS API, change the environment variable **SYNC** to "True".

If this should be run on a specific HDX site, change the environment variable **HDX_URL** to the full url.

### Usage

This script can be run two ways.

1. On Github Actions: edit the environment variables and hit the run button.


2. Locally: you must be an HDX administrator. 


    python run.py

For the script to run, you will need to have a file called .hdx_configuration.yaml in your home directory containing your HDX key.  

    hdx_key: "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
    hdx_read_only: false
    hdx_site: prod

You will also need to supply the universal .useragents.yaml file in your home directory as specified in the parameter *user_agent_config_yaml* passed to facade in run.py. The collector reads the key **hdx-update-cods-level** as specified in the parameter *user_agent_lookup*.

Alternatively, you can set up environment variables: HDX_KEY, USER_AGENT, PREPREFIX
