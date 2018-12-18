import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 


raw_data =  [{'title': 'Employee', 'branch':'SF' , 'salary': 60.0}, 
             {'title': 'Employee' , 'branch': 'SF', 'salary': 60.0},
             {'title': 'Employee', 'branch': 'NY' , 'salary': 100.0},
             {'title': 'Manager' , 'branch': 'SF','salary': 300.0},
             {'title': 'Manager', 'branch':'NY' ,'salary': 390.0},
             {'title': 'Manager', 'branch':'NY' ,'salary': 306.0},
             {'title': 'Sub' , 'branch': 'SF','salary': 10.0},
             {'title': 'Temp', 'branch': 'SF' ,'salary': 20.0},
             {'title': 'Manager', 'branch': 'NY' ,'salary': 400.0}]

raw_data_hidden = [{'title': 'Employee', 'branch':'SF' , 'salary': 60.0}, 
                   {'title': 'Employee' , 'branch': 'SF', 'salary': 60.0},
                   {'title': 'Employee', 'branch': 'NY' , 'salary': 50.0},
                   {'title': 'Manager' , 'branch': 'SF','salary': 300.0},
                   {'title': 'Manager', 'branch':'NY' ,'salary': 290.0},
                   {'title': 'Manager', 'branch':'NY' ,'salary': 90.0},
                   {'title': 'Sub' , 'branch': 'SF','salary': 10.0},
                   {'title': 'Temp', 'branch': 'SF' ,'salary': 20.0},
                   {'title': 'Manager', 'branch': 'NY' ,'salary': 40.0}]