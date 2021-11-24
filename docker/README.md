# ✨Instructions✨

1. 🛠 Before uploading the required files on an EC2 instance, create a directory named, for example, *Pinterest*.

2. 🛠 Using the command below and provided you are at the same level as the *EC2-Ubuntu-20.04* folder, upload the files from your PC to the EC2 instance:
   
   ***scp -i </path/my-key-pair.pem> ./EC2-Ubuntu-20.04/\* ubuntu\@\<public-dns>\:\<path/>***

   The path in the EC2 instance would normally be *~/Pinterest* where *Pinterest* is the directory created previously.

3. 🛠 Log in to your EC2 instance.
4. 🛠 Moving into the *Pinterest* directory, run the following command:
   
   ***sudo docker build -t \<image-name> .***
   
5. 🛠 The container can then be created using:

    ***sudo docker container run -it --name \<container-name> --rm \<image-name>:latest***
