import os, string
import urllib2
from datetime import datetime

try:
	from shotgun_api3.shotgun import Shotgun
except ImportError:
	try:
		from tank_vendor.shotgun_api3.shotgun import Shotgun
	except ImportError:
		shotgun_folder = os.path.join(os.path.dirname(__file__), "python-api")
		if os.path.exists(shotgun_folder):
			os.sys.path.append(shotgun_folder)
			from shotgun_api3.shotgun import Shotgun
			del shotgun_folder
		else:
			raise LookupError("could not import shotgun_api3 or find python-api folder")

Schema_Data       = {}
Entity_Type_Names = []
Schema_Entities   = None
_Active_Entity_Memory = {}
_sg_connection    =  None
########################################################################
class Standered_Entity_Types(object):
	""""""
	ActionMenuItem                                 = "ActionMenuItem"
	ApiUser                                        = "ApiUser"
	AppWelcomeUserConnection                       = "AppWelcomeUserConnection"
	Asset                                          = "Asset"
	AssetAssetConnection                           = "AssetAssetConnection"
	AssetBlendshapeConnection                      = "AssetBlendshapeConnection"
	AssetElementConnection                         = "AssetElementConnection"
	AssetMocapTakeConnection                       = "AssetMocapTakeConnection"
	AssetSceneConnection                           = "AssetSceneConnection"
	AssetSequenceConnection                        = "AssetSequenceConnection"
	AssetShootDayConnection                        = "AssetShootDayConnection"
	AssetShotConnection                            = "AssetShotConnection"
	Attachment                                     = "Attachment"
	BannerUserConnection                           = "BannerUserConnection"
	Booking                                        = "Booking"
	CameraMocapTakeConnection                      = "CameraMocapTakeConnection"
	ClientUser                                     = "ClientUser"
	CutVersionConnection                           = "CutVersionConnection"
	Department                                     = "Department"
	ElementShotConnection                          = "ElementShotConnection"
	EventLogEntry                                  = "EventLogEntry"
	FilesystemLocation                             = "FilesystemLocation"
	Group                                          = "Group"
	GroupUserConnection                            = "GroupUserConnection"
	HumanUser                                      = "HumanUser"
	Icon                                           = "Icon"
	LaunchSceneConnection                          = "LaunchSceneConnection"
	LaunchShotConnection                           = "LaunchShotConnection"
	LocalStorage                                   = "LocalStorage"
	MocapTakeRangeShotConnection                   = "MocapTakeRangeShotConnection"
	Note                                           = "Note"
	Page                                           = "Page"
	PageHit                                        = "PageHit"
	PageSetting                                    = "PageSetting"
	PerformerMocapTakeConnection                   = "PerformerMocapTakeConnection"
	PerformerRoutineConnection                     = "PerformerRoutineConnection"
	PerformerShootDayConnection                    = "PerformerShootDayConnection"
	PermissionRuleSet                              = "PermissionRuleSet"
	Phase                                          = "Phase"
	PhysicalAssetMocapTakeConnection               = "PhysicalAssetMocapTakeConnection"
	PipelineConfiguration                          = "PipelineConfiguration"
	Playlist                                       = "Playlist"
	PlaylistShare                                  = "PlaylistShare"
	PlaylistVersionConnection                      = "PlaylistVersionConnection"
	Project                                        = "Project"
	ProjectUserConnection                          = "ProjectUserConnection"
	PublishedFile                                  = "PublishedFile"
	PublishedFileDependency                        = "PublishedFileDependency"
	PublishedFileType                              = "PublishedFileType"
	Release                                        = "Release"
	ReleaseTicketConnection                        = "ReleaseTicketConnection"
	Reply                                          = "Reply"
	Revision                                       = "Revision"
	RevisionRevisionConnection                     = "RevisionRevisionConnection"
	RevisionTicketConnection                       = "RevisionTicketConnection"
	RvLicense                                      = "RvLicense"
	Sequence                                       = "Sequence"
	ShootDaySceneConnection                        = "ShootDaySceneConnection"
	Shot                                           = "Shot"
	ShotShotConnection                             = "ShotShotConnection"
	Status                                         = "Status"
	Step                                           = "Step"
	Task                                           = "Task"
	TaskDependency                                 = "TaskDependency"
	TaskTemplate                                   = "TaskTemplate"
	Ticket                                         = "Ticket"
	TicketTicketConnection                         = "TicketTicketConnection"
	TimeLog                                        = "TimeLog"
	Tool                                           = "Tool"
	Tool_sg_source_code_package_Connection         = "Tool_sg_source_code_package_Connection"
	Version                                        = "Version"
#################################################################################
class DATA_TYPES(object):
	CHECKBOX     = 'checkbox'
	COLOR        = 'color'
	TEXT         = 'text'
	IMAGE        = 'image'
	FLOAT        = 'float'
	NUMBER       = 'number'
	ENTITY       = 'entity'
	ENTITY_TYPE  = 'entity_type'
	DATE         = 'date'
	MULTI_ENTITY = 'multi_entity'
	PIVOT_COLUMN = 'pivot_column'
	DURATION     = 'duration'
	PERCENT      = 'percent'
	FOOTAGE      = 'footage'
	TIMECODE     = 'timecode'
	PASSWORD     = 'password'
	SERIALIZABLE = 'serializable'
	DATE_TIME    = 'date_time'
	URL          = 'url'
	LIST         = 'list'
	SUMMARY      = 'summary'
	TAG_LIST     = 'tag_list'
	STATUS_LIST  = 'status_list'
	UUID         = 'uuid'
########################################################################
class Base_Entity(object):
	'''Base class that represents a Shotgun Entity.'''
	#__metaclass__ = Base_Entity_Metaclass
	data_types = DATA_TYPES
	#----------------------------------------------------------------------
	def __init__(self, connection, entity_data):
		self.sg = connection
		isinstance(self.sg, Shotgun_Connection)
		self._entity = {'id': entity_data['id'], 'type': entity_data['type']}
		entity_attr  = getattr(self.sg.Entities, entity_data['type'])
		for field in entity_attr.field_names:
			if not field in ["type"]:
				try:
					self.__setattr__(field, Entity_Field_Memory_Attribute(self.sg, entity_data[field], field, entity_data['type']))
				except KeyError:
					pass
	#----------------------------------------------------------------------
	def activity_stream(self, limit=None):
		""""""
		return Dict_Attribute_Keys(self.sg.connection.activity_stream_read(self._entity["type"], self._entity['id'], entity_fields=None, min_id=None, max_id=None,limit=limit))
	#----------------------------------------------------------------------
	def iter_changed_fields(self):
		""""""
		for att in getattr(self.sg.Entities, self._entity["type"]).field_names:
			field = getattr(self, att)
			try:
				if field.value_changed:
					yield field
			except:
				pass
	#----------------------------------------------------------------------
	def update(self):
		""""""
		ID         = self._entity['id']
		TYP        = self._entity['type']
		entity_cls = self.sg.get_Entity_Class_By_Name(TYP)
		data       = {}
		for field in self.iter_changed_fields():
			data[field.field_name] = field.value
		self.sg.connection.update(TYP,ID,data)
		del self.sg._Active_Entity_Memory[TYP][ID]
		self = entity_cls(ID)
	#----------------------------------------------------------------------
	@property
	def followers(self):
		""""""
		users = self.sg.connection.followers(self._entity)
		ids   = [item['id'] for item in users]
		users = Schema_Entities.HumanUser.find(["id", "is", ids])
		return users
	#----------------------------------------------------------------------
	def follow(self, human):
		""""""
		if hasattr(human, "_entity"):
			return self.sg.connection.follow(human._entity, self._entity)
		else:
			return self.sg.connection.follow(human, self._entity)
	#----------------------------------------------------------------------
	def unfollow(self, human):
		""""""
		if hasattr(human, "_entity"):
			return self.sg.connection.unfollow(human._entity, self._entity)
		else:
			return self.sg.connection.unfollow(human, self._entity)
	#----------------------------------------------------------------------
	def delete(self):
		res = self.sg.connection.delete(self.__class__.__name__,self.id)
		return res
	def __repr__(self):
		return str(self._entity)
	def __str__(self):
		return str(self._entity)

data_lookups ={'color'       :str,
               'currency'    :float,
               'checkbox'    :bool,
               'date'        :str,
               'date_time'   :object, 
               'duration'    :int,
               'entity'      :dict,
               'entity_type' :str,
               'float'       :float,
               'image'       :str,
               'list'        :list,
               'multi_entity':list,
               'number'      :int,
               'password'    :str,
               'percent'     :int,
               'pivot_column':str,
               'serializable':dict,
               'status_list' :str,
               'summary'     :str,
               'tag_list'    :list,
               'text'        :str,
               'timecode'    :int,
               'footage'     :str,
               'url'         :dict,
               'addressing'  :list,
               'uuid'        :str}

#----------------------------------------------------------------------
def SafeDecode( obj, useEncoding='utf-8' ):
	"""Utility function to safely try to decode strings (or dict/list contents)"""
	try:
		if isinstance( obj, unicode ):
			#already unicode, just reutnr it
			return obj
		elif isinstance( obj, str ):
			#it's a str, decode it
			return obj.decode( useEncoding )
		elif isinstance( obj, dict ):
			#recursively convert contents
			for k, v in obj.iteritems():
				obj[k] = SafeDecode( v )
		elif isinstance( obj, list ):
			#recursively convert contents
			for i in range( len(obj) ):
				obj[i] = SafeDecode( obj[i] )
		else:
			#last ditch attempt
			return unicode( obj, encoding=useEncoding )
	except:
		pass
	return obj

#----------------------------------------------------------------------
def connect(host, api_script=None, api_key=None, user=None, password=None):
	if host is None:
		raise ValueError("No Host Url Was Supplied For The Connection")
	
	if len([x for x in [user, password] if x != None]) == 2:
		sg = Shotgun(host,login=user,password=password,convert_datetimes_to_utc=True,http_proxy=None,ensure_ascii=True,connect=True,ca_certs=None)
		
		if sg.authenticate_human_user(user, password) == None:
			raise ValueError("The Human User %s Could Not Be Authenticated" % user)
		
	elif len([x for x in [api_script , api_key] if x != None]) == 2:
		sg = Shotgun(host,script_name=api_script, api_key=api_key,convert_datetimes_to_utc=True,http_proxy=None,ensure_ascii=True,connect=True,ca_certs=None)
	else:
		raise ValueError("Encorrect Values We Supplied For The Connection")
	return sg
#----------------------------------------------------------------------
def connect_with_script(host, api_script, api_key):
	sg = connect(host, api_script=api_script, api_key=api_key, user=None, password=None)
	return sg
#----------------------------------------------------------------------
def connect_with_login(host, user, password):
	sg = connect(host, api_script=None, api_key=None, user=user, password=password)
	return sg
#----------------------------------------------------------------------
def connect_with_config_file(config_file):
	""""""
	if isinstance(config_file, (str, unicode)) and os.path.exists(str(config_file)):
		import xml.etree.ElementTree as etree
		tree       = etree.parse(config_file)
		host       = tree.findtext("host")
		api_script = tree.findtext("api_script")
		api_key    = tree.findtext("api_key")
		user       = tree.findtext("user")
		password   = tree.findtext("password")
		
		if len([x for x in [user, password] if x != None]) == 2 and host != None:
			sg = connect_with_login(host, user, password)
			
		elif len([x for x in [api_script , api_key] if x != None]) == 2 and host != None:
			sg = connect_with_script(host, api_script, api_key)
		else:
			raise ValueError("The Config file %s Contains Incorrect Values" % config_file)
		return sg
#----------------------------------------------------------------------
def connect_with_Environment_Varibles():
	""""""
	host       = os.environ.get("SHOTGUN_HOST_URL", None)
	api_script = os.environ.get("SHOTGUN_API_SCRIPT", None)
	api_key    = os.environ.get("SHOTGUN_API_KEY", None)
	user       = os.environ.get("SHOTGUN_USER_NAME", None)
	password   = os.environ.get("SHOTGUN_USER_PASSWORD", None)

	if len([x for x in [user, password] if x != None]) == 2 and host != None:
		sg = connect(host, api_script, api_key, user, password)

	elif len([x for x in [api_script , api_key] if x != None]) == 2 and host != None:
		sg = connect(host, api_script, api_key, user, password)
	else:
		raise ValueError("The Environment Varibles Contain Incorrect Values")
	return sg
#################################################################################
class Dict_Attribute_Keys(object):
	def __init__(self, data):
		invalid_chars = list(string.punctuation.replace("_", "") + string.whitespace)
		string_digits = list(string.digits)
		data = SafeDecode(data)
		for key, value in data.iteritems():
			key = "".join([k for k in list(key) if not k in invalid_chars])
			key = str("n_" + key) if key[0] in string_digits else key
			if isinstance(value, dict):
				self.__dict__[key] = Dict_Attribute_Keys(value)
			elif isinstance(value, list):
				new_val = []
				for val in value:
					if isinstance(val, dict):
						val = Dict_Attribute_Keys(val)
					new_val.append(val)
				self.__dict__[key] = new_val
			else:
				self.__dict__[key] = value
########################################################################
class Non_Editable_Attribute(object):
	""""""
	__slots__ = ["_data"]
	#----------------------------------------------------------------------
	def __init__(self, value):
		"""Constructor"""
		self._data = value
		
	@property
	def data(self):
		'''returns The Value Of This Attribute'''
		return self._data
	
	#----------------------------------------------------------------------
	def __repr__(self):
		""""""
		return "%s(%r)" % (self.__class__.__name__, self._data)
	#----------------------------------------------------------------------
	def __str__(self):
		""""""
		return str(self._data)
########################################################################
class Editable_Attribute(object):
	""""""
	__slots__ = ["_data"]
	#----------------------------------------------------------------------
	def __init__(self, value):
		"""Constructor"""
		self._data = value

	@property
	def data(self):
		'''returns The Value Of This Attribute'''
		return self._data
	@data.setter
	def data(self, value):
		self._data = value
	#----------------------------------------------------------------------
	def __repr__(self):
		""""""
		return "%s(%r)" % (self.__class__.__name__, self._data)
	#----------------------------------------------------------------------
	def __str__(self):
		""""""
		return str(self._data)
########################################################################
class Entity_Field_Memory_Attribute(object):
	""""""
	__slots__ = ["_connection", "_data", "_original_value", "_old_Value", "_inishlized_time", "_last_modified_time", "_field_name", "_entity_type","_value_changed", "_schema_field"]
	#----------------------------------------------------------------------
	def __init__(self, connection, value, field_name, entity_type):
		"""Constructor"""
		self._data               = value
		self._connection         = connection
		self._original_value     = Non_Editable_Attribute(value)
		self._entity_type        = Non_Editable_Attribute(entity_type)
		self._field_name         = Non_Editable_Attribute(field_name)
		self._old_Value          = None
		self._last_modified_time = None
		self._value_changed      = False
		self._inishlized_time    = datetime.now()
		self._schema_field       = getattr(getattr(self._connection.Entities, entity_type), field_name)
	#----------------------------------------------------------------------
	@property
	def value(self):
		'''returns The Value Of This Field'''
		if self.data_type == DATA_TYPES.ENTITY:
			if not isinstance(self._data, Base_Entity):
				self._data      = getattr(self._connection.Entities, self._data['type'])(self._data['id'])
		return self._data
	#----------------------------------------------------------------------	
	@value.setter
	def value(self, value):
		if self.data_type == DATA_TYPES.ENTITY:
			if isinstance(value, Base_Entity):
				if not value == self.value:
					self._old_Value = self._data
					self._data = value
					self._value_changed = True
					self._last_modified_time = datetime.now()
		else:
			if not self._data == value:
				self._old_Value = self._data
				self._data = value
				self._value_changed = True
				self._last_modified_time = datetime.now()
	#----------------------------------------------------------------------	
	@property
	def field_name(self):
		'''returns The This Fields Data Type'''
		return self._schema_field.name
	#----------------------------------------------------------------------	
	@property
	def data_type(self):
		'''returns The This Fields Data Type'''
		return self._schema_field.data_type
	#----------------------------------------------------------------------	
	@property
	def py_data_type(self):
		'''returns The This Fields Data Type'''
		return data_lookups[self.data_type]
	#----------------------------------------------------------------------	
	@property
	def valid_inputs(self):
		'''returns The This Fields Data Type'''
		if self._schema_field.__class__.__name__ == Entity_Field_Attribute.__class__.__name__:
			return self._schema_field.valid_types
		elif self._schema_field.__class__.__name__ == Values_Field_Attribute.__class__.__name__:
			return self._schema_field.valid_values
		return [data_lookups[self.data_type].__class__.__name__]
	#----------------------------------------------------------------------	
	@property
	def display_value_names(self):
		'''returns The This Fields Data Type'''
		if self._schema_field.__class__.__name__ == Values_Field_Attribute.__class__.__name__:
			return self._schema_field.display_value_names
		return []
	#----------------------------------------------------------------------	
	@property
	def display_values(self):
		'''returns The This Fields Data Type'''
		if self._schema_field.__class__.__name__ == Values_Field_Attribute.__class__.__name__:
			return self._schema_field.display_values
		return []
	#----------------------------------------------------------------------
	@property
	def original_value(self):
		'''returns The Original Value Of This Field'''
		return self._original_value._data
	#----------------------------------------------------------------------
	@property
	def entity_type(self):
		'''returns The Original Value Of This Field'''
		return self._entity_type._data
	#----------------------------------------------------------------------	
	@property
	def field_name(self):
		'''returns The Original Value Of This Field'''
		return self._field_name._data
	#----------------------------------------------------------------------
	@property
	def last_modified_time(self):
		'''returns The Original Value Of This Field'''
		return self._last_modified_time
	#----------------------------------------------------------------------
	@property
	def inishlized_time(self):
		'''returns The Original Value Of This Field'''
		return self._inishlized_time
	#----------------------------------------------------------------------
	@property
	def value_changed(self):
		'''returns The Original Value Of This Field'''
		return self._value_changed
	#----------------------------------------------------------------------
	def __repr__(self):
		""""""
		return str(self.value)
	#----------------------------------------------------------------------
	def __str__(self):
		""""""
		return str(self.value)
########################################################################
class Base_Field_Data(object):
	""""""
	__slots__ = ["editable", "value"]
	#----------------------------------------------------------------------
	def __init__(self, editable=None, value=None):
		"""Constructor"""
		self.editable = Non_Editable_Attribute(editable)
		self.value    = Non_Editable_Attribute(value)
		
	#----------------------------------------------------------------------
	def __repr__(self):
		""""""
		return "%s(editable=%r,value=%r)" % (self.__class__.__name__, self.editable.data, self.value.data)
	#----------------------------------------------------------------------
	def __str__(self):
		""""""
		return "%s(editable=%r,value=%r)" % (self.__class__.__name__, self.editable.data, self.value.data)
########################################################################
class Base_Properties_Field_Data(object):
	""""""
	__slots__ = ["_default_value", "_summary_default"]
	#----------------------------------------------------------------------
	def __init__(self, propertiesDict={}):
		"""Constructor"""
		self._default_value    = Base_Field_Data(propertiesDict["default_value"]['editable'], propertiesDict["default_value"]['value'])
		self._summary_default  = Base_Field_Data(propertiesDict["summary_default"]['editable'], propertiesDict["summary_default"]['value'])
	@property
	def default_value(self):
		""""""
		return self._default_value.value.data
	@property
	def summary_default(self):
		""""""
		return self._summary_default.value.data
########################################################################
class Summary_Properties_Field_Data(Base_Properties_Field_Data):
	""""""
	__slots__ = ["_default_value", "_summary_default", "_summary_field", "_summary_value"]
	#----------------------------------------------------------------------
	def __init__(self, propertiesDict={}):
		"""Constructor"""
		super(Summary_Properties_Field_Data, self).__init__(propertiesDict)
		self._summary_field = Base_Field_Data(propertiesDict["summary_field"]['editable'], propertiesDict["summary_field"]['value'])
		self._summary_value = Base_Field_Data(propertiesDict["summary_value"]['editable'], propertiesDict["summary_value"]['value'])
	@property
	def summary_field(self):
		""""""
		return self._summary_field.value.data
	@property
	def summary_value(self):
		""""""
		return self._summary_value.value.data
########################################################################
class Values_Properties_Field_Data(Base_Properties_Field_Data):
	""""""
	__slots__ = ["_default_value", "_summary_default", "_display_values", "_hidden_values", "_valid_values"]
	#----------------------------------------------------------------------
	def __init__(self, propertiesDict={}):
		"""Constructor"""
		super(Values_Properties_Field_Data, self).__init__(propertiesDict)
		self._display_values = Base_Field_Data(propertiesDict["display_values"]['editable'], propertiesDict["display_values"]['value'])
		self._hidden_values  = Base_Field_Data(propertiesDict["hidden_values"]['editable'], sorted(propertiesDict["hidden_values"]['value']))
		self._valid_values   = Base_Field_Data(propertiesDict["valid_values"]['editable'], sorted(propertiesDict["valid_values"]['value']))
	@property
	def display_values(self):
		""""""
		return self._display_values.value.data
	@property
	def hidden_values(self):
		""""""
		return self._hidden_values.value.data
	@property
	def valid_values(self):
		""""""
		return self._valid_values.value.data
########################################################################
class Entity_Properties_Field_Data(Base_Properties_Field_Data):
	""""""
	__slots__ = ["_default_value", "_summary_default", "_valid_types"]
	#----------------------------------------------------------------------
	def __init__(self, propertiesDict={}):
		"""Constructor"""
		super(Entity_Properties_Field_Data, self).__init__(propertiesDict)
		self._valid_types    = Base_Field_Data(propertiesDict["valid_types"]['editable'], sorted(propertiesDict["valid_types"]['value']))
	@property
	def valid_types(self):
		""""""
		return self._valid_types.value.data
########################################################################
class Base_Field_Attribute(object):
	""""""
	__slots__ = ["_data_type", "_description", "_editable", "_entity_type", "_mandatory", "_name", "_unique", "_visible"]
	#----------------------------------------------------------------------
	def __init__(self, fieldDict={}):
		"""Constructor"""
		self._data_type   = Base_Field_Data(fieldDict["data_type"]['editable'], fieldDict["data_type"]['value'])
		self._description = Base_Field_Data(fieldDict["description"]['editable'], fieldDict["description"]['value'])
		self._editable    = Base_Field_Data(fieldDict["editable"]['editable'], fieldDict["editable"]['value'])
		self._entity_type = Base_Field_Data(fieldDict["entity_type"]['editable'], fieldDict["entity_type"]['value'])
		self._mandatory   = Base_Field_Data(fieldDict["mandatory"]['editable'], fieldDict["mandatory"]['value'])
		self._name        = Base_Field_Data(fieldDict["name"]['editable'], fieldDict["name"]['value'])
		self._unique      = Base_Field_Data(fieldDict["unique"]['editable'], fieldDict["unique"]['value'])
		self._visible     = Base_Field_Data(fieldDict["visible"]['editable'], fieldDict["visible"]['value'])
		
	@property
	def data_type(self):
		""""""
		return self._data_type.value.data
	@property
	def description(self):
		""""""
		return self._description.value.data
	@property
	def editable(self):
		""""""
		return self._editable.value.data
	@property
	def entity_type(self):
		""""""
		return self._entity_type.value.data
	@property
	def mandatory(self):
		""""""
		return self._mandatory.value.data
	@property
	def name(self):
		""""""
		return self._name.value.data
	@property
	def unique(self):
		""""""
		return self._unique.value.data
	@property
	def visible(self):
		""""""
		return self._visible.value.data
########################################################################
class Standered_Field_Attribute(Base_Field_Attribute):
	""""""
	__slots__ = ["_data_type", "_description", "_editable", "_entity_type", "_mandatory", "_name", "_unique", "_visible", "_properties"]
	#----------------------------------------------------------------------
	def __init__(self, fieldDict={}):
		"""Constructor"""
		super(Standered_Field_Attribute, self).__init__(fieldDict)
		self._properties =  Base_Properties_Field_Data(fieldDict["properties"])
########################################################################
class Summary_Field_Attribute(Base_Field_Attribute):
	""""""
	__slots__ = ["_data_type", "_description", "_editable", "_entity_type", "_mandatory", "_name", "_unique", "_visible", "_properties"]
	#----------------------------------------------------------------------
	def __init__(self, fieldDict={}):
		"""Constructor"""
		super(Summary_Field_Attribute, self).__init__(fieldDict)
		self._properties =  Summary_Properties_Field_Data(fieldDict["properties"])
	@property
	def summary_field(self):
		""""""
		return self._properties.summary_field
	@property
	def summary_default(self):
		""""""
		return self._properties.summary_default
########################################################################
class Values_Field_Attribute(Base_Field_Attribute):
	""""""
	__slots__ = ["_data_type", "_description", "_editable", "_entity_type", "_mandatory", "_name", "_unique", "_visible", "_properties"]
	#----------------------------------------------------------------------
	def __init__(self, fieldDict={}):
		"""Constructor"""
		super(Values_Field_Attribute, self).__init__(fieldDict)
		self._properties = Values_Properties_Field_Data(fieldDict["properties"])
	@property
	def display_values(self):
		""""""
		return self._properties.display_values
	@property
	def hidden_values(self):
		""""""
		return self._properties.hidden_values
	@property
	def valid_values(self):
		""""""
		return self._properties.valid_values
	
	@property
	def display_value_names(self):
		""""""
		res = []
		for tag in self.valid_values:
			res.append(self.display_values[tag])
		return res
########################################################################
class Entity_Field_Attribute(Base_Field_Attribute):
	""""""
	__slots__ = ["_data_type", "_description", "_editable", "_entity_type", "_mandatory", "_name", "_unique", "_visible", "_properties"]
	#----------------------------------------------------------------------
	def __init__(self, fieldDict={}):
		"""Constructor"""
		super(Entity_Field_Attribute, self).__init__(fieldDict)
		self._properties = Entity_Properties_Field_Data(fieldDict["properties"])
	@property
	def valid_types(self):
		""""""
		return self._properties.valid_types
########################################################################
class Shotgun_Auto_Close_Connection(object):
	''''''
	#----------------------------------------------------------------------
	def __init__(self, connection=None):
		""""""
		self.connection = connection
	#----------------------------------------------------------------------
	def __enter__(self):
		self.sg = none_To_ShotgunEvents(self.connection)
		return self.sg
	#----------------------------------------------------------------------
	def __exit__(self, type, value, traceback):
		# If The 
		if self.connection is None:
			self.sg.close()
########################################################################
class Shotgun_Connection(object):
	def __init__(self, host=None, api_script=None, api_key=None, user=None, password=None, config_file=None, use_env=False):
		self._Schema_Data       = {}
		self._Entity_Type_Names = []
		self._Schema_Entities   = None
		self._Active_Entity_Memory = {}
		
		self._host        = host
		self._api_script  = api_script
		self._api_key     = api_key
		self._user        = user
		self._password    = password
		self._config_file = config_file
		self._use_env     = use_env
		self.set_connection()
	#----------------------------------------------------------------------
	def set_connection(self):
		""""""
		if self._use_env:
			connection =  connect_with_Environment_Varibles()
		elif isinstance(self._config_file, (str, unicode)):
			connection =  connect_with_config_file(self._config_file)
		else:
			if self._host is None:
				raise ValueError("No Host Url Was Supplyed For The Connection")
			else:
				connection = connect(self._host, self._api_script, self._api_key, self._user, self._password)
		
		self._connection = Non_Editable_Attribute(connection)
	@property
	#----------------------------------------------------------------------
	def connection(self):
		""""""
		return self._connection.data
	@property
	#----------------------------------------------------------------------
	def auth_params(self):
		""""""
		return self.connection._auth_params()
	@property
	#----------------------------------------------------------------------
	def info(self):
		""""""
		return self.connection.info()
	@property
	#----------------------------------------------------------------------
	def session_token(self):
		""""""
		return self.connection.get_session_token()
	#----------------------------------------------------------------------
	def schema(self, project_entity=None):
		""""""
		if project_entity is not None:
			schema_query = self.connection.schema_read(project_entity=project_entity)
		else:
			schema_query = self.connection.schema_read()
		return schema_query
	#----------------------------------------------------------------------
	def get_Entity_Class_By_Name(self, entity_type_name):
		""""""
		entity_class = getattr(self.Entities, entity_type_name)
		isinstance(entity_class, Shotgun_Schema_Entity)
		return entity_class
	#----------------------------------------------------------------------
	def entity_class_creator(self, project_entity=None):
		global Schema_Data, Entity_Type_Names
		Shotgun_Schema_Entity.sg = self
		self._Schema_Data       = self.schema(project_entity=project_entity)
		self._Entity_Type_Names = sorted(self._Schema_Data.keys())
		self._Schema_Entities   = {}
		self._Active_Entity_Memory = dict()
		Schema_Data = self._Schema_Data
		Entity_Type_Names = self._Entity_Type_Names
		Schema_Entities = {} 
		for name in self._Entity_Type_Names:
			self._Active_Entity_Memory[name] = dict()
			
			slots = ["field_names", "simple_fields", "entity_fields", "multi_entity_fields", "multi_type_entity_fields", "multi_type_multi_entity_fields"] + self._Schema_Data[name].keys()
			slots.sort()
			code_str  = '''class %s(Shotgun_Schema_Entity):\n''' % name
			code_str += '''\t""""""\n'''
			code_str += '''\t__slots__ = %r''' % slots
	
			exec code_str
			cls = locals()[name]
			cls.sg =  self
			self._Schema_Entities[name] = cls
			Schema_Entities[name] = cls()
		self.Schema_Entities = Dict_Attribute_Keys(self._Schema_Entities)
		self.Entities = Dict_Attribute_Keys(Schema_Entities)
		return self.Entities
	
########################################################################
class Base_Entity_Metaclass(type):
	""""""
	#----------------------------------------------------------------------
	def __new__(cls, *args, **kwargs):
		global Schema_Data, Entity_Type_Names
		cls_name = args[0]
		obj = super(Base_Entity_Metaclass, cls).__new__(cls, *args, **kwargs)
		if cls_name in  Entity_Type_Names:
			cls_field_dic = Schema_Data[cls_name]
			Field_names = sorted(cls_field_dic.keys())
			for field_name in Field_names:
				fieldDict        = cls_field_dic[field_name]
				field_data_type  = fieldDict["data_type"]["value"]
				field_properties = fieldDict["properties"]
		
				if field_data_type in ["entity", "multi_entity"]:
					attr = Entity_Field_Attribute(fieldDict)
				elif "display_values" in field_properties:
					attr = Values_Field_Attribute(fieldDict)
				elif "summary_value"  in field_properties:
					attr = Summary_Field_Attribute(fieldDict)
				else:
					attr = Standered_Field_Attribute(fieldDict)
				setattr(obj, field_name, attr)
			simple_fields = _find_simple_field_names(obj)
			entity_fields = _find_entity_field_names(obj)
			multi_type_entity_fields = _find_multi_type_entity_field_names(obj)
			multi_entity_fields = _find_multi_entity_field_names(obj)
			multi_type_multi_entity_fields = _find_multi_type_multi_entity_field_names(obj)
			setattr(obj, "field_names", Field_names)
			setattr(obj, "simple_fields", simple_fields)
			setattr(obj, "entity_fields", entity_fields)
			setattr(obj, "multi_type_entity_fields", multi_type_entity_fields)
			setattr(obj, "multi_entity_fields", multi_entity_fields)
			setattr(obj, "multi_type_multi_entity_fields", multi_type_multi_entity_fields)
		return obj
	#----------------------------------------------------------------------
	def __init__(cls, name, bases, kwds):
		super(Base_Entity_Metaclass, cls).__init__(name, bases, kwds)
	#----------------------------------------------------------------------
	def __call__(cls, *args, **kwargs):
		obj = super(Base_Entity_Metaclass, cls).__call__( *args, **kwargs)
		return obj
########################################################################
class Shotgun_Schema_Entity(object):
	""""""
	__metaclass__ = Base_Entity_Metaclass
	sg =  None
	#----------------------------------------------------------------------
	def __call__(self, Id):
		obj =  self.find_By_ID(Id)
		return obj
	#----------------------------------------------------------------------
	@classmethod
	def get_field_attributes(cls):
		res = []
		for name, value in cls.__dict__.iteritems():
			if isinstance(value, Base_Field_Attribute):
				res.append(value)
		return res
	#----------------------------------------------------------------------
	@classmethod
	def find(cls, filters=[], fields=[], sort_by='created_at',sort_direction='desc',limit=0):
		sg  = cls.sg.connection
		res = []
		
		entity_collection =  cls.sg._Active_Entity_Memory[cls.__name__]
		
		fields = fields if len(fields) else cls.field_names
		
		order = [{'column':sort_by,'direction':sort_direction}]
		
		if type(filters) == list:
			for item in filters:
				if not isinstance(item,(list,dict)):
					filters = [filters]
					break
		
		elif type(filters) == tuple:
			filters = list(filters)
		
		query = sg.find(cls.__name__, filters=filters, fields=fields, order=order, limit=limit)
		
		for item in query:
			if entity_collection.has_key(item.get("id")):
				item = entity_collection[item.get("id")]
				res.append(item)
			else:
				item = Base_Entity(cls.sg, item)
				entity_collection[item.id.value] = item
				res.append(item)
		return res
	#----------------------------------------------------------------------
	@classmethod
	def find_one(cls, filters=[], fields=[]):
		entity_collection =  cls.sg._Active_Entity_Memory[cls.__name__]
		sg  = cls.sg.connection
		res = None
		if type(filters) == list:
			for item in filters:
				if not isinstance(item,(list,dict)):
					filters = [filters]
					break
		elif type(filters) == tuple:
			filters = list(filters)
		
		query = sg.find_one(cls.__name__, filters=filters)
		
		if query is not None:
			if entity_collection.has_key(query.get("id")):
				res = entity_collection[query.get("id")]
			else:
				fields = fields if len(fields) else cls.field_names
				query  = sg.find_one(cls.__name__, filters=[["id", "is", query.get("id")]], fields=fields)
				res    = Base_Entity(cls.sg, query)
				entity_collection[res.id.value] = res
		return res
	#----------------------------------------------------------------------
	@classmethod
	def find_By_ID(cls, Id):
		entity_collection =  cls.sg._Active_Entity_Memory[cls.__name__]
		if isinstance(Id, list):
			res = []
			for i in Id:
				if entity_collection.has_key(i):
					Id.remove(i)
					res.append[entity_collection[i]]
			
			query = cls.find(filters=[["id", "in", Id]])
			
			for item in query:
				res.append(item)
		else:
			if entity_collection.has_key(Id):
				res = entity_collection[Id]
			else:
				res = cls.find_one(filters=["id", "is", Id])
		return res
	#----------------------------------------------------------------------
	@classmethod
	def find_all_created_in_calendar_day(cls, filters=[], fields=[], sort_by='created_at',sort_direction='desc',limit=0,offset=0):
		res = []
		if type(filters) == tuple:
			filters = list(filters)
		filters.append( ["created_at" ,'in_calendar_day', offset] )
		res = cls.find(filters=filters, fields=fields, sort_by=sort_by, sort_direction=sort_direction, limit=limit)
		return res
	#----------------------------------------------------------------------
	@classmethod
	def create(cls,data):
		sg  = cls.sg.connection
		res = sg.create(cls.__name__, data,cls.field_names)
		return res

#----------------------------------------------------------------------
def _find_simple_field_names(cls):
	res = []
	for name, value in cls.__dict__.iteritems():
		if isinstance(value, Standered_Field_Attribute):
			if value.data_type in data_lookups:
				if data_lookups.get(value.data_type) in [str,int,float,bool]:
					res.append(name)
	res.sort()
	return res
#----------------------------------------------------------------------
def _find_entity_field_names(cls):
	res = []
	for name, value in cls.__dict__.iteritems():
		if isinstance(value, Entity_Field_Attribute):
			if value.data_type == DATA_TYPES.ENTITY:
				res.append(name)
	res.sort()
	return res
#----------------------------------------------------------------------
def _find_multi_type_entity_field_names(cls):
	res = []
	for name, value in cls.__dict__.iteritems():
		if isinstance(value, Entity_Field_Attribute):
			if value.data_type == DATA_TYPES.ENTITY:
				if len(value.valid_types) > 1:
					res.append(name)
	res.sort()
	return res
#----------------------------------------------------------------------
def _find_multi_entity_field_names(cls):
	res = []
	for name, value in cls.__dict__.iteritems():
		if isinstance(value, Base_Field_Attribute):
			if value.data_type == DATA_TYPES.MULTI_ENTITY:
				if len(value.valid_types) == 1:
					res.append(name)
	res.sort()
	return res
#----------------------------------------------------------------------
def _find_multi_type_multi_entity_field_names(cls):
	res = []
	for name, value in cls.__dict__.iteritems():
		if isinstance(value, Entity_Field_Attribute):
			if value.data_type == DATA_TYPES.MULTI_ENTITY:
				if len(value.valid_types) > 1:
					res.append(name)
	res.sort()
	return res
#----------------------------------------------------------------------
def _get_Field_Value(entity,field):
	_cls_dict = Base_Entity._cls_dict
	cashed_fields  = entity._cashed_fields
	if field in entity._cashed_fields.keys():
		if entity._cashed_fields[field] != None:
			return entity._cashed_fields[field]
	connection     = entity.get_connection()
	entity_id      = entity._entity.get("id")
	query          = find_one(connection, entity.type_name, entity_id, field)
	field_value    = query[field]

	if isinstance(field_value,dict):
		field_type = field_value['type']

		if field_type in _cls_dict.keys():
			cls = _cls_dict[field_type]
			field_value = cls(field_value)
		else:
			field_value = Dict_Attribute_Keys(field_value)
	elif isinstance(field_value,list):
		field_values = []
		for i,v in enumerate(field_value):
			item = field_value[i]
			if isinstance(item,dict):
				item_type = item['type']
				if item_type in _cls_dict.keys():
					cls = _cls_dict[item_type]
					field_values.append(cls(item))
		if len(field_values):
			field_value = field_values

	if field in cashed_fields.keys():
		if cashed_fields[field] == None and field_value != None:
			cashed_fields[field] = field_value
	return field_value
#----------------------------------------------------------------------
def _set_Field_Value(entity,field,value):
	cashed_fields  = entity._cashed_fields

	if isinstance(value,list):
		values = []
		for item in value:
			if isinstance(item,Base_Entity):
				values.append(item._entity)
			else:
				values.append(item)
		data = {field:values}
	else:
		values = value
		data = {field:value}
	entity.shotgun_connection.update(entity.type_name, entity._id, data)
	if field in cashed_fields.keys():
		cashed_fields[field] = value
#----------------------------------------------------------------------
def create_Attribute_Access(att):
	fget = lambda cls:_get_Field_Value(cls,att)
	fset = lambda cls,val:_set_Field_Value(cls,att,val)
	prop = property(fget,fset)
	return prop

#----------------------------------------------------------------------
def entity_class_creator(connection=None, update=True, global_space=None):
	global Schema_Data, Entity_Type_Names, Schema_Entities, _Active_Entity_Memory
	Schema_Data       = AW_Shotgun_Access.get_Shotgun_Schema(connection=connection, update=update)
	Entity_Type_Names = sorted(Schema_Data.keys())
	Schema_Entities   = {}
	_Active_Entity_Memory = dict()
	for name in Entity_Type_Names:
		_Active_Entity_Memory[name] = dict()
	if global_space == None:
		global_space = globals()
	if not connection is None:
		Shotgun_Schema_Entity.sg = Shotgun_Connection(base_url=connection.base_url, script_name=connection.config.script_name, api_key=connection.config.api_key, login=None, password=None)
	else:
		Shotgun_Schema_Entity.sg = Shotgun_Connection()
	for name in sorted(Schema_Data.keys()):
		
		code_str  = '''class %s(Shotgun_Schema_Entity):\n''' % name
		code_str += '''\t""""""\n'''
		slots = ["field_names", "simple_fields", "entity_fields", "multi_entity_fields", "multi_type_entity_fields", "multi_type_multi_entity_fields"] + Schema_Data[name].keys()
		slots.sort()
		code_str += '''\t__slots__ = %r''' % slots

		exec code_str
		cls = locals()[name]
		Schema_Entities[name] = cls
		global_space[name] = cls()
	Schema_Entities = Dict_Attribute_Keys(Schema_Entities)
	cls_Collection = dict(Schema_Entities=Schema_Entities)
	global_space.update(cls_Collection)	

if __name__ == "__main__":
	connection = Shotgun_Connection(use_env=True)
	connection.entity_class_creator()
	prj =  connection.Entities.Project(81)
	shot = connection.Entities.Shot.find(filters=[['project','is',{'type':'Project','id':81}]])
	# entity_class_creator(connection=connection, update=True, global_space=None)
	# prj = Project.find_By_ID(80)
