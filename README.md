# grafana-exporter-importer
A python tool that synchronises grafana dashboards between instances

# What does it do?
It uses the [HTTP API](http://docs.grafana.org/reference/http_api/) to pull out all the dashboards from a source system, and push them into a desination system.

# Prerequisites:
First you'll need to install progress bar:
```bash
pip install progressbar
```
Once you have that, you'll need to generate some API keys in grafana: ![Screenshot of API location](http://docs.grafana.org/img/v2/orgdropdown_api_keys.png) 
The Source will only require viewing access, the destination will need editor or above.

# Passing Keys and hostnames to the script

`export-grafana-dashboards.py` expects four environment variables to be set:
* **SOURCEKEY**: the API key for the source grafana
* **DESTKEY**: the API key for the destination grafana
* **SOURCEHOST**: the hostname of the source grafana instance in the form of `http://your-hostname.com`
* **DESTHOST**: Same again but for Destination grafana

if you've done everything correct, you'll see this:

```bash
Using default values
Downloading dashboards from source grafana instance
100%|##########################################################################|


Uploading dashboards to destination Grafana instance
100%|##########################################################################|
```
