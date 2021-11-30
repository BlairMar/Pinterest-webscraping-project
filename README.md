# Pinterest-webscraping-project
[![AiCore](https://img.shields.io/badge/AI%20School-AiCore-orange)](https://www.theaicore.com/)

![AiCore - Specialist Ai & Data Educator](./images/AiCore-logo.png)

## About this project 📑

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

This project is part of the curriculum of the AiCore BootCamp. The aim of this project is to automate the scraping on the [Pinterest](https://www.pinterest.co.uk/ideas/) website. The entire scraper is written in the ***Python*** programming language. The scraper was also containerized using docker and also deployed on EC2 for scheduling.

![Explore Pinterest](images/Pinterest-root-page.png)

## People in the project 👩‍💻

![GitHub Contributors Image](https://contrib.rocks/image?repo=BlairMar/Pinterest-webscraping-project)

The contributors of this project are:
| Full Name | Email |
| ----- | ----- |
| Pascal Weiliam Li Poo Kim | paswei98@gmail.com |
| Luke Gardiner | Luke.gardiner.95@gmail.com |
| Daniel Zakaiem | danielzakaiem@yahoo.co.uk |

Our supervisor and instructor for this project is *Blair Martin* (blair@theaicore.com).

## Libraries to install 📚

The ***Python*** libraries that are required to make the scraper work are:
- beautifulsoup4 - [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- requests - [Requests: HTTP for Humans](https://docs.python-requests.org/en/latest/)
- boto3 - [Boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- selenium - [Selenium with Python](https://selenium-python.readthedocs.io/)
- tqdm - [tqdm](https://github.com/tqdm/tqdm)
- urllib3 - [urllib3](https://urllib3.readthedocs.io/en/stable/)
- pandas -[pandas](https://pandas.pydata.org/)
- sqlalchemy -[The Python SQL Toolkit and Object Relational Mapper](https://www.sqlalchemy.org/)


## Brief overview how to use the scraper

[![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg)
[![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)
[![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://code.visualstudio.com/)

1. When running the main Python script in VS code, [pinterestScraper.py](src/pinterestScraper.py), a web browser window will appear. In this project, the web browser engine used for scraping is **Google Chrome**.

2. In the terminal of VS code, a list of available categories on the webpage will be printed. The users will be asked to choose how many categories that they would want to scrap and also which category(ies).

3. The users have the flexibility to choose whether to download the images or not, and if they want to download the data, they also have the option to choose whether they want to download the data locally on their PC or directly to an ***AWS S3 Bucket***, provided that the users have public buckets to upload to. The data do not consist only of images but also JSON files which contain the link to each image, description, follower count, etc.

4. Once all the choices have been made, the scraper can be left to perform its task.

5. At the end of data collection, the user will be asked whether tables for RDS should be created. If the user answers yes, the user can then choose between remote ***AWS RDS*** or local RDS. The user will need to provide his/her credentials for each section.

6. *pgadmin* (postgres) was the application used to see the created tables both remotely and locally. If other SQL DB should be used, this should be changed in the codes in the function where the script is connected to the RDS.

## Deploying the scraper in a Docker container on EC2

[![Docker](https://badgen.net/badge/icon/docker?icon=docker&label)](https://https://docker.com/)

* The EC2 image that should be used to use Docker and for testing is the *Ubuntu (focal) 20.04*. It will not work on the *AMI Linux 2 Free Tier*.

* It is important to note that the codes in the [pinterestScraper.py](docker/EC2-Ubuntu-20.04/pinterestScraper.py) are slightly different from the Python script run locally. This is just the way the codes were implemented to work on the EC2 instance and Docker.

* Although, it is preferable to save the data from the scraper in a S3 bucket, it is still possible to save it on the EC2 instance and access it, provided a volume is mounted on the container.

* More info about deployment on EC2 can be found in the **docker** folder.

