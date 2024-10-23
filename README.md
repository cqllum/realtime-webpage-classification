# Real-Time Webpage Classification and Analysis

This project is my  **Real-Time Webpage Classification and Analysis** project to demonstrate Python classification and web crawling in tandem with a real time streaming on Apache Kafka.

This application leverages the Python to scrape, analyse, and classify websites in real-time. Built for scalability and efficiency, it offers a robust pipeline for understanding web content and extracting meaningful insights.

The application will continuously crawl new links that are picked up on pages that are sent to the queue, and new domains can be added to the crawler queue when they enter the To Process topic in Kafka.

  
## Features

- **Real-Time Analysis**: Scrapes websites and analyses content on-the-fly.
- **Keyword Extraction**: Identifies relevant keywords from webpage content.
- **Website Classification**: Classifies websites into various categories (e.g., technology, health, finance).
- **Kafka Integration**: Utilizes Kafka for message brokering, ensuring reliable data flow and processing.
- **Extensible Pipeline**: Easily add or modify processing steps for custom workflows.

## Demonstration
Below is an exaxmple of instruction the process to crawl https://www.example.com

**Adding a domain to Kafka Topic:**
```py
> python -m src.kafka_push_domain --domain https://www.example.com

Domain https://www.example.com sent to domains_pending_analysis topic
```

This will then send `https://www.example.com` to the Queue, and will be picked up by the `kafka_monitor.py` application automatically.

**Kafka Monitor - Kafka Topic:**

This script can be constantly running to pickup new services and push data to a processed topic
```py
> python -m src.kafka_monitor
```
Outputs:

![alt text](https://i.imgur.com/jxlXw3R.png)

**Processed Output Data (JSON)**

Data will now enter the topic, containing the full JSON structure of the processed outputs of what was scraped from the site.
![alt text](https://i.imgur.com/JH8rRRv.png) 

#### Example JSON Outputs:
```json
{
  "success": true,
  "url": "https://www.example.com",
  "hostname": "www.example.com",
  "title": "Example Domain",
  "meta_description": "No Description Found",
  "images": [],
  "internal_links": [
    "link found on site.."
  ],
  "domain_info": "whois info here...",
  "keywords": [
    "keyword here..",
  ],
  "category": "uncategorized",
  "description": "This site is about blablabla",
  "legitimacy": "legitmate"
}

```

#### Now what?
The script will now endlessly crawl through links that it comes across on every web page that it discovers. It will only crawl a page once per run time, as it adds the domains to a list within the runtime of the application.


## Getting Started

To get started with this project, follow the steps below:

### Prerequisites

- [Python](https://www.python.org/) (version 3.7 or higher)
- [Apache Kafka](https://kafka.apache.org/) (or access to a Kafka cloud service like Confluent Cloud)
- Required Python packages (install via `pip`)

#### Installsation
```bash
git clone https://github.com/cqllum/realtime-webpage-classification.git
cd realtime-webpage-classification
pip install -r requirements.txt
```

Once you have installed the requirements, you are ready to go, now you will need to ammend the config/config.json file with your Kafka broker details, and also need to ensure the topics that are in the broker are available, as this script doesn't have the capability to create them if they don't exist. You can read more about the Kafka setup below


You will then need to ensure that you have the application continuously running, this can be done with the script:
```py
python -m src.kafka_monitor
```

By doing this, you will now have your Python script listening for new domains that come into the topic. Feel free to modify it accordingly for your own purposes.

To add new domains to the queue, you are able to simply push the following data to the pending topic with the following data
```json
{"domain": "https://example.com"}
```
Alternately, there is a tool in this application that can help you add data to the topic, and can be done with the following:

```py
python -m src.kafka_push_domain --domain https://www.example.com
 ```


## Architecture & Lineage


#### Domain Crawling and Queue Management

This application includes a powerful domain crawling feature that systematically explores a given website to discover and process all internal pages.

1. **Crawling the Domain**: When a domain is scraped, the application analyzes the webpage to extract all internal links. Internal links are defined as links that point to pages within the same domain, ensuring that the crawler does not wander off to external websites.

2. **Adding to the Queue**: Once the internal links are identified, they are added to the Kafka queue for further analysis. This allows the system to keep track of which pages need to be processed, ensuring no page is overlooked.

3. **Avoiding Duplicates**: The application maintains a record of processed URLs to prevent duplicate processing. If an internal link has already been crawled, it will not be added to the queue again, optimizing resource usage and improving efficiency.

4. **Continuous Monitoring**: The system continuously monitors the Kafka queue, ensuring that all new pages are processed in real-time, enabling timely analysis and data collection.

This crawling mechanism enhances the application's ability to gather comprehensive data from a website, providing a deeper understanding of its structure and content.



![alt text](https://imgur.com/BMulvRl.png)


`Source Topic` - **domains_pending_analysis** - The queue of domains that will be processed. Input values are JSON Format as follows:
```json
{'domain': 'example.com'}
```

`Consumer Group` - **domain-monitor-group** - This is the consumer group that is listening to the Source Topic.

`Processed Topic` - **domains_completed_analysis** - The finalised output of domains that have been processed.
```json
{'domain': 'example.com'}
```



## TLDR
Essentially, when a message enters the Source Topic of the correct format, this application will begin to crawl the domain to gather needed data for processing in which the Kafka Consumer Group will pick it up for processing.. Domain internal links will be added to the queue, to continuously crawl endless pages of websites and identify key data about them, all outputs will be sent to the **Processed Topic**. 



## Kafka Setup

Included in this application, you will find a `config.json` file, in which you will put your Kafka broker details as well as source/destination topics for the application, structured like so:
```json
{
    "kafka": {
        "brokers": ["broker:9092"],
        "pending_topic": "domains_pending_analysis",
        "completed_topic": "domains_completed_analysis",
        "security_protocol": "SASL_SSL",
        "sasl_mechanisms": "PLAIN",
        "sasl_username": "SECRET_USERNAME_HERE",
        "sasl_password": "SECRET_PASSWORD_HERE",
        "session_timeout_ms": 45000
    }
}
```

It utilises the **SASL_SSL** security protocol, please ensure your Kafka brokers support credentials via this method, any modifications on security protocol may require some additional changes to the application code.



**You may get a free set of Kafka brokers, as I had done in this project from Confluent.cloud like so**

1) Sign up to Confluent Cloud & add a payment method to redeem the free trial.
2) Navigate to the environment creation area ( https://confluent.cloud/create-environment ) and create your free environment.

![Imgur](https://imgur.com/i1tvIUv.png)


3. Once you have created your cluster etc, navigate into your Cluster

4) Once you have your environment, navigate to your API keys

![Imgur](https://imgur.com/gdhBXtm.png)

5) Create a new set of API keys, then take note of the **KEY** and **SECRET**. 
6. Navigate to your Cluster Settings (shown under the API keys in the previous image)
7. Take note your Broker Bootstrap server

![Imgur](https://imgur.com/cKSqRro.png)

8. Navigate into Topics, and create two new topics that will be used for this project, this is up to you, but by default in the config.json, you will find it to be:
- **domains_pending_analysis** - Processing Queue
- **domains_completed_analysis** - Outputs of processing

9. Now that you have the **KEY**, **SECRET**, **BROKER BOOTSTRAP SERVER**, and have created the **Topics**, you can ammend the `config.json` meantioned previously.



## Application File Descriptions
Below you will find descriptions on the hierarchy of files in this project 
### File tree
```
dir/ 
── src/
│   ├── __init__.py               # Marks the directory as a package
│   ├── main.py                    # Main orchestrator
│   ├── scraper.py                 # Web scraping logic
│   ├── processor.py               # Text processing functions
│   ├── classifier.py              # Website categorization logic
│   ├── scam_classifier.py         # Scam detection logic
│   ├── kafka_push_domain.py       # Kafka producer for domains
│   └── kafka_monitor.py           # Kafka consumer and producer management
│
├── config/
│   └── config.json                # Kafka broker credentials and other config
│
├── requirements.txt               # List of dependencies
│
├── README.md                      # Project overview and instructions
│
└── .gitignore                     # Files and directories to ignore in Git

```

### File purposes
- `main.py`: This is the main orchestrator that handles the overall flow of the application, including scraping and processing the website.
- `scraper.py`: Responsible for web scraping, it gathers the initial data from the target websites.
- `processor.py`: Contains functions for processing the text, extracting keywords, and summarizing the content from the scraped data.
- `classifier.py`: Implements the logic for categorizing the website based on its content.
- `scam_classifier.py`: Checks the legitimacy of the site to help identify potential scams or fraudulent sites.
- `config.json`: Kafka broker credentials.
- `kafka_push_domain.py`: Takes a domain argument for sending a domain into the Kafka topic for processing
- `kafka_monitor.py`: Manages the Kafka consumer and producer, processing domains from the pending topic and publishing results to the completed topic.


## Some to dos for inspiration:
- Integrate the existing code snippet frrom from the file (`visualizer.py`) which is found in this codebase, to create word clouds as png base64 uri paths to introduce onto a webpage, showing a summary of key words by hostname.
- Processing / Joining data with Apache Flink or Airflow to transform the data and join it with other real time data sets.
- Plotting the data on graphs within tools like Grafana, and watch how the tool quickly spreads across the web and gathers summarised keyword data.
- Perhaps do some machine learning on the kind of sites out there


### ⚠ Disclaimer
Please use this application responsibly and ensure you have permissions from the web-masters of the applications you are crawling from. In future, the next steps is to also consider the `robots.txt` of the pages that it comes across. Also be considerate of your own bandwidth as this can be quite exhausting if you set of the bot to crawl heavy pages. The purpose of this application is to demonstrate how crawlers typically behave across the internet, and what kind of data you can retrieve from websites, and how that it can extensively fetch data for one domain after the other. This application also demonstrates the use of real time data instructions and also self learning application links, all within Apache Kafka that allows this to work seamlessly. Please use this application for Educational purposes only, and allow it to assist you in your understanding of crawling web pages for data.









