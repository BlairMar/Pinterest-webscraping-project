# ✨Instructions✨

## 🛠 Setting up the container on EC2
1. Before uploading the required files on an EC2 instance, create a directory named, for example, *Pinterest*.

2. Using the command below and provided you are at the same level as the *EC2-Ubuntu-20.04* folder, upload the files from your PC to the EC2 instance:
   
   **scp -i </path/my-key-pair.pem> ./EC2-Ubuntu-20.04/\* ubuntu\@\<public-dns>\:\<path/>**

   The path in the EC2 instance would normally be *~/Pinterest* where *Pinterest* is the directory created previously.

3. Log in to your EC2 instance.
4. Moving into the *Pinterest* directory, run the following command:
   
   **sudo docker build -t \<image-name> .**
   
5. The container can then be created using:

    **sudo docker container run -it --name \<container-name> --rm \<image-name>:latest**
    
    However, the above command is valid only if the *pinterestScraper.py* in the *EC2-Ubuntu-20.04* folder is similar to that in the *src* folder, that is, with the input prompt codes and not using arguments (see below for more details regarding predefined arguments for automating the run).

## 💻 Automate input via CMD arguments

1. Steps 1. to 4. are similar as above.

2. However, in this case, if a volume is beforehand created and then mounted to a container, the new command would be:

   **sudo docker container run --name testremote --rm -v \<volume-name>:/\<folder-in-container> \<image-name> arg1 arg2 ... arg18**

   This command will run the default arguments in the ***CMD*** part of the Dockerfile. The above command is found in the *run_container.sh* file which should normally be the file to run.

3. To add arbitrary inputs, the arguments should be provided as shown previously, that is, at the end of the last command in the same order as they are defined in the Dockerfile or the scraper will not work. The same number of input arguments should also be provided even if some of the inputs will be omitted depending on the answers from the previous questions.

4. The docker volune mounted on the container is essential so that data recorded in JSON files in past runs can be detected and read. In this way, new data/images can always be appended to the existing dataset without overwriting the latter.

5. As a side note, run the docker container in the foreground to check whether the arguments provided are valid. If any one of them is invalid, the codes will not move on but will be stuck in a loop of with "invalid input" messages. In the event that this occurs, the container will need to be stopped.

## ⁉ Input Questions and Responses

It must be noted that not all the questions will be asked as it depends on the previous question response. However, it needs to be emphasized again that in the *run_container.sh* file, arguments should be provided and ordered as if all the questions were being asked even though previous response may be negative.

| Questions | Possible Responses |
| ----- | ----- |
| 1. How many categories of images do you wish to grab? 1 to *P*: | [1, P] |
| 2. Please select your desired categories. Separate your choices by commas. You have *x* choice(s) to make: | 1,2,3,...,P |
| 3. Would you like to download images for any of the selected categories? Y or N: | (Y or N) |
| 4. Please select which categories you would like to download images for. Enter your answer as a comma separated list: | (A or 1,2,..,N-1) |
| 5. Would you like to save any of your data/images to a remote bucket? Y or N: | (Y or N) |
| 6. Please enter the name of your desired S3 bucket | \<bucket-name> |
| 7. You have entered \<bucket-name> as your s3 bucket. | (Y or N)|
| 8. Which categories would you like to download to this bucket? Please enter your choice as a comma separated list: | (A or 1,2,...,N-1) |
| 9. Would you like to add to your existing data? Y or N: | (Y or N) |
| 10. How many times would you like to scroll through each category (The average is 12-15 images per scroll)?: | [1,M] |
| 11. Do you want to create an RDS? [Y/N] | (Y or N) |
| 12. Do you want a remote AWS RDS? [Y/N]: | (Y or N) |
| 13. User (default = postgres): | \<text> |
| 14. Password: | \<text> |
| 15. Port (default = 5433): | \<text> |
| 16. Database (default = Pagila): | \<text> |
| 17. AWS endpoint:  | \<text> |
| 18. Host (default = localhost): | \<text> |

where
- *P* is the total number of categories available on the root webpage
- *x* is the response from Q1
- A means all categories
- [] means a range of number you can choose from. Only **ONE** number should be selected
- () is equivalent to either or (but not both)
- 1,2,3,... denotes a list of integers can be provided
- \<text> indicates that arbitrary word should be provided

## Schedule scraping on EC2 instance
1. The command for running the docker container is found in the *run_container.sh* file.
2. All the arguments and parameters should be modified in this *.sh* file.
3. For the cron job, after typing *crontab -e*, put into the file for instance:

   **\* \* \* \* \* \* sh \<path\to\sh-file>**
