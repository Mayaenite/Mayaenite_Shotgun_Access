"""
For detailed information please see

http://shotgunsoftware.github.com/shotgunEvents/api.html
"""
import logging
import os
import sys
from xml.etree import ElementTree as etree
#os.sys.path.append(os.path.dirname(__file__))
# os.sys.path.append("S:\\SGTK_Core\\install\\core\\python")
# os.sys.path.append("C:\Users\dloveridge\Documents\AW_Git_Repo\Shotgun")
import Schema_Entity_Model
import sgtk
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

def Shotgun_Toolkit_Builder(project_id, config_file):
	if not os.path.exists(config_file):
		raise OSError("Could Not Find config file to parse %r" % config_file)
	else:
		tree = etree.parse(config_file)
		win_projects_folder   = tree.findtext("win_projects_folder")
		mac_projects_folder   = tree.findtext("mac_projects_folder")
		linux_projects_folder = tree.findtext("linux_projects_folder")
		
		win_schema_install    = tree.findtext("win_schema_install")
		mac_schema_install    = tree.findtext("mac_schema_install")
		linux_schema_install  = tree.findtext("linux_schema_install")
		schema_config_uri     = tree.findtext("schema_config_uri")
		
		if win_projects_folder is None:
			raise ValueError("The Windows Project Folder Must Have A Valid Folder Path And Nothing Was Given")
		
		if win_schema_install is None:
			raise ValueError("The Windows Schema Install Folder Must Have A Valid Folder Path And Nothing Was Given")	
		
		if schema_config_uri is None:
			schema_config_uri = 'tk-config-default'
	
	if os.name == 'nt':
		# Check To Make Sure That The Base Projects Folder Exists
		# For Safty Reasons This Folder Is Not Automaticly Created
		if not os.path.exists(win_projects_folder):
			raise OSError("The Input Projects Folder Path %r Does Not Exist Please Create it And Run Again" % win_projects_folder)
		# Check To Make Sure That The Base Toolkit Config Folder Exists
		# For Safty Reasons This Folder Is Not Automaticly Created
		if not os.path.exists(win_schema_install):
			raise OSError("The Input Config Folder Path %r Does Not Exist Please Create it And Run Again" % win_schema_install)
	
	else:
		raise NotImplementedError("Only Windows Is Supported At This Time")

	
	project = sg_access.Entities.Project(project_id)
	
	# The Project name.
	project_name = project.name.value
	
	# Name of the folder which you want
	# to be the root point of the created project.
	# If a project already exists
	# this parameter must reflect the name of
	# the top level folder of the project.
	project_folder_name = project_name.replace(" ", "_")
	
	# Build The Base Project Folder Path
	if os.name == 'nt':
		win_project_path   = os.path.join(win_projects_folder , project_folder_name)
		mac_project_path   = mac_projects_folder if mac_projects_folder is None else os.path.join(mac_projects_folder , project_folder_name).replace("\\", "/")
		linux_project_path = linux_projects_folder if linux_projects_folder is None else os.path.join(linux_projects_folder , project_folder_name).replace("\\", "/")
		
		win_storage_path   = os.path.join(win_schema_install, project_folder_name)
		mac_storage_path   = mac_schema_install if mac_schema_install is None else os.path.join(mac_schema_install, project_folder_name).replace("\\", "/")
		linux_storage_path = linux_schema_install if linux_schema_install is None else os.path.join(linux_schema_install, project_folder_name).replace("\\", "/")
		
		# Check IF The Base Project and Storage Path Exists
		# And If Not Create It This Step Is Done Because 
		# The ShotGun Tool Kit Will Not Create It For You
		# And Will Error out Because It Does Not Exist
		for folder_path in [win_project_path, win_storage_path]:
			if not os.path.exists(folder_path):
				os.makedirs(folder_path)
	else:
		raise NotImplementedError("Only Windows Is Supported At This Time")
	
	psetup = sgtk.get_command("setup_project")
	
	# The configuration to use when setting up this project.
	# This can be a path on disk to a directory containing a config,
	# a path to a git bare repo
	# (e.g. a git repo path which ends with .git)
	# or 'tk-config-default' to fetch the default config from the toolkit app store.
	# config_uri                = "https://github.com/Mayaenite/Master_Config.git"
	config_uri                = schema_config_uri
	
	# The path on disk where the configuration should be installed on Windows.
	config_path_win           = win_storage_path
	# The path on disk where the configuration should be installed on Linux.
	config_path_linux         = linux_storage_path
	# The path on disk where the configuration should be installed on Mac.
	config_path_mac           = mac_storage_path
	
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
	
if __name__ == "__main__":
	Shotgun_Toolkit_Builder(85, "C:\Users\dloveridge\Documents\GitHub\Mayaenite_Shotgun_Access\AW_sgtk_config.xml")
