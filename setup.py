import cx_Freeze

executables = [cx_Freeze.Executable("Board.py", base=None, targetName='Graph-Vis')]

cx_Freeze.setup(
    name="Graph Visualizer",
    options={"build_exe": {"packages":["pygame"],}},
    executables = executables)