from MDSplus import Tree, String
import st40_mds_trees.utility.mdsHelpers as mh
import plasma_node as p
import vacuum_node as v
import getpass
user = getpass.getuser()
def create(shot,run):

    try:
        t = Tree("SOPHIA", shot, "EDIT")
    except:
        print('No SOPHIA tree exists for #'+str(shot))
        return False
    try:
        t.setDefault(t.getNode(run))
    except:
        print('No run '+run+' in SOPHIA tree exists for #'+str(shot))
        return False
    top_run = t.getDefault()
    descr='Vacuum phase node'
    descriptions=[descr]
    okv=v.tree(t,top_run,descriptions,'SOPHIA')
    descr='Plasma phase node'
    descriptions=[descr]
    oka=p.tree(t,top_run,descriptions,'SOPHIA')
    t.write()
    t.close
    if okv: print('VACUUM node is created')
    if oka: print('ASTRA node is created')
    return True
def delete(pulseNo, run):
    t = Tree('SOPHIA', pulseNo, 'edit')

    # get the username of who wrote this run
    try:
        n = t.getNode(r'\SOPHIA::TOP.' + run + '.ASTRA.CODE_VERSION:USER')
        user_already_written = n.data()
    except:
        user_already_written = "unknown user"

    if not(user_already_written==user):
        print('#####################################################')
        print('#  *** WARNING ***                                  #')
        print("#  You are about to delete a different user's run!  #")
        nspaces = 49 - len(user_already_written)
        spaces = ' '*nspaces
        print('#  ' + user_already_written + spaces + '#')
        print('#####################################################')
        return False

    t.deleteNode(run)
    t.write()
    t.close
    return True
