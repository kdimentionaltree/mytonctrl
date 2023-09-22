import os
import json
import subprocess
import requests
import base64

from mytoncore.utils import hex2b64, dict2b64
from mytoninstaller.utils import StartMytoncore, GetInitBlock
from mypylib.mypylib import ip2int, Dict


defaultLocalConfigPath = "/usr/bin/ton/local.config.json"


def GetConfig(**kwargs):
	path = kwargs.get("path")
	file = open(path, 'rt')
	text = file.read()
	file.close()
	config = Dict(json.loads(text))
	return config
#end define


def SetConfig(**kwargs):
	path = kwargs.get("path")
	data = kwargs.get("data")

	# write config
	text = json.dumps(data, indent=4)
	file = open(path, 'wt')
	file.write(text)
	file.close()
#end define


def BackupVconfig(local):
	local.add_log("Backup validator config file 'config.json' to 'config.json.backup'", "debug")
	vconfig_path = local.buffer.vconfig_path
	backupPath = vconfig_path + ".backup"
	args = ["cp", vconfig_path, backupPath]
	subprocess.run(args)
#end define


def BackupMconfig(local):
	local.add_log("Backup mytoncore config file 'mytoncore.db' to 'mytoncore.db.backup'", "debug")
	mconfig_path = local.buffer.mconfig_path
	backupPath = mconfig_path + ".backup"
	args = ["cp", mconfig_path, backupPath]
	subprocess.run(args)
#end define


def GetPortsFromVconfig(local):
	vconfig_path = local.buffer.vconfig_path

	# read vconfig
	local.add_log("read vconfig", "debug")
	vconfig = GetConfig(path=vconfig_path)

	# read mconfig
	local.add_log("read mconfig", "debug")
	mconfig_path = local.buffer.mconfig_path
	mconfig = GetConfig(path=mconfig_path)

	# edit mytoncore config file
	local.add_log("edit mytoncore config file", "debug")
	mconfig.liteClient.liteServer.port = mconfig.liteservers[0].port
	mconfig.validatorConsole.addr = f"127.0.0.1:{mconfig.control[0].port}"

	# write mconfig
	local.add_log("write mconfig", "debug")
	SetConfig(path=mconfig_path, data=mconfig)

	# restart mytoncore
	StartMytoncore(local)
#end define


def CreateLocalConfig(local, initBlock, localConfigPath=defaultLocalConfigPath):
	# dirty hack, but GetInitBlock() function uses the same technique
	from mytoncore import hex2base64

	# read global config file
	file = open("/usr/bin/ton/global.config.json", 'rt')
	text = file.read()
	data = json.loads(text)
	file.close()

	# edit config
	liteServerConfig = GetLiteServerConfig(local)
	data["liteservers"] = [liteServerConfig]
	data["validator"]["init_block"]["seqno"] = initBlock["seqno"]
	data["validator"]["init_block"]["root_hash"] = hex2base64(initBlock["rootHash"])
	data["validator"]["init_block"]["file_hash"] = hex2base64(initBlock["fileHash"])
	text = json.dumps(data, indent=4)

	# write local config file
	file = open(localConfigPath, 'wt')
	file.write(text)
	file.close()

	# chown
	user = local.buffer.user
	args = ["chown", "-R", user + ':' + user, localConfigPath]

	print("Local config file created:", localConfigPath)
#end define


def GetLiteServerConfig(local):
	keys_dir = local.buffer.keys_dir
	liteserver_key = keys_dir + "liteserver"
	liteserver_pubkey = liteserver_key + ".pub"
	result = Dict()
	file = open(liteserver_pubkey, 'rb')
	data = file.read()
	file.close()
	key = base64.b64encode(data[4:])
	ip = requests.get("https://ifconfig.me").text
	mconfig = GetConfig(path=local.buffer.mconfig_path)
	result.ip = ip2int(ip)
	result.port = mconfig.liteClient.liteServer.port
	result.id = Dict()
	result.id["@type"]= "pub.ed25519"
	result.id.key= key.decode()
	return result
#end define
