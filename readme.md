This script can be use to download/upload xliff files for translation from Pendo. 

# Downloading Files
Use the Python Interactive Command Line to download and upload files. Activate the prompt by navigating to the script folder in the terminal then typing `python` or `python3` depending on your system. Once the prompt is open:

    from pendo import download_xliffs
    download_xliffs(<search_string>, <save_folder>, <api_key>)
    
- Search String: A strings that can be found in the guide name for the guides you would like to download, for example "pNPS_Q3_2024"
- Save Folder: A location on your computer where the downloaded xliff files shoudl be saved
- api_key: an access token for the pendo account you are searching. Note that there are multiple Pendo Accounts/API keys and the script must be run for each one separately.