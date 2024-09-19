## DTC Re Execution App Documentation

This application serves as a tool to re-execute glue jobs and procedures related to consumer data. This tool is designed to streamline the process of rerunning jobs and procedures. This will allow anyone with the proper access to execute specific days or date ranges for all pipelines. Once finished the user can then excute the procedure to move the data from mud_room to clean room.

### Glue Jobs

Glue jobs are python scripts in AWS that load and proccess dtc data from s3 and writes it to our mud_room database in redshift. This app gives you the ability to re-run these glue jobs with a simple click of a button. The app provides a list of available jobs which you can choose from. 

### Procedures

Procedures in this context refer to sql code that extracts, stores and propegates out user data into our vault then pushes the clean records to the clean_room database. This app allows you to re-run these procedures. A list of available procedures is provided for you to select and execute.

### How to use

1. **Select the job type**: Choose between 'Glue jobs' and 'Procedure' based on the operation you want to perform.
2. **Select the job or procedure**: Depending on the job type selected, the app will provide a list of available jobs or procedures. Select the one you wish to execute.
3. **Select the table(s)**: For some jobs, you will be asked to select the table(s) to run the job on.
4. **Select the date or date range**: Some jobs might require you to provide a specific date or date range.
5. **Submit**: Click on the 'Submit' button to execute the job or procedure.

The app will then run the selected job or procedure and display the result on the page.

### Issues

If there are any issues reach out to Adam Dion