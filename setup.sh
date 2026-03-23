#!/bin/bash

# Title: setup.sh
# Author: Jenna Cook
# Description: Enter values for these envrionement
# variables before running threat_profile.py

# Enter your API key for the Gemini API
export GENAI_API_KEY="ENTER_VALUE_HERE"
# Enter your API key for the OpenCTI API
export OPENCTI_API_KEY="ENTER_VALUE_HERE"
# Enter the website link of the OpenCTI instance
# OpenCTI Demo Instance: https://demo.opencti.io/
# NetmanageIT Instance: https://opencti.netmanageit.com/
export OPENCTI_INSTANCE="ENTER_VALUE_HERE"
# Enter the cybercriminal organization name. It must
# match the name displayed in the OpenCTI instance.
# Examples: Rhysida, Play, INC Ransom
export CYBERCRIMINAL_ORG="ENTER_VALUE_HERE"
# Enter the name of the scraping function.
# Examples: scrape_rhysida, scrape_play,
# scrape_inc_ransom
export SCRAPING_FUNC="ENTER_VALUE_HERE"
