# Script for creating the model tree for vacuum case (no plasma, just magnetics)
# Alexei -- 07/2019
# Peter Buxton -- added username and checks before deleting -- Feb / 2021
# Peter Buxton -- added  copy_runs and warning_message  -- Feb / 2021
#/home/alexei.dnestrovskij/mdsplus/DB_nodes/Python_Scripts
from MDSplus import *
from numpy import *
import numpy as np
import mdsHelpers as mh
from imp import reload
reload(mh)
import getpass
import vacuum_node as v
user = getpass.getuser()
MDSplus_IP_address = '192.168.1.7:8000'  # smaug IP address

## look at /home/ops/mds_trees/ for inspiration
def delete(pulseNo, node):
    t = Tree('ASTRA', pulseNo, 'edit')

    # get the username of who wrote this run
    try:
        n = t.getNode(r'\ASTRA::TOP.' + node + '.CODE_VERSION:USER')
        user_already_written = n.data()
    except:
        user_already_written = user
    """
    # First warning if you are going to delete someone else' run
    if not(user_already_written==user):
        print('#####################################################')
        print('#  *** WARNING ***                                  #')
        print("#  You are about to delete a different user's run!  #")
        nspaces = 49 - len(user_already_written)
        spaces = ' '*nspaces
        print('#  ' + user_already_written + spaces + '#')
        print('#####################################################')

        print(' Proceed yes/no?')
        yes_typed = input(">>  ")
        if (yes_typed.lower()=='no')  or  (yes_typed.lower()=='n'):
            return
        while not(not(yes_typed.lower()=='yes')  or  not(yes_typed.lower()=='y')):
            print(' Error try again')
            yes_typed = input(">>  ")

        print(' To confirm type in: "' + user_already_written + '"')
        user_typed = input(">>  ")
        while not(user_already_written==user_typed):
            print(' Error try again')
            user_typed = input(">>  ")
        print(' ')

    # Second warning to confirm delete
    print('#####################################################')
    print('#  *** WARNING ***                                  #')
    print('#  You are about to delete data                     #')
    nspaces = 49 - len(user_already_written)
    spaces = ' '*nspaces
    print('#  ' + node + spaces + '#')
    print('#####################################################')
    print(' Proceed yes/no?')
    yes_typed = input(">>  ")
    if (yes_typed.lower()=='no')  or  (yes_typed.lower()=='n'):
        return
    while not(not(yes_typed.lower()=='yes')  or  not(yes_typed.lower()=='y')):
        print(' Error try again')
        yes_typed = input(">>  ")
    """
    # Delete
    t.deleteNode(node)
    t.write()
    t.close
    print(' Data deleted')


def create(pulseNo, node, descr):
    
    ###############################################################
    ####################    Create the tree    ####################
    ##############################################################    
    try:
        t = Tree( 'ASTRA', pulseNo, 'edit' )

        # get the username of who wrote this run
        try:
            n = t.getNode(r'\ASTRA::TOP.' + node + '.CODE_VERSION:USER')
            user_already_written = n.data()
        except:
            user_already_written = user
        if not(user_already_written==user):
            print('########################################################')
            print('#  *** WARNING ***                                     #')
            print("#  You are about to overwrite a different user's run!  #")
            print('########################################################')

            print(' Proceed yes/no?')
            yes_typed = input(">>  ")
            if (yes_typed.lower()=='no')  or  (yes_typed.lower()=='n'):
                return
            while not(not(yes_typed.lower()=='yes')  or  not(yes_typed.lower()=='y')):
                print('error try again')
                yes_typed = input(">>  ")

            print(' To confirm type in: "' + user_already_written + '"')
            user_typed = input(">>  ")
            while not(user_already_written==user_typed):
                print('error try again')
                user_typed = input(">>  ")
            print(' ')

    except:
        t = Tree( 'ASTRA', pulseNo, 'New' )

    # Second warning to confirm delete
    try:
        n = t.getNode(r'\ASTRA::TOP.' + node + '.CODE_VERSION:USER')
        user_already_written = n.data()
    except:
        user_already_written='noname'
    """
    if (user_already_written==user):
        print('#####################################################')
        print('#  *** WARNING ***                                  #')
        print('#  You are about to overwrite data                  #')
        print('#  ' + node + '       #')
        print('#####################################################')
        print(' Proceed yes/no?')
        yes_typed = input(">>  ")
        if (yes_typed.lower()=='no')  or  (yes_typed.lower()=='n'):
            return False
        while not(not(yes_typed.lower()=='yes')  or  not(yes_typed.lower()=='y')):
            print(' Error try again')
            yes_typed = input(">>  ")
    """            
    branches = node
    descriptions = [descr]
    astra = t.getDefault()
    okv=v.tree(t,branches,descriptions,'ASTRA')
    
    t.setDefault(astra)
    t.write()
    t.close
    if okv: print('VACUUM node is created')
    return True

def modifyhelp(pulseNo,node,descr):
    try:
        t = Tree( 'ASTRA', pulseNo, 'edit' )
    except:
        t = Tree( 'ASTRA', pulseNo, 'New' )
    astra = t.getDefault()
    t.setDefault(astra)
    descr0=t.getNode(node+":HELP").getData()
    print(descr0)
    t.getNode(node+":HELP").putData(descr)
    t.write()
    descr1=t.getNode(node+":HELP").getData()
    print(descr1)
    t.close

def addglobal(pulseNo,runnum,addnode,descr):
    try:
        t = Tree( 'ASTRA', pulseNo, 'edit' )
    except:
        t = Tree( 'ASTRA', pulseNo, 'New' )
    t.setDefault(t.getNode('\\TOP.'+runnum+".GLOBAL"))
    n = mh.createNode(t,addnode,"SIGNAL",descr);
    t.write()
    t.close

def copy_runs(pulseNo_from, run_from, pulseNo_to, run_to, tree):
    # Example usage:
    # move_runs(314, 'RUN1', 1000004, 'RUN1', 'ASTRA')
    
    path_from = '\\' + tree + '::TOP.' + run_from
    path_to = '\\' + tree + '::TOP.' + run_to
    print(path_from)

    # Read what we want to move:
    t_from = Tree(tree, pulseNo_from)
    command = "GETNCI('\\" + path_from + "***','FULLPATH')"
    fullpaths_from = t_from.tdiExecute(command).data().astype(str, copy=False).tolist()
    command = "GETNCI('\\" + path_from + "***','USAGE')"
    usages_from = t_from.tdiExecute(command).data()

    # Read where we want to 
    try:
        t_to = Tree(tree, pulseNo_to, 'EDIT')
        print('editing...')
    except:
        t_to = Tree(tree, pulseNo_to, 'NEW')
        print('new...')

    # Add the run if needed
    try:
        run_node_to = t_to.getNode(path_to)

        # Command line warning_message
        warning_message(pulseNo_to, path_to)

        # Delete node
        t_to.deleteNode(run_node_to)
    except:
        pass
    # Add a new fully empty node
    t_to.addNode(path_to)

    for i in range(0, len(fullpaths_from)):
        fullpath_from = fullpaths_from[i].strip()
        fullpath_to = fullpaths_from[i].replace(path_from, path_to).strip()
        usage = usages_from[i]
        if (usage==1):
            datatype = 'STRUCTURE'
        elif (usage==5):
            datatype = 'NUMERIC'
        elif (usage==6):
            datatype = 'SIGNAL'
        elif (usage==8):
            datatype = 'TEXT'
        elif (usage==11):
            datatype = 'SUBTREE'
        else:
            print('UNKNOWN DATA TYPE!!')
        # Make the node
        n = t_to.addNode(fullpath_to, datatype)

        # Move NUMBER, SIGNAL or TEXT
        if (usage==5)  or  (usage==6)  or  (usage==8):
            n_from = t_from.getNode(fullpath_from)
            n_to = t_to.getNode(fullpath_to)
            n_to.putData(n_from.getRecord())

    t_to.write()
    t_to.close()
    t_from.close()

    print('Data successfully moved')


def warning_message(pulseNo, node):
    pulseNo_str = str(pulseNo)
    print('#####################################################')
    print('#  *** WARNING ***                                  #')
    print('#  You are about to overwrite data                  #')
    spaces = ' '*(41 - len(pulseNo_str))
    print('#  pulseNo=' + pulseNo_str + spaces + '#')
    spaces = ' '*(49 - len(node))
    print('#  ' + node + spaces + '#')
    print('#####################################################')
    print(' Proceed yes/no?')
    yes_typed = input(">>  ")
    if (yes_typed.lower()=='no')  or  (yes_typed.lower()=='n'):
        return
    while not(not(yes_typed.lower()=='yes')  or  not(yes_typed.lower()=='y')):
        print(' Error try again')
        yes_typed = input(">>  ")

