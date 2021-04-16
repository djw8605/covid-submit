#!/usr/bin/env python
import htcondor
import getpass
import os
import subprocess

max_total_jobs = 20000
max_idle_single_core = 8000
max_idle_eight_core = 2000
max_idle_gpu_core = 1000

def main():
    # Get the number of submitted covid jobs
    # Get my username for the query
    username = getpass.getuser()
    schedd = htcondor.Schedd()
    #single_query_result = schedd.query(constraint = 'Owner =?= "{}" && RequestCPUs == 1'.format(username), attr_list=["JobStatus"])
    #total_jobs = len(single_query_result)
    #idle_jobs = 0
    #for job in single_query_result:
    #    if job['JobStatus'] == 1:
    #        idle_jobs += 1

    # If less than 8000 idle jobs, submit another 1000.
    # We should always have from just below 8000 and 9000 idle jobs
    #if idle_jobs < max_idle_single_core and total_jobs < max_total_jobs:
    #    # Read in the submit file
    #    # Have to use the condor_submit interface because of scitokens and wrapper stuff
    #    submit_file = ""
    #    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    #    subprocess.call("/usr/local/bin/condor_submit covid.submit", shell=True)
    #    print("Submitted 1000 single core jobs")
    #else:
    #    print("Decided to not submit more jobs: idle_jobs:{}, total_jobs:{}".format(idle_jobs, total_jobs))

    eight_query_result = schedd.query(constraint = 'Owner =?= "{}" && RequestCPUs == 8'.format(username), attr_list=["JobStatus"])
    total_jobs = len(eight_query_result)
    idle_jobs = 0
    for job in eight_query_result:
        if job['JobStatus'] == 1:
            idle_jobs += 1

    # If less than 2000 idle jobs, submit another 1000.
    # We should always have from just below 2000 and 3000 idle jobs
    if idle_jobs < max_idle_eight_core and total_jobs < max_total_jobs:
        # Read in the submit file
        # Have to use the condor_submit interface because of scitokens and wrapper stuff
        submit_file = ""
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        subprocess.call("/usr/local/bin/condor_submit covid.submit -append request_cpus=8 -append request_memory=15000 -append arguments=8 -append priority=10", shell=True)
        print("Submitted 1000 eight core jobs")
    else:
        print("Decided to not submit more eight core jobs: idle_jobs:{}, total_jobs:{}".format(idle_jobs, total_jobs))
    
    gpu_query_result = schedd.query(constraint='Owner =?= "{}" && RequestGpus == 1'.format(username), attr_list=["JobStatus"])
    total_jobs = len(gpu_query_result)
    idle_jobs = 0
    for job in gpu_query_result:
        if job['JobStatus'] == 1:
            idle_jobs += 1

    # If less than 1000 idle jobs, submit another 1000.
    # We should always have from just below 1000 and 2000 idle jobs
    if idle_jobs < max_idle_gpu_core and total_jobs < max_total_jobs:
        # Read in the submit file
        # Have to use the condor_submit interface because of scitokens and wrapper stuff
        submit_file = ""
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        subprocess.call("/usr/local/bin/condor_submit covid.submit.gpu --append priority=10", shell=True)
        print("Submitted 1000 gpu jobs")
    else:
        print("Decided to not submit more gpu jobs: idle_jobs:{}, total_jobs:{}".format(idle_jobs, total_jobs))


    

if __name__ == "__main__":
    main()
