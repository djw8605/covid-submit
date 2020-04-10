#!/usr/bin/env python
import htcondor
import getpass
import os
import subprocess



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
        # Have to use the condor_submit interface because of scitokens and wrapper stuff
        submit_file = ""
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        subprocess.call("condor_submit covid.submit", shell=True)
        print("Submitted 1000 jobs")
    else:
        print("More than 1000 idle jobs: {}".format(idle_jobs))

if __name__ == "__main__":
    main()
