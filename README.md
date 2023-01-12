### Changing the cod-level attribute on HDX

This script collects the COD level (standard, enhanced) from the ITOS API and updates the HDX COD datasets. It can also override those levels with user-specified parameters.

If there are new datasets that need a cod-level assigned, or if an existing dataset needs to be changed, edit the configuration file (config/project_configuration). Add HDX datasets to the lists under **cod-enhanced** or **cod-standard** using the dataset name (last part of the url).

### Usage

This script can be run two ways.

1. On Github Actions: edit the configuration and hit the run button.


2. Locally: you must be an HDX administrator. 


    python run.py

For the script to run, you will need to have a file called .hdx_configuration.yml in your home directory containing your HDX key.  

    hdx_key: "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
    hdx_read_only: false
    hdx_site: prod

You will also need to supply the universal .useragents.yml file in your home directory as specified in the parameter *user_agent_config_yaml* passed to facade in run.py. The collector reads the key **hdx-update-cods-level** as specified in the parameter *user_agent_lookup*.

Alternatively, you can set up environment variables: HDX_SITE, HDX_KEY, USER_AGENT, PREPREFIX
