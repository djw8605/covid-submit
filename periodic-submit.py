import htcondor
import getpass
import os



def main():
    # Get the number of submitted covid jobs
    # Get my username for the query
    username = getpass.getuser()
    schedd = htcondor.Schedd()
    query_result = schedd.query(constraint = 'Owner =?= "{}" && JobStatus == 1'.format(username), attr_list=["JobStatus"])
    idle_jobs = len(query_result)

    # If less than 1000 idle jobs, submit another 1000.  
    # We should always have from just below 1000 and 2000 idle jobs
    if idle_jobs < 1000:
        # Read in the submit file
        submit_file = ""
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        with open('covid.submit', 'r') as covid_submit:
            submit_file = covid_submit.read()
        
        # Submit the number
        sub = htcondor.Submit(submit_file)
        sub.setQArgs("1000")
        with schedd.transaction() as txn:
            sub.queue(txn)
        print("Submitted 1000 jobs")
    else:
        print("More than 1000 idle jobs: {}".format(idle_jobs))

if __name__ == "__main__":
    main()
