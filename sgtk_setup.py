"""
For detailed information please see

http://shotgunsoftware.github.com/shotgunEvents/api.html
"""
import logging
import os
import sys
#os.sys.path.append(os.path.dirname(__file__))
# os.sys.path.append("S:\\SGTK_Core\\install\\core\\python")
# os.sys.path.append("C:\Users\dloveridge\Documents\AW_Git_Repo\Shotgun")
import Schema_Entity_Model
sg_access = Schema_Entity_Model.Shotgun_Connection(use_env=True)

def check_and_change_project_name(sg, logger, event):
	"""checks the project for name for ' ' and replaces them with '_'"""
	
	project = sg.find_one("Project", filters=[["id","is",event.get('meta').get('entity_id')]],fields=["name"])
	project_name = project.get("name")
	project_id   = project.get("id")
	
	# Check for spaces
	if " " in project_name:
		# replace spaces with underscores
		project_name = project_name.replace(" ", "_")
		# update Project With New Name
		sg.update("Project", project_id, dict(name=project_name) )

def Shotgun_Toolkit_Builder(sgtk, project_id, projects_folder, config_settings, win_config_folder, mac_config_folder=None):
	# Check To Make Sure That The Base Projects Folder Exists
	# For Safty Reasons This Folder Is Not Automaticly Created
	if not os.path.exists(projects_folder):
		raise OSError("The Input Projects Folder Path %r Does Not Exist Please Create it And Run Again" % projects_folder)
	
	# Check To Make Sure That The Base Toolkit Config Folder Exists
	# For Safty Reasons This Folder Is Not Automaticly Created
	if not os.path.exists(config_folder):
		raise OSError("The Input Config Folder Path %r Does Not Exist Please Create it And Run Again" % config_folder)
	
	project      = sg.find_one("Project", filters=[["id","is",project_id]],fields=["name"])
	project_name = project.get("name")
	
	# Name of the folder which you want
	# to be the root point of the created project.
	# If a project already exists
	# this parameter must reflect the name of
	# the top level folder of the project.
	project_folder_name = project_name.replace(" ", "_")
	
	# Shotgun id for the project you want to set up.
	project_id          = project.get("id")
	
	# Build The Base Project Folder Path
	# "\\\\BLUE\\Arc\\User\\dloveridge\\Shotgun_Mayaenite\\Projects\\" + project_folder_name
	project_path = os.path.join(projects_folder , project_folder_name)
	# Check IF The Base Project Path Exists
	# And If Not Create It This Step Is Done Because 
	# The ShotGun Tool Kit Will Not Create It For You
	# And Will Error out Because It Does Not Exist
	if not os.path.exists(project_path):
		os.makedirs(project_path)
	
	# Build The Base Project Folder Path
	# storage_path = "\\\\BLUE\\Arc\\User\\dloveridge\\Shotgun_Mayaenite\\Tank\\" + project_folder_name
	storage_path = os.path.join(config_folder, project_folder_name)
	
	# Check IF The Base Storage Path Exists
	# And If Not Create It This Step Is Done Because 
	# The ShotGun Tool Kit Will Not Create It For You
	# And Will Error out Because It Does Not Exist	
	if not os.path.exists(storage_path):
		os.makedirs(storage_path)
	psetup = sgtk.get_command("setup_project")
	
	# The configuration to use when setting up this project.
	# This can be a path on disk to a directory containing a config,
	# a path to a git bare repo
	# (e.g. a git repo path which ends with .git)
	# or 'tk-config-default' to fetch the default config from the toolkit app store.
	# config_uri                = "https://github.com/Mayaenite/Master_Config.git"
	config_uri                = config_settings
	
	# The path on disk where the configuration should be installed on Windows.
	# config_path_win           = "\\\\BLUE\\Arc\\User\\dloveridge\\Shotgun_Mayaenite\\Tank\\" + project_folder_name
	config_path_win           = "\\\\BLUE\\Arc\\User\\dloveridge\\Shotgun_Mayaenite\\Tank\\" + project_folder_name
	
	# The path on disk where the configuration should be installed on Linux.
	# config_path_linux         = "/Volumes/Arc/User/dloveridge/Shotgun_Mayaenite/Tank/" + project_folder_name
	config_path_linux         = "/Volumes/Arc/User/dloveridge/Shotgun_Mayaenite/Tank/" + project_folder_name
	
	# The path on disk where the configuration should be installed on Mac.
	# config_path_mac           = "/Volumes/Arc/User/dloveridge/Shotgun_Mayaenite/Tank/" + project_folder_name
	config_path_mac           = "/Volumes/Arc/User/dloveridge/Shotgun_Mayaenite/Tank/" + project_folder_name
	
	# Enabling this flag allows you to run the
	# set up project on projects which have 
	# already been previously set up.
	force                     = True
	
	# Check that the path to the storage exists.
	# this is enabled by default but can be turned off
	# in order to deal with certain expert level use 
	# cases relating to UNC paths.
	check_storage_path_exists = False
	
	parameters = dict(
	    config_uri                = config_uri,
	    config_path_win           = config_path_win,
	    config_path_linux         = config_path_linux,
	    config_path_mac           = config_path_mac,
	    project_folder_name       = project_folder_name,
	    project_id                = project_id,
	    check_storage_path_exists = check_storage_path_exists,
	    force                     = force
	)
	
	psetup.execute(parameters)
	
	# prj = sgtk.sgtk_from_entity("Project",project_id)
	
	# prj.create_filesystem_structure("Project",project_id)
	
	## New Code For Shot Creation
	
	# shot_data = create_Shot_One_Previs(sg, project)
	
	# if not shot_data == False:
		# shot_id   = shot_data.get("id")
		
		# sgtk_shot = sgtk.sgtk_from_entity("Shot", shot_id)
		
		# sgtk_shot.create_filesystem_structure("Shot", shot_id)
		
		# create_Task_Previs(sg, project, shot_data)
		
if __name__ == "__main__":
	connection = AW_Shotgun_Access.connect_to_script("Toolkit", "21a993fd1dafe1caa0ed38eeba4d7684eaa0f47299f614b17fc2cab429b8212b","https://mayaenite.shotgunstudio.com")
	Shotgun_Toolkit_Builder(connection, 82)
