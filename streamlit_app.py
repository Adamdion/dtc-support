from pathlib import Path
import streamlit as st
import requests
import datetime
import json

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)


def runAPI(job_name='', table_names=[], specific_date='',date_range=(today,tomorrow),run_type='',job_id=None):
    """
    Function to call API to start reloads
    """
    # Define the headers
    headers = {'Content-Type': 'application/json'}
    
    if run_type == 'Status':
        print(f"IN SATUS: job: id:{job_id}, name:{job_name}")
        response = requests.post("https://04ktu24fr2.execute-api.us-west-2.amazonaws.com/DEV/job/status", headers=headers, json={"job": {'id':job_id,'name':job_name}})
        print(response)
        return response.json()
    
    elif run_type == 'Start':
        specific_date, date_range = dateFormatting(specific_date,date_range, job_name)
        # Format the API body
        api_body = {
            "job": {
                "name": job_name,
                "date_range": f"{date_range}",
                "list_of_dates": "[]",
                "specific_date": f"{specific_date}",
                "table_list": str(table_names)  # Convert list to string
            }
        }
        response = requests.post("https://04ktu24fr2.execute-api.us-west-2.amazonaws.com/DEV/job/start", headers=headers, json=api_body)

        return response.json()


def load_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

def main():
  # Add a selectbox to the sidebar:
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Home", "Documentation"])

    if page == "Home":
        run_main_page()  # The function to run the main page of your app
    elif page == "Documentation":
        st.title('Documentation')
        st.markdown(load_markdown_file("documentation.md"), unsafe_allow_html=True)

def run_main_page():
    """
    Main for streamlit app to Re-Execute glue jobs and Procedures
    """
    st.title("DTC Re Execution App")
    glue_ran = False
    job_id = ''

    # Read in json of jobs and tables
    with open('execution-data.json', 'r') as f:
        results = json.load(f)
    job_to_tables = results['glueJobs']
    table_to_procedures = results['procedures']

    # Get job names from the keys of the dictionary
    job_names = list(job_to_tables.keys())
    job_type = st.radio("Select job type", ("Glue jobs", "Procedure"))

    # Display content based on selected job type
    if job_type == "Glue jobs":
        selected_job = st.selectbox("Select Job", job_names)  

        table_names = job_to_tables[selected_job]

        if selected_job in ['ejgallo-lake-dtc-create-tables-antares', 'ejgallo-lake-dtc-create-tables-mudroom-um-exports',
                             'ejgallo-lake-dtc-create-tables-zinrelo-disengaged','ejgallo-lake-dtc-moosy-subscribers-to-mudroom',
                            ' ejgallo-lake-dtc-create-tables-mudroom-um-exports']:
                if st.button("Submit"):
                    result = runAPI(selected_job, [],None,(today,tomorrow),'Start')
                    glue_ran = True
                    st.write(result)
        elif selected_job == 'ejgallo-lake-dtc-beaconstac-to-mudroom':
            selected_table = st.multiselect("Select Table", table_names)

            if st.button("Submit",key="button1"):
                result = runAPI(selected_job, selected_table, None, (today,tomorrow),'Start')
                glue_ran = True
                st.write(result)
        else:
            # Get the table names for the selected job
            table_names = job_to_tables[selected_job]

            selected_table = st.multiselect("Select Table", table_names)

            selected_date = st.date_input("Select Date", None)

            selected_date_range = st.date_input('Select Date Range', (today,tomorrow))

            if st.button("Submit", key="button1"):
                result = runAPI(selected_job, selected_table, selected_date, selected_date_range,'Start')
                glue_ran = True
                st.write(result)
                job_id = result.get("JobRunId")
                print(f'Early Job ID: {job_id}')

        st.subheader("Chcek Status")
        if glue_ran:
            print(f"Job Ran: {result['JobRunId']}")
            # job_id = st.text_input("Job Id",value=result['JobRunId'])
            # job_id = result['JobRunId']
            print(f"job_id: {job_id}")
        # else:
        #     job_id = st.text_input("Job Id")

        if st.button("Submit", key="button2"):
            print(f"Job ID: {job_id}")
            # Checks status
            if job_id != '':
                result = runAPI(job_name=selected_job,run_type='Status',job_id=job_id)
                st.write(result)
            else:
                st.error("Run a glue job first")

    elif job_type == "Procedure":
        source_names = list(table_to_procedures.keys())

        st.write("Display procedure content here")
        selected_source = st.selectbox("Select Job", source_names)  

        procedure_names = table_to_procedures[selected_source]

        selected_table = st.multiselect("Select Table", procedure_names)
        if st.button("Submit"):
            result = runAPI("ejgallo-lake-dtc-run-redshift-procedures", selected_table, None, (today, tomorrow))
            st.write(result)

def dateFormatting(specific_date,date_range, job_name):
    """
    Function to format the dates to pass into apu for reloads
    """
    if specific_date is None:
        specific_date = "''"
    else:

        if job_name in ['ejgallo-lake-dtc-create-tales-luxary-AMS-EWINERY','ejgallo-lake-dtc-moosy-sweepstackes-to-mudroom']:
            specific_date = specific_date.strftime('%Y/%m/%d')
        elif job_name in ['ejgallo-lake-dtc-create-tables-sfmcdv-to-mudroom','ejgallo-lake-dtc-create-tables-sfmcde-to-mudroom','ejgallo-lake-dtc-create-tables-sfmc-to-mudroom']:
            specific_date = specific_date.strftime('%Y-%m-%d')
        else:
            specific_date =specific_date.strftime('%Y/%#m/%#d')


        # selected_date = specific_date.zfill(2)

    if date_range[0] == today and date_range[1] == tomorrow:
        date_range = {}
    else:
        date_range = {"start": date_range[0].strftime('%Y/%#m/%#d'), "end": date_range[1].strftime('%Y/%#m/%#d')}
    
    return specific_date, date_range

if __name__ == "__main__":
    main()