# ✨Instructions✨

## 🛠 Image without CMD (With manuel user input)
1. Before uploading the required files on an EC2 instance, create a directory named, for example, *Pinterest*.

2. Using the command below and provided you are at the same level as the *EC2-Ubuntu-20.04* folder, upload the files from your PC to the EC2 instance:
   
   **scp -i </path/my-key-pair.pem> ./EC2-Ubuntu-20.04/\* ubuntu\@\<public-dns>\:\<path/>**

   The path in the EC2 instance would normally be *~/Pinterest* where *Pinterest* is the directory created previously.

3. Log in to your EC2 instance.
4. Moving into the *Pinterest* directory, run the following command:
   
   **sudo docker build -t \<image-name> .**
   
5. The container can then be created using:

    **sudo docker container run -it --name \<container-name> --rm \<image-name>:latest**

## 💻 Automate input via CMD arguments

1. Steps 1. to 4. are similar as above.

2. However, in this case, if a volume is beforehand created and then mounted to a container, the new command would be:

   **docker container run --name testremote --rm -v \<volume-name>:/\<folder-in-container> \<image-name> arg1 arg2 ... arg18**

   This command will run the default arguments in the ***CMD*** part of the Dockerfile.

3. To add arbitrary inputs, the arguments should be provided as shown previously, that is, at the end of the last command in the same order as they are defined in the Dockerfile or the scraper will not work. The same number of input arguments should also be provided even if some of the inputs will be omitted depending on the answers from the previous questions.

4. The docker volune mounted on the container is essential so that data recorded in JSON files in past runs can be detected and read. In this way, new data/images can always be appended to the existing dataset without overwriting the latter.

5. As a side not, run the docker container in the foreground to check whether the arguments provided are valid. If any one of them is invalid, the codes will not move on but will be stuck in a loop of with "invalid input" messages. In the event that this occurs, the container will need to be stopped.
