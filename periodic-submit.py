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
    single_query_result = schedd.query(constraint = 'Owner =?= "{}" && JobStatus == 1 && RequestCPUs == 1'.format(username), attr_list=["JobStatus"])
    idle_jobs = len(single_query_result)

    # If less than 8000 idle jobs, submit another 1000.
    # We should always have from just below 8000 and 9000 idle jobs
    if idle_jobs < 8000:
        # Read in the submit file
        # Have to use the condor_submit interface because of scitokens and wrapper stuff
        submit_file = ""
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        subprocess.call("/usr/local/bin/condor_submit covid.submit", shell=True)
        print("Submitted 1000 single core jobs")
    else:
        print("More than 1000 idle single core jobs: {}".format(idle_jobs))

    eight_query_result = schedd.query(constraint = 'Owner =?= "{}" && JobStatus == 1 && RequestCPUs == 8'.format(username), attr_list=["JobStatus"])
    idle_jobs = len(eight_query_result)

    # If less than 2000 idle jobs, submit another 1000.
    # We should always have from just below 2000 and 3000 idle jobs
    if idle_jobs < 2000:
        # Read in the submit file
        # Have to use the condor_submit interface because of scitokens and wrapper stuff
        submit_file = ""
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        subprocess.call("/usr/local/bin/condor_submit covid.submit -append request_cpus=8 -append arguments=8 --append priority=10", shell=True)
        print("Submitted 1000 eight core jobs")
    else:
        print("More than 1000 idle eight core jobs: {}".format(idle_jobs))
    

    

if __name__ == "__main__":
    main()
