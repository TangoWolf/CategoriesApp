# Categories App
A database and third party authorization web app for Udacity's Full stack nanodegree  

## Design
The design is pretty straightforward. There's a database with academic subjects, and related courses.  
The main screen shows the subjects, a button to add a new subject, and a link to login/logout.  
Each subject's individual screen shows that subjects courses, a button to add a new course, and the login/logout link.  
When you're logged in, you can also edit or delete any subjects or courses you've created.

## Instructions

Download the data from the repository. Unzip the file, into a vagrant file used  
to spin up a virtual machine on your computer on which to run an instance of  
Linux to host the web app. In your command line, cd to your vagrant and run the following commands:  
"vagrant up"  
"vagrant ssh"  
"cd /vagrant"  
"cd catalog"  
"py database_setup.py"  
"py lotsofcategories.py"  
"py project.py"  
and then open a web browser, and navigate to "localhost:5000".
