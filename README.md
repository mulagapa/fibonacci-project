**Running the application**
    The application already contains the docker file. By running the docker file you will be able to deploy and use the application with out the need for external 
    dependencies.

    1. Make sure the system has docker installed.
    2. By running 'docker-compose up' command it will run the application on the localhost.

    If the docker command is not working by running the flask application the applicatio will still run.

**Project Explanation**
    The project is a way of displaying the first n fibonacci numbers.
    The first page contains a text box in which users can enter the value of n. 
    upon clicking the submit button after entering the n value. 
    The user will be redirected to a second page where he the first n values will be displayed.

**Features**

    1. We are storing the values in a mysql data base. so if a user enters the same value again it doesn't have to be calculated it can be displayed directly
        by retrieving the value from the database.
        
    2. We are also using a cache dictionary system in this application. Where we are storing the 5 most recently used values in the flask application. 
    
    3.The application also contains the docker files which will support the appication to be run on any cloud service such as aws or gcp easily.
    
    4. The front end part of the applications is stored on the templates folder.
    
    5. The application also sotre the values of the last 2 number of n for example if the value of n is 5, it will store the value for both 3 and 4, while     
       calculating for 5. This is a way of dynamic optimsation generallly followed while calculating fibonacci. In this case since we are already calculating the 
       value of 3 and 4 it is better to store the values so that if a user asks them they can be provided.
    
**Improvements**

    1. In this application i was using basic dictionary as my cache but it can also be used with redis (key values pair )or mysqlite (relational) to improve the         time taken for the application to retrieve values. Instead of accessing the values from data base it can be taken from the cache server in less time.
    
    2. This application already contains unit test but also adding integration tests we will be able to support testing the application better.

    
