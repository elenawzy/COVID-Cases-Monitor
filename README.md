# Assignment 2 Documentation

## Instructions to run app

We implemented a flask API that has an html and CSS frontend to upload files and apply filters to retrieve data.
First, after pulling the files from github, the necessary modules need to be installed (pip install):
1. pandas
2. numpy

To run the app, navigate in the terminal to COVIDMonitor (cd COVIDMonitor), and then run “python main.py” in the terminal. The app is now running on localhost:5000 or 127.0.0.1:5000 (the link that is given in the terminal)

Going to the link is the front page and you can choose a file to upload and click the blue “Submit Data File” to upload the file into a local “csvfiles” folder. You can upload as many files as you would like, and any duplicate files will be updated with the newest upload. The added files can be viewed in the local file directory of the project. We have coded it assuming that the file submitted is either a time series file or daily report file as specified in the handout, so they will be sorted into “dailyreports” folder or “timeseries” folder (subfolders of “csvfiles”). If the daily report file is inconsistent with the 06-05-2020.csv file as specified in the handout, then an error will occur trying to parse the data, so the file must be the recent layout.

For the user to request info, they first will need to choose if they want to see time series data or daily report data, and pressing one of the black “filter” buttons will redirect to a filter page. The filtering options for times series data and daily reports data are different. 

In the time series filtering page, the user can enter province, country, start date, and end date in their textboxes, and then choose a format to be exported. The country and province entered are case-sensitive so the user has to capitalize the first letter. Any misspell or not formatted inputs for country and province will result in the inability of filtering out the desired data. The user can also leave the province and country textboxes blank or enter multiple provinces and countries as long as they separate each country/province using “;”. For the filtering of time period, the user can leave both start date and end date textboxes blank, fill out the start date for search on a single day, or fill out both the start date and the end date for multiple days time period. We assume that the user follows the format rules of “mm/dd/yyyy”, and the fact that the end date must be after(larger than) the start date. 

The daily reports filtering page includes everything that time series filtering page has, and two additional filters. One new textbox to enter the combined keys of the location (ie. Adair, Iowa, US). This combined keys option also allows multiple locations as long as they are separated by “;”. Another new option is for selecting the data content (Deaths, Confirms, Active, Recovered). Only one of the 4 options can be selected each time. 

Once hitting the blue “Submit filters” button, you will be redirected to a page that displays the data in either csv, json or text format (text format is just an html table). Additionally, a copy of the filtered data is also saved in the “resultfiles” folder inside “COVIDMonitor”. It is important to note that only one of each file type can be saved in the folder, since multiple files with the same file type will have the same file name, which results in a replacement of the files.


## Unit Tests
Running tests are done the same way as the starter handout, with:
```
pytest --cov-report term --cov=COVIDMonitor tests/unit_tests.py (in the root directory)
```
This will also show the coverage, which is an overall 81%.

## Pair Programming

#### Feature 1&2: 
We decided to pair program the whole process of uploading files and updating files with Elena as the driver and Gavin as the navigator. This didn’t include parsing the csv because just figuring out how to get form information and how to add the files to our directory was very new to us, so we spent a good amount of time just figuring this out together for pair programming.

##### Process
We didn’t know if we wanted to do an API with Flask or just a CLI so we decided to take our own time researching which would be a better fit, and then start designing after. We decided to do a Flask API since Flask comes with many tools to design a REST API.
- Checkpoint 1: Make endpoints and have them able to return html pages properly
- Checkpoint 2: Allow file upload
- Checkpoint 3: Save files 
- Checkpoint 4: Have name-checking for files to sort them into separate folders (in local repo)

##### Pros and cons
The roles were the same for the whole feature, since we found it hard to switch roles after only 30-60 min. 
The best part of pair programming for this part was to have a navigator watching and looking out for potential mistakes, or giving tips and maybe what would be a better implementation. Checkpoint 3 gave us a bit of trouble because we weren’t sure exactly how we could sort files, so I (Elena) just added them into a new folder, but then the name-checking feature for checkpoint 4 wasn’t fulfilled. Gavin was able to suggest making more separate folders, so we could sort them into those and also have later data parsing functions find the right files easily. Taking breaks in between and thinking about each other’s code and approaches helped a lot to get back into coding easily, because we could discuss what would maybe be a better implementation, or how to solve an upcoming problem. Having a navigator really helps to see the code from a general point of view, and guide the driver when they are confused about a more specific piece of code. 

Pair programming let us debug our code a bit quicker since we were able to both look at what might be going wrong. The code seemed a little bit cleaner than the code I usually write, mainly because there were 2 eyes looking at how to structure the design. 

The process was a bit slow, and I found that it would have been just faster if we thought of designs ourselves, and then compared with each other, rather than researching together. I felt a little bit restricted since every idea I thought of I had to run through my partner, rather than have the whole thinking process to myself, and getting feedback after. I am still unsure whether I would like to do this again since I like mapping out a design myself first since I feel like I have more control, even though pair programming helped make a solution that was probably a bit more concise. I learned that definitely talking to a partner at some point about problems is something that is very helpful for code design and debugging.

#### Feature 3:
Since the reading and parsing of data is directly connected to uploading files and receiving user inputs on filtering data, we decided to work on the section of querying data together, with Gavin as the driver and Elena as the navigator.

###### Process
Since both of us did not take CSC343 yet, we don’t want to force ourselves to create databases for the data. Therefore we decided to use pandas dataframe to store the data. We decided to create 2 data classes for the two types of input file. Since the two classes have very similar structures, we decided to use the abstract factory design pattern, which uses a single abstract class as the base for both classes.
- Checkpoint 1: Create abstract class/interface as the base of the two data classes
- Checkpoint 2: Create the two subclasses of the abstract class and override all abstract functions
- Checkpoint 3: Import the classes into routes.py
- Checkpoint 4: Connect the user input we obtained and use it for the read/query/export functions

###### Pros and cons
The process of pair programming for this feature worked very well. During the designing phase, we are able to provide different solutions to how to implement the class and how they are formatted. Using the abstract factory method to implement the data classes is one of the results that came from the discussion during the designing phase. Since Elena is the driver for the file upload feature and also worked on the frontend page, she is very helpful during the checkpoint 3 and 4, where we have to obtain and use user input for backend functions. I am not very familiarized with flask and its format, therefore having her being the navigator of these checkpoints greatly reduced my time spent on researching. 

On the other hand, the initial phase of coding the data classes had less benefits from pair programming, since it is not connected to any previous code Elena had done. Coding process is often slower than coding alone, which is one of the few cons pair programming has. However, it is still beneficial in the aspect of error checking and code formatting. 

## Program Design

#### Abstract Factory
We used the abstract factory design pattern for the two parseData files (parseDataTimeSeries.py and parseDataDailyReport.py) , which holds data classes with reading, querying and exporting functions. Since the two data classes (time series data and daily report data) are structurally very similar and also share many similar functions, we decided to create an abstract parent class for these data classes. This allows us to simplify and streamline the data classes, which allows easy implementation for additional data classes in the future. 

#### REST API
Flask is a framework that supports RESTful app design and below are some aspects of REST that were implemented into our API:
- Client-Server: We had a clear separation between the client and server side, with python files as our backend, and html files as our frontend. In the API, we would render_template any html files that need to be served, or return any csv or json files. The client side is on our browser, and the server side is on Flask. This made it really easy to focus on coding specifically frontend or backend, and reduced confusion when figuring out if a problem was from the frontend or backend. 
- Uniform Interface: The client communicated to the server with GET and POST requests, while the server served html/csv/json files with the appropriate response code. These resources are saved into the local repo, and are served when requested for. We also made an error handler, to give proper messages to the client if something goes wrong. The API does not need to change whether we’re on a laptop or a mobile phone (assuming that this API is deployed).
- Stateless: The server does not store any info that the client sends to it. It will take in a file and then parse it into files of the local directory with some other python modules that were made. The information required to handle a GET request for information would not be taken from the server, but from the local files saved. If a client requests a file, the server doesn’t need to remember that they uploaded a file earlier, it just needs to take the file in the local repository and serve it to the client.
- Caching: Since our app is fairly simple and caching would not help the performance that much, we did not implement it, but did consider how it would be implemented. We would use the Flask-Caching extension to implement simple caching. This would let a bigger scale version of this API to be more responsive and perform faster. You would need to:
1. import flask-caching in the beginning of the file
2. initialize the caching with app.config\[CACHE_TYPE\] = “simple” and cache.init_app(app)
3. Add @cache.cached(timeout=10) after any @app.route() call (however many timeout seconds)
- Layered: Since this project was relatively simple, we did not implement any layering other than caching, but Flask provides many modules that can implement aspects like authentication, monitoring, load balancing, etc. Choosing Flask for API projects can be easily layered.

## Code Craftsmanship:

For the front end html, atom-beautify was used to format the code nicely in a readable way (with the atom IDE). Atom’s CSS linter was also used for checking the css code. 
For the python code,  Prettier- Code formatter extension is used in VS Code for the automatic formatting and cleaning of code. Pylint was used for code analysis and standardization of the code structure. 
