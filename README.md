# NormattivaCrawling

## License

This project is licensed under the terms of the GNU General Public License v3.0 (GPLv3).  
Any modification must be released under the same license.  
Commercial or private proprietary use is **not allowed** without releasing the source code.

## Overview

NormattivaCrawling is a Python-based web crawler designed to extract data from Normattiva website. The crawler automates the process of navigating the website, collecting specific information, and storing it in a structured format for further processing and analysis.

## Features

- **Automated Web Scraping**: Efficiently scrapes large volumes of data from normattiva website.
- **Post-processing**: Cleans and formats the collected data for easier analysis.

## Installation

1. **Prerequisites**:  
   - The project uses a ChromeDriver for Windows, which is already included in the `chrome` directory. Therefore, you do not need to download or install ChromeDriver separately. The project is ready to use, but it must be run in a Windows environment.

2. **Steps to Install the Project Locally**:  
   - Clone the repository:

     ```bash
     git clone https://github.com/FValerio96/NormattivaCrawling.git
         ```

That's it! The project is ready to run once cloned. Ensure that you are on a Windows machine since the included ChromeDriver is configured specifically for Windows.

## Usage

This project **enables you to download entire years of legal acts** from the "Normattiva" website and save them in a `.jsonl` file. By specifying a range of years, the program crawls the site and retrieves **all acts** within that range, making it easy to collect comprehensive legal data for multiple years.

### How to Use the Project

1. **Specify the Year Range**:  
   To start crawling, you need to define the `starting_year` and `ending_year`. The program will download **all acts** within this year range, and **both years are included**. For example, if you specify 1970 as the `starting_year` and 1975 as the `ending_year`, the program will retrieve acts for **all six years** from 1970 through 1975.

2. **Modify the Code**:  
   Open the `main.py` file and locate the following line of code:

   ```python
   crawling_per_anni(1970, 1975)

3. **File Output**: \
The downloaded data will be saved in a file located in the main directory. This file is created automatically and named as "from ending_year to starting_year elenco atti.jsonl".

4. **Post-processing**: \
It is possible that there may be duplicate acts in the collected data. To handle this, a postProcessor is provided in the crawling folder. To use it:

    * Open the postProcessor file.

    * Modify the path of the file to be processed. Set the jsonl_file_path to the path of the file you want to clean, for example:
    * run the postProcessor.

    ```python
    #example
    jsonl_file_path = 'dataset/from 1959 to 1964 elenco atti.jsonl'


**Please note**:

During the crawling process, an interruption in work may occur. This is not a significant problem and may be due to factors such as drops in network quality or temporary problems with Normattiva's server.

To avoid loss of work already done, the crawler automatically saves the collected links in the `links.txt` file, located in the main project folder. If the crawler stops, it will automatically resume from the link where it had stopped.

Important:
If you wish to stop crawling a given range of years and start a new process, you must empty the contents of the `links.txt` file (without deleting the file itself). Only in this way will the crawler start a new cycle from scratch, rather than picking up where it left off.


   
    

