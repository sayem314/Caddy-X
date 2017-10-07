from __future__ import print_function
from sys import exit
import sys,os,subprocess,platform,tarfile,zipfile
# import urllib for downloading http files
if int(platform.python_version()[0]) >= 3:
	from urllib.request import urlretrieve
else:
	from urllib import urlretrieve
# set text color
try:
	import colorama
	colorama.init()
	err = colorama.Back.RED + 'error:' + colorama.Style.RESET_ALL
	scs = colorama.Back.GREEN + 'success:' + colorama.Style.RESET_ALL
except ImportError:
	err = 'error:'
	scs = 'success:'

# output error on invalid command
if len(sys.argv) == 1:
	print("not enough argument!")
	exit()

if len(sys.argv) > 4:
	print("too much argument!")
	exit()

# print information about this tool
if str(sys.argv[1]) in ["-V", "--version"]:
	print("Caddy-X", "v1.0.0 beta")
	print("Author: Sayem Chowdhury")
	print("CLI tool for downloading/building Caddy web server")
	print("Support: github.com/sayem314/Caddy-X")
	exit()

if not str(sys.argv[1]) in ["install", "get", "build"]:
    print("usage:", sys.argv[0], "install/get/build")
    print("with plugins:", sys.argv[0], "install/get/build -p example.plugin")
    exit()

# set caddy web server name
caddyname = "caddy web server"

# get current directory
cwd = os.getcwd()
userpath = os.path.expanduser('~')
slash = os.sep
caddygo = userpath + slash + 'go' + slash + 'src' + slash + 'github.com' + slash + 'mholt' + slash + 'caddy' + slash + 'caddy'

# Get system type
whatos = platform.system().lower()

def Get():
	# Get system bits
	getbits = platform.architecture()[0]
	cpubits="unknown"
	if getbits == '64bit':
		cpubits="amd64"
		cpubitsname="64bit.."
	elif getbits == '32bit':
		cpubits="386"
		cpubitsname="32bit.."
	isarm = platform.uname()[4].lower()
	if isarm[:3] == 'arm':
		cpubits = isarm[:3] + isarm[4]
		if getbits == '64bit':
			cpubits='arm64'
		cpubitsname=isarm + ".."
	if isarm == 'aarch64':
		cpubits='arm64'
		cpubitsname="arm 64bit.."

	# set caddy archive name
	iszip = "no"
	filename = "caddy_" + whatos + "_" + getbits + "_custom.tar.gz"
	if whatos == 'windows' or whatos == 'darwin':
		import ssl
		iszip = 'yes'
		filename = "caddy_" + whatos + "_" + getbits + "_custom.zip"

	# Check if plugin need to be installed
	if len(sys.argv) == 3:
		if str(sys.argv[2]) in ["-p", "-P", "--plugin", "--plugins"]:
			print(err, "you did not pass any plugins to install")
			exit()
		else:
			print(str(sys.argv[2]), "is unknown parameter!")
			exit()
	if len(sys.argv) >= 3:
		if str(sys.argv[2]) in ["-p", "-P", "--plugin", "--plugins"]:
			plugins = "?plugins=" + sys.argv[3] + "&license=personal"
			printplugin = print("downloading", caddyname, "with plugin", str(sys.argv[3]), "for", cpubitsname)
		else:
			print(str(sys.argv[3]), "is not a valid argument!")
			exit()
	else:
		plugins = "?license=personal"
		printplugin = print("downloading", caddyname, "for", cpubitsname)

	url = "https://caddyserver.com/download/" + whatos + "/" + cpubits + plugins
	printplugin

	if iszip != 'yes':
		try:
			urlretrieve(url, filename)
		except IOError:
			print(err, "is your internet connection ok?")
			exit()
		try:
			tar = tarfile.open(filename)
		except tarfile.ReadError:
			print(err, "corrupted file:", filename)
			exit()
		tar.extractall("caddyserver")
		tar.close()
		print(scs, "downloaded 'caddyserver' to current folder:", cwd)
	else:
		context = ssl._create_unverified_context()
		try:
			urlretrieve(url, cwd + slash + filename, context=context)
		except IOError:
			print(err, "failed to download! is your internet connection ok?")
			exit()
		try:
			with zipfile.ZipFile(filename, "r") as z:
				z.extractall("caddyserver")
		except zipfile.BadZipfile:
			print(err, "corrupted file:", filename)
			exit()

def AddPlugin(plugin):
	# set import link of plugins
	print("importing plugin:", plugin)
	if plugin == 'http.authz':
		plugin = 'github.com/casbin/caddy-authz'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.awses':
		plugin = 'github.com/miquella/caddy-awses'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.awslambda':
		plugin = 'github.com/coopernurse/caddy-awslambda'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.cache':
		plugin = 'github.com/nicolasazrak/caddy-cache'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.cgi':
		plugin = 'github.com/jung-kurt/caddy-cgi'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.cors':
		plugin = 'github.com/captncraig/cors'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.datadog':
		plugin = 'github.com/payintech/caddy-datadog'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.expires':
		plugin = 'github.com/epicagency/caddy-expires'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.filemanager':
		plugin = 'github.com/hacdias/filemanager'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.filter':
		plugin = 'github.com/echocat/caddy-filter'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.forwardproxy':
		plugin = 'github.com/caddyserver/forwardproxy'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.git':
		plugin = 'github.com/abiosoft/caddy-git'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.gopkg':
		plugin = 'github.com/zikes/gopkg'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.grpc':
		plugin = 'github.com/pieterlouw/caddy-grpc'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.hugo':
		plugin = 'github.com/hacdias/filemanager'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.ipfilter':
		plugin = 'github.com/pyed/ipfilter'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.jekyll':
		plugin = 'github.com/hacdias/filemanager'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.jwt':
		plugin = 'github.com/BTBurke/caddy-jwt'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.login':
		plugin = 'github.com/tarent/loginsrv'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.mailout':
		plugin = 'github.com/SchumacherFM/mailout'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.minify':
		plugin = 'github.com/hacdias/caddy-minify'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.nobots':
		plugin = 'github.com/Xumeiquer/nobots'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.prometheus':
		plugin = 'github.com/miekg/caddy-prometheus'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.proxyprotocol':
		plugin = 'github.com/mastercactapus/caddy-proxyprotocol'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.ratelimit':
		plugin = 'github.com/xuqingfeng/caddy-rate-limit'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.realip':
		plugin = 'github.com/captncraig/caddy-realip'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.reauth':
		plugin = 'github.com/freman/caddy-reauth'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.restic':
		plugin = 'github.com/restic/caddy'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.upload':
		plugin = 'github.com/wmark/caddy.upload'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'http.webdav':
		plugin = 'github.com/hacdias/caddy-webdav'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'tls.dns.cloudflare':
		plugin = 'github.com/caddyserver/dnsproviders'
		subprocess.call(['go', 'get', plugin])
		plugin = 'github.com/caddyserver/dnsproviders/cloudflare'

	elif plugin == 'tls.dns.digitalocean':
		plugin = 'github.com/caddyserver/dnsproviders'
		subprocess.call(['go', 'get', plugin])
		plugin = 'github.com/caddyserver/dnsproviders/digitalocean'

	elif plugin == 'tls.dns.dnsimple':
		plugin = 'github.com/caddyserver/dnsproviders'
		subprocess.call(['go', 'get', plugin])
		plugin = 'github.com/caddyserver/dnsproviders/dnsimple'

	elif plugin == 'tls.dns.dnspod':
		plugin = 'github.com/caddyserver/dnsproviders'
		subprocess.call(['go', 'get', plugin])
		plugin = 'github.com/caddyserver/dnsproviders/dnspod'

	elif plugin == 'tls.dns.dyn':
		plugin = 'github.com/caddyserver/dnsproviders'
		subprocess.call(['go', 'get', plugin])
		plugin = 'github.com/caddyserver/dnsproviders/dyn'

	elif plugin == 'tls.dns.exoscale':
		plugin = 'github.com/caddyserver/dnsproviders'
		subprocess.call(['go', 'get', plugin])
		plugin = 'github.com/caddyserver/dnsproviders/exoscale'

	elif plugin == 'tls.dns.gandi':
		plugin = 'github.com/caddyserver/dnsproviders'
		subprocess.call(['go', 'get', plugin])
		plugin = 'github.com/caddyserver/dnsproviders/gandi'

	elif plugin == 'tls.dns.googlecloud':
		plugin = 'github.com/caddyserver/dnsproviders'
		subprocess.call(['go', 'get', plugin])
		plugin = 'github.com/caddyserver/dnsproviders/googlecloud'

	elif plugin == 'tls.dns.linode':
		plugin = 'github.com/caddyserver/dnsproviders'
		subprocess.call(['go', 'get', plugin])
		plugin = 'github.com/caddyserver/dnsproviders/linode'

	elif plugin == 'tls.dns.namecheap':
		plugin = 'github.com/caddyserver/dnsproviders'
		subprocess.call(['go', 'get', plugin])
		plugin = 'github.com/caddyserver/dnsproviders/namecheap'

	elif plugin == 'tls.dns.ovh':
		plugin = 'github.com/caddyserver/dnsproviders'
		subprocess.call(['go', 'get', plugin])
		plugin = 'github.com/caddyserver/dnsproviders/ovh'

	elif plugin == 'tls.dns.rfc2136':
		plugin = 'github.com/caddyserver/dnsproviders'
		subprocess.call(['go', 'get', plugin])
		plugin = 'github.com/caddyserver/dnsproviders/rfc2136'

	elif plugin == 'tls.dns.route53':
		plugin = 'github.com/caddyserver/dnsproviders'
		subprocess.call(['go', 'get', plugin])
		plugin = 'github.com/caddyserver/dnsproviders/route53'

	elif plugin == 'tls.dns.vultr':
		plugin = 'github.com/caddyserver/dnsproviders'
		subprocess.call(['go', 'get', plugin])
		plugin = 'github.com/caddyserver/dnsproviders/vultr'

	elif plugin == 'hook.service':
		plugin = 'github.com/bruhs/caddy-service'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'dns':
		plugin = 'github.com/coredns/coredns'
		subprocess.call(['go', 'get', plugin])

	elif plugin == 'net':
		plugin = 'github.com/pieterlouw/caddy-net/caddynet'
		subprocess.call(['go', 'get', plugin])

	else:
		print(err, "bad plugin:", plugin)
		exit()

	# write to run.go
	inputfile = open('run.go', 'r').readlines()
	write_file = open('run.go','w')
	for line in inputfile:
		if not plugin in line:
			write_file.write(line)
			if 'imported' in line:
				write_file.write('	' + '_ ' + '"' + plugin + '"' + os.linesep) 
	write_file.close()
	print("imported:", plugin)

def Build():
	devnull = open(os.devnull,"w")
	cmd = "where" if whatos == "windows" else "which"
	checkgit = subprocess.call([cmd, 'git'], stdout=devnull, stderr=subprocess.STDOUT)
	if checkgit != 0:
		print(err, 'exec: "git": executable file not found in $PATH')
		exit()
	checkgo = subprocess.call([cmd, 'go'], stdout=devnull, stderr=subprocess.STDOUT)
	if checkgo != 0:
		print(err, 'exec: "go": executable file not found in $PATH')
		exit()

	# get caddy via go
	print("please wait. downloading latest source..")
	subprocess.call(['go', 'get', 'github.com/caddyserver/builds'])
	subprocess.call(['go', 'get', 'github.com/mholt/caddy'])
	os.chdir(caddygo + slash + 'caddymain')

	# Check if plugin need to be installed
	if len(sys.argv) == 3:
		if str(sys.argv[2]) in ["-p", "-P", "--plugin", "--plugins"]:
			print(err, "you did not pass any plugins to build")
			exit()
		else:
			print(str(sys.argv[2]), "is unknown parameter!")
			exit()
	if len(sys.argv) >= 3:
		if str(sys.argv[2]) in ["-p", "-P", "--plugin", "--plugins"]:
			plugins = (sys.argv[3].split(','))
			for word in plugins:
				AddPlugin(word)
		else:
			print(str(sys.argv[3]), "is not a valid argument!")
			exit()

	# build caddy web server
	os.chdir(caddygo)
	print("building caddy web server..")
	subprocess.call(['go', 'run', 'build.go'])
	if os.path.isfile("caddy"):
		os.rename("caddy", cwd + slash + "caddy")
		print(scs, "finised building:", cwd + slash + "caddy")
		exit()
	else:
		print(err, "are you sure all build tools is installed?")

# main commands!
try:
	if str(sys.argv[1]) == "get":
		if os.path.isfile("caddyserver" + slash +"caddy"):
			print(err, "caddy exists: caddyserver/caddy")
			exit()
		if cpubits == "unknown":
			print("unknown architecture!")
			exit()
		Get()

	elif str(sys.argv[1]) == "build":
		Build()
	elif str(sys.argv[1]) == "install":
		devnull = open(os.devnull,"w")
		cmd = "where" if whatos == "windows" else "which"
		checkgit = subprocess.call([cmd, 'git'], stdout=devnull, stderr=subprocess.STDOUT)
		checkgo = subprocess.call([cmd, 'go'], stdout=devnull, stderr=subprocess.STDOUT)
		if checkgit == 0 and checkgo == 0:
			print("found git and go installed!")
			print("executing build script..")
			Build()
			print("executing download command..")
			Get()
		else:
			print("git or go is not installed!")
			print("executing download command..")
			Get()
except KeyboardInterrupt:
	print("Aborted.")
	exit()
