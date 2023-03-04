# Crawl_URLs
Simply searches for URLs in source code(Control+U). Has crawldepth feature.




Create virtual environment(if desired)

pip install -r requirements     <--- May need to do "pip install Cython" for some reason.

pip install bs4 requests




Usage:
------
python URLscraper.py https://nmap.org 3     <--- Where 3 is the number for desired crawldepth
