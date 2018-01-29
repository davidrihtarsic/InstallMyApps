#!/usr/bin/env python
from myTUI import Form, Edit, Text, cls, setCursor
import sys
import os
import weakref
import copy

cls()

user_path = os.path.expanduser('~')
user = user_path[user_path.rfind("/")+1:]
download_dir = user_path + '/Downloads/'
opt_dir = '/opt/'
menu_desktop = '/usr/share/applications/'
profile_dir = '/etc/profile.d/'
escapeColorDefault = '\x1B[39m'
escapeColorCmd = '\x1B[38;5;130m'
escapeColorInstalled = '\x1B[32m'
thisAppOutput = escapeColorCmd+'--> '
confirmText = escapeColorDefault+' [y/n]:'

## POSTOPEK INSTALACIJE ########################################
def deBug(info):
	print(info)
	input()

class NovProgram(object):
	_instances = set()

	def __init__(self):
		super(NovProgram, self).__init__()
		self._instances.add(weakref.ref(self))
		self.program_name = ''
		self.index = 0
		self.category = ''
		self.description = ''
		self.arch_yaourt_cmds = []
		self.arch_pacman_cmds=	[]
		self.arch_zsh_cmds= []
		self.check_version_cmd = ''
		self.notes = ''

	@classmethod
	def getinstances(cls):
		dead = set()
		for ref in cls._instances:
			obj = ref()
			if obj is not None:
				yield obj
			else:
				dead.add(ref)
			cls._instances -= dead

	def arch_yaourt_install(self):
		## install from terminal command
		if len(self.arch_yaourt_cmds) != 0:
			for yaourt_cmd in self.arch_yaourt_cmds:
				if self.category == 'Auto':
					if self.version_check():
						#it is alredy installed... skip it!
						pass
					else:
						#it is not installed... install it!
						os.system('yaourt -S --noconfirm '+yaourt_cmd)
				else:
					key = input(thisAppOutput+'Install with YAOURT: '+yaourt_cmd+ confirmText)
					if key == 'y':
						os.system('yaourt -S '+yaourt_cmd)

	def arch_pacman_install(self):
		## install from terminal pacman command
		if len(self.arch_pacman_cmds) != 0:
			for pacman_install in self.arch_pacman_cmds:
				if self.category == 'Auto':
					if self.version_check():
						#it is alredy installed... skip it!
						pass
					else:
						#it is not installed... install it!
						os.system('sudo pacman -S --noconfirm ' + pacman_install)
				else:
					key = input(thisAppOutput+'Install with PACMAN: '+pacman_install+ confirmText)
					if key == 'y':
						os.system('sudo pacman -S ' + pacman_install)

	def arch_run_zsh_cmds(self):
		## Post INSTALL operations #####################################################
		if len(self.arch_zsh_cmds) != 0:
			for arch_zsh_cmds in self.arch_zsh_cmds:
				if self.category == 'Auto':
					key='y'
				else:
					key = input(thisAppOutput+'Execute: '+arch_zsh_cmds+ confirmText)
				if key == 'y':
					os.system(arch_zsh_cmds)

	def version_check(self):
		## KONEC INSTALACIJE samo se navodila in verzija check! ########################
		if len(self.check_version_cmd)>0:
			pckg_name = self.check_version_cmd
		else:
			if (len(self.arch_yaourt_cmds)>0) or (len(self.arch_pacman_cmds)>0):
				if len(self.arch_yaourt_cmds)<len(self.arch_pacman_cmds):
					pckg_name = self.arch_pacman_cmds[0]
				else:
					pckg_name = self.arch_yaourt_cmds[0]
		info_installed_file = os.popen('pacman -Qs '+ pckg_name)
		info_installed_text = info_installed_file.read()
		if len(info_installed_text)>1 :
			#it is alredy installed... 
			sys.stdout.write(thisAppOutput+'Paket : '+ pckg_name +' je ze namescen.' +escapeColorDefault+'\n' )
			sys.stdout.write(escapeColorInstalled + info_installed_text + escapeColorDefault+'\n' )
			return True
		else:
			#it is not installed...
			return False

	def show_notes(self):
		if self.notes != '':
			sys.stdout.write(thisAppOutput+self.notes+''+escapeColorDefault+'\n')	

				
	def install(self):
		sys.stdout.write(	 '###########################################################\n'
							+'## Postopek instalacije programa \n'
							+'## '+escapeColorCmd+ self.program_name+''+escapeColorDefault+'\n'
							+'-----------------------------------------------------------\n')
		if self.description != '':
			new_start = 0
			last_presledek = 0
			for n in range (1, len(self.description)):
				presledek = self.description.find(' ',last_presledek+1,n)
				#testing izpis ne dela najbolje...
				new_line = self.description.find('\n',last_presledek+1,n)
				if (new_line > last_presledek):
					print(escapeColorDefault+self.description[new_start:new_line])
					last_presledek = new_line + 1
					new_start = new_line + 1

				if (new_line > new_start + 59):
					print(escapeColorDefault+self.description[new_start:last_presledek])
					new_start = last_presledek + 1

				if (presledek > new_start + 59):
					print(escapeColorDefault+self.description[new_start:last_presledek])
					new_start = last_presledek + 1 	
				else:
					if (presledek > 0):
					    last_presledek=presledek

			sys.stdout.write(escapeColorDefault+self.description[new_start:]+''+escapeColorDefault+'\n'
							+'###########################################################\n')
		self.arch_pacman_install()
		self.arch_yaourt_install()
		self.arch_run_zsh_cmds()
		self.show_notes()		
		sys.stdout.write(thisAppOutput+'Pritisni [ENTER] za nadaljevanje...'+escapeColorDefault+'\n')
## DEFINICIJA PROGRAMOV ZA INSTALACIJO #########################
def Install_programms():
## HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP ######
	#global Ime_Novega_Programa
	#Ime_Novega_Programa = NovProgram()
	#Ime_Novega_Programa.program_name = ''
	# 	PROGRAME_NAME - ime programa, priporoca se, da je brez presledkov,
	# 	ta besedlni niz se uporabi za prikaz imena programa v menu-ju in
	# 	tudi za ime datoteke *.desktop (/usr/share/applications/ime_programa.desktop).
	#	primer uporabe:
	#	novProgram.program_name='firefox'					
	#Ime_Novega_Programa.description = ''
	# 	DESCRIPTON - string se uporablja za nekaj uvodnega besedila v menuju.
	#	primer uporabe:
	#	novProgram.description=	'Ta program se uporablja za pisanje besedil.\n Uporabljamo'\
	#				'pa ga lahko tudi ta urejanje nastavitev...' 
	#Ime_Novega_Programa.arch_zsh_cmds = []
	#	EXTRA_CMD - niz ukazov, ki bi jih morali vtipkati v terminal po instalacijskem postopku.
	#	Na tem mestu lahko dodate link v /usr/bin/ tako, da lahko zazenete program od koderkoli,
	#	kakor smo to naredili za program thunderbird...
	#	primer uporabe:
	#	Thunderbird.extra_cmd = ['sudo ln -s /opt/thunderbird/thunderbird /usr/bin/thunderbird'] 
	#Ime_Novega_Programa.check_version_cmd = ''
	#	CHECK_VERSION_CMD - string se izvrsi kot cmd ukaz v ternimalu in je namenjen
	#	preverjanju verzije. Ta ukaz se izvede po instalaciji.
	#	primer uporabe:
	#	novProgram = 'nano --version' 
	#Ime_Novega_Programa.notes = ''
	#	NOTES - ko se instalacijski postopek zakljuci se izpise neko besedilo, ki sporoci
	#	uporabniku kaka nadaljna navodila. Naprimer, ce program potrebuje kake dodatne
	#	nastavitve, kot v primeru terminatorja za prikaz podatkov o racunalniku z neofetch.
	#
## Ime_Novega_Programa #########################################
	#global Ime_Novega_Programa
	#Ime_Novega_Programa = NovProgram()
	#Ime_Novega_Programa.program_name = ''
	#Ime_Novega_Programa.arch_pacman_cmds = []
	#Ime_Novega_Programa.arch_yaourt_cmds = []	
	#Ime_Novega_Programa.arch_zsh_cmds = []
	#Ime_Novega_Programa.check_version_cmd = ''
	#Ime_Novega_Programa.notes = ''
## GIT #########################################################
	global git
	git = NovProgram()
	git.program_name = 'git'					#ime naj bo brez presledkov
	git.category = 'System'
	git.description = 'Protokol za skrbno spremljanje verzij'\
					'razvojnih programov.'					#neko besedilo za opis
	git.arch_pacman_cmds = ['git']
	git.notes = ''
	git.arch_zsh_cmds = ['git config --global user.email "david.rihtarsic@gmail.com"',
					 'git config --global user.name "davidrihtarsic"',
					 'git clone https://github.com/davidrihtarsic/Arduino-serial-API.git ~/Files/GitHub_noSync/Arduino-serial-API',
					 'git clone https://github.com/davidrihtarsic/ArchLabs.git ~/Files/GitHub_noSync/ArchLabs',
					 'git clone https://github.com/davidrihtarsic/InstallMyApps.git ~/Files/GitHub_noSync/InstallMyApps',
					 'git clone https://github.com/davidrihtarsic/myLinuxNotes.git ~/Files/GitHub_noSync/myLinuxNotes',
					 'git clone https://github.com/davidrihtarsic/Korad3005p.git ~/Files/GitHub_noSync/Korad3005p',
					 'git clone https://github.com/davidrihtarsic/BunsenLab.git ~/Files/GitHub_noSync/BunsenLab',
					 'git clone https://github.com/davidrihtarsic/RobDuino.git ~/Files/GitHub_noSync/RobDuino',
					 'git clone https://github.com/davidrihtarsic/ArduinoCNC-DCmotors.git ~/Files/GitHub_noSync/CNC-ArduinoDCmotors'
					 ]
## Thunar ######################################################
	global Thunar
	Thunar = NovProgram()
	Thunar.program_name = 'Thunar'
	Thunar.category ='System'
	Thunar.description = 'Thunar is a file manager for Linux and other Unix-like systems, written using the GTK+ 2 toolkit, and shipped with Xfce version 4.4 RC1 and later. Thunar is developed by Benedikt Meurer, and was originally intended to replace XFFM, Xfces previous file manager. It was initially called Filer but was changed to Thunar due to a name clash.'
	Thunar.arch_yaourt_cmds = [	'thunar']

	global Thunar_samba
	Thunar_samba = NovProgram()
	Thunar_samba.program_name = 'Thunar_samba'
	Thunar_samba.category ='System'
	Thunar_samba.description = 'Thunar_samba support.'
	Thunar_samba.arch_yaourt_cmds = [	'thunar-shares-plugin',
										'gvfs-smb']
	Thunar.notes = 'You shuld REBOOT... (not just log-OUT/log-IN)'
## Nemo ######################################################
	global Nemo
	Nemo = NovProgram()
	Nemo.program_name = 'Nemo'
	Nemo.category ='System'
	Nemo.description = 'Nemo is a fork of GNOME Files. It is also the default file manager of the Cinnamon desktop. Nemo is based on the Files 3.4 code. It was created as a response to the changes in Files 3.6 which saw features such as type ahead find and split pane view removed.'
	Nemo.arch_pacman_cmds = [	'nemo',
								'nemo-fileroller',
								'nemo-preview',
								'nemo-terminal']
	Nemo.notes = ''
## PDFtk ######################################################
	global PDFtk
	PDFtk = NovProgram()
	PDFtk.program_name = 'PDFtk'
	PDFtk.category ='Other'
	PDFtk.description = 'PDF Tools'
	PDFtk.arch_yaourt_cmds = [	'pdftk' ]
	PDFtk.notes = ''
## PanDoc ######################################################
	global PanDoc
	PanDoc = NovProgram()
	PanDoc.program_name = 'PanDoc'
	PanDoc.category ='Misc'
	PanDoc.description = 'PDF Tools'
	PanDoc.arch_pacman_cmds = [	'pandoc',
								'texlive-latexextra',
								'texlive-fontsextra' ]
	PanDoc.notes = ''
## NMON ########################################################
	global nmon
	nmon = NovProgram()
	nmon.program_name = 'nmon'
	nmon.category = 'System'
	nmon.description = 'Spremljanje procesov, diska...'
	nmon.arch_pacman_cmds = ['nmon']
## WAVEMON #####################################################
	global wavemon
	wavemon = NovProgram()
	wavemon.program_name = 'wavemon'					#ime naj bo brez presledkov
	wavemon.category = 'System'
	wavemon.description = 'Program za monitoring wireless omrezj'					#neko besedilo za opis
	wavemon.arch_pacman_cmds = ['wavemon']					#ime za apt-get
## NMAP ########################################################
	global nmap
	nmap =NovProgram()
	nmap.program_name = 'nmap'
	nmap.category = 'System'
	nmap.description = 'map ("Network Mapper") is a free and open source (license) utility for network discovery and security auditing. Many systems and network administrators also find it useful for tasks such as network inventory, managing service upgrade schedules, and monitoring host or service uptime. Nmap uses raw IP packets in novel ways to determine what hosts are available on the network, what services (application name and version) those hosts are offering, what operating systems (and OS versions) they are running, what type of packet filters/firewalls are in use, and dozens of other characteristics.'
	nmap.arch_pacman_cmds = ['nmap']
## ADB  to-do ##################################################
## ARCH config files ###########################################
	global Arch_config
	Arch_config = NovProgram()
	Arch_config.program_name = 'Upadate .config'
	Arch_config.category = 'System'
	Arch_config.description = 'Moji .config fili iz GitHuba...'
	Arch_config.arch_zsh_cmds = ['cp -r -v ~/Files/GitHub_noSync/ArchLabs/MyDotFiles/. ~'
							]
	Arch_config.check_version_cmd = 'git'
## alias WEATHER ###############################################
#	global weather
#	weather = NovProgram()
#	weather.program_name = 'weather'					#ime naj bo brez presledkov
#	weather.category = 'Other'
#	weather.description = 'izpis vremena za tri dni v terminalnem oknu'
#					#neko besedilo za opis
#	weather.add_bash_parameter = ["\nalias weather='curl wttr.in/~begunje'"]			#text ki je za dodat v .bash 
#	weather.notes = ''
## FileZilla ###################################################
	# NOT testet yet ... - was preinstalled on BL
	#global FileZilla
	#FileZilla = NovProgram()
	#FileZilla.program_name = '_to_do_FileZilla'
	#FileZilla.category = 'Other'
	#FileZilla.description = 'FileZilla is open source software distributed free of charge under the terms of the GNU General Public License'					
	#FileZilla.apt_get_name = 'FileZilla'
	##FileZilla.notes = ''
## python-serial ###############################################
	#test OK @ BL 64bit (David)
	#global python_serial
	#python_serial = NovProgram()
	#python_serial.program_name = '_to_do_python-serial'
	#python_serial.category = 'System'
	#python_serial.description = 'This module encapsulates the access for the serial port. It provides backends for Python running on Windows, OSX, Linux, BSD (possibly any POSIX compliant system) and IronPython. The module named "serial" automatically selects the appropriate backend.'
	#python_serial.apt_get_name = 'python-serial'
	##python-serial.notes = ''
## FreeFileSync ################################################
	global FreeFileSync
	FreeFileSync = NovProgram()
	FreeFileSync.program_name = 'FreeFileSync'
	FreeFileSync.category = 'System'
	FreeFileSync.description = 'FreeFileSync is a free Open Source software that helps you synchronize files and synchronize folders for Windows, Linux and macOS. It is designed to save your time setting up and running backup jobs while having nice visual feedback along the way.'
	FreeFileSync.arch_yaourt_cmds = ['freefilesync']
## ARDUINO #####################################################
	global Arduino
	Arduino = NovProgram()
	Arduino.program_name = 'ArduinoIDE'
	Arduino.category = 'Programming'
	Arduino.description = 'Arduino je mikrokrmilnik na maticni plosci, ki je zasnovan '\
						'tako da bi bil postopek z uporabo elektronike v multidisci'\
						'plinarnih projektih, bolj dostopen. Strojno opremo sestavljajo '\
						'odprtokodna oblika plosce in 8-bitni mikrokrmilnik Atmel AVR '\
						'ali 32-bitni Atmel ARM. Programska oprema je sestavljena iz '\
						'standardnega programskega jezika, prevajalnika in zagonskega '\
						'nalagalnika, ki se izvaja na mikrokrmilniku. Razvojne plosce '\
						'Arduino so naprodaj ze sestavljene ali pa v sestavi sam izvedbi. '\
						'Mikrokrmilnik so razvili na soli oblikovanja v italijanskem '\
						'mestu Ivrea in predstavlja enega zgodnjih mejnikov v gibanju '\
						'odprtokodne strojne opreme.'
	Arduino.arch_pacman_cmds =['arduino']
	Arduino.arch_zsh_cmds = ['sudo usermod -a -G uucp '+ user]
	# tole je treba še zrihtat !!!
	Arduino.notes = 'NASTAVITI JE POTREBNO "SERIAL PORT PERMITIONS"!\n'\
					'poglej na: http://playground.arduino.cc/Linux/All#Permission\n'\
					'1. -> ls -l /dev/ttyUSB* ali ls -l /dev/ttyACM*\n'\
					'	dobimo:\n'\
					'	crw-rw---- 1 root dialout 188, 0  5 apr 23.01 ttyACM0\n'\
					'	kjer je "dailout" - group name\n'\
					'2. -> sudo usermod -a -G group-name username\n'\
					'3. log-OUT & log-IN'
## QCAD ########################################################
	global qCAD
	qCAD = NovProgram()
	qCAD.program_name = 'Qcad'
	qCAD.category = 'Graphics'
	qCAD.description = 'Qcad je racunalnisko podprto orodje za 2D nacrtovanje in '\
						'risanje. Zacetki razvoja segajo v leto 1999, ko je programsko '\
						'orodje nastalo kot rezultat spinoff projekta izdelave CAD '\
						'sistema. Z njim izdelamo tehnicne risbe (nacrti zgradb, '\
						'njihovih notranjosti, mehanski deli, sheme, diagrami ipd.). '\
						'Uporaben je na razlicnih tehniskih podrocjih: strojnistvo, '\
						'lesarstvo, gradbenistvo, arhitektura, geodezija in elektrotehnika.'
	qCAD.arch_pacman_cmds = ['qcad']
## FREECAD #####################################################
	global FreeCAD
	FreeCAD = NovProgram()
	FreeCAD.program_name = 'FreeCAD'
	FreeCAD.category = 'Graphics'
	FreeCAD.description = 'Orodje za tehnisko risanje.'
	FreeCAD.arch_pacman_cmds =['freecad']
## Skype #######################################################
	global Skype
	Skype = NovProgram()
	Skype.program_name = 'Skype'
	Skype.category = 'Media'
	Skype.description = 'Komunikacija preko interneta...'
	Skype.arch_yaourt_cmds =['skypeforlinux-stable-bin']
	Skype.check_version_cmd = 'skypeforlinux'
## Stellarium ##################################################
	global stellarium
	stellarium = NovProgram()
	stellarium.program_name = 'Stellarium'
	stellarium.category = 'Other'
	stellarium.description = 'Zvezvde...'
	#stellarium.pre_install_cmds = []					
	stellarium.arch_pacman_cmds = ['pacman -S stellarium']
## Fritzing ####################################################
    #32 bit BL tested
	global Fritzing
	Fritzing = NovProgram()
	Fritzing.program_name = 'Fritzing'
	Fritzing.category = 'Other'
	Fritzing.description = 'Program za risanje vezij oziroma elektrotehniskih shem'
	Fritzing.arch_yaourt_cmds = ['fritzing']
## Audacity ####################################################
	global audacity
	audacity = NovProgram()
	audacity.program_name = 'Audacity'
	audacity.category = 'Media'
	audacity.description = 'Audacity is free, open source, cross-platform audio software for multi-track recording and editing.'					
	audacity.arch_yaourt_cmds = ['audacity']
	#audacity.notes = ''
## bCNC ########################################################
	#test OK @ BL 64-bit (David)
	global bCNC
	bCNC = NovProgram()
	bCNC.program_name = 'bCNC'
	bCNC.category = 'Misc'
	bCNC.description = 'An advanced fully featured g-code sender for GRBL. bCNC is a cross platform program (Windows, Linux, Mac) written in python. The sender is robust and fast able to work nicely with old or slow hardware like Rasperry PI (As it was validated by the GRBL mainter on heavy testing).'
	bCNC.arch_yaourt_cmds = ['bcnc']
## ECLIPSEC ####################################################
	#testing...  @ BL 64-bit (David)
	# instalacija dela...
	global eclipse
	eclipse = NovProgram()
	eclipse.program_name = 'Eclipse'
	eclipse.category = 'Programming'
	eclipse.description = 'Programsko okolje ...'
	eclipse.arch_yaourt_cmds = ['eclipse-cpp']
## QT5 Creator #################################################
	global QT5_creator
	QT5_creator = NovProgram()
	QT5_creator.program_name = 'QT5 Creator'
	QT5_creator.category = 'Programming'
	QT5_creator.description = 'Qt Creator provides a cross-platform, complete integrated development environment (IDE) for application developers to create applications for multiple desktop, embedded, and mobile device platforms, such as Android and iOS. It is available for Linux, macOS and Windows operating systems. For more information, see Supported Platforms.'
	QT5_creator.arch_yaourt_cmds = ['qtcreator']
## Stencyl #####################################################
	#64 bit BL tested
	global Stencyl
	Stencyl = NovProgram()
	Stencyl.program_name = 'Stencyl'
	Stencyl.category = 'Other'
	Stencyl.description = "Stencyl isn't your average game creation software. It's a gorgeous, intuitive toolset that accelerates your workflow and then gets out of the way. We take care of the essentials, so you can focus on what's important - making your game yours."
	Stencyl.arch_yaourt_cmds = ['stencyl']
## PopCornTime #################################################
	global PopCornTime
	PopCornTime = NovProgram()
	PopCornTime.program_name = 'PopCornTime'
	PopCornTime.category = 'Media'
	PopCornTime.arch_yaourt_cmds =['popcorntime-bin']
	PopCornTime.description = "Popcorn Time is constantly searching all over the web for the best torrents from the most important sites."
## Gimp ########################################################
	global Gimp
	Gimp = NovProgram()
	Gimp.program_name = 'Gimp'
	Gimp.category = 'Preinstalled'
	Gimp.arch_pacman_cmds =['gimp']
	Gimp.description = "GIMP is a cross-platform image editor available for GNU/Linux, OS X, Windows and more operating systems. It is free software, you can change its source code and distribute your changes."
## LibreOffice #################################################
	global LibreOffice
	LibreOffice = NovProgram()
	LibreOffice.program_name = 'LibreOffice'
	LibreOffice.category = 'Preinstalled'
	LibreOffice.arch_pacman_cmds =['libreoffice']
	LibreOffice.description = "LibreOffice is a powerful office suite – its clean interface and feature-rich tools help you unleash your creativity and enhance your productivity. LibreOffice includes several applications that make it the most powerful Free and Open Source office suite on the market."
## Terminator ##################################################
	global Terminator
	Terminator = NovProgram()
	Terminator.program_name = 'Terminator'
	Terminator.category = 'Preinstalled'
	Terminator.arch_pacman_cmds =['terminator']
	Terminator.description = ""
## PhoronixTestSuite ###########################################
	global PhoronixTestSuite
	PhoronixTestSuite = NovProgram()
	PhoronixTestSuite.program_name = 'PhoronixTestSuite'
	PhoronixTestSuite.category = 'Testing'
	PhoronixTestSuite.arch_yaourt_cmds =['phoronix-test-suite']
	PhoronixTestSuite.description = 'The Phoronix Test Suite makes the process of carrying out automated tests incredibly simple. The Phoronix Test Suite will take care of the entire test process from dependency management to test download/installation, execution, and result aggregation.'
## GoogleChrome ################################################
	global GoogleChrome
	GoogleChrome = NovProgram()
	GoogleChrome.program_name = 'GoogleChrome'
	GoogleChrome.category = 'Internet'
	GoogleChrome.arch_yaourt_cmds =['google-chrome']
	GoogleChrome.description = "Chrome is designed to be fast in every possible way. It's quick to start up from your desktop, loads web pages in a snap, and runs complex web applications lightning fast."
## Dolphin ################################################
	global Dolphin
	Dolphin = NovProgram()
	Dolphin.program_name = 'Dolphin'
	Dolphin.category = 'Internet'
	Dolphin.arch_pacman_cmds =['dolphin','konsole']
	Dolphin.arch_yaourt_cmds = ['fsearch-git','kdegraphics-thumbnailers']
	Dolphin.description = 'Dolphin is a lightweight file manager. It has been designed with ease of use and simplicity in mind, while still allowing flexibility and customisation. This means that you can do your file management exactly the way you want to do it.'
## MOJ IZBOR ######################
	global auto_programe1
	auto_programe1 = NovProgram()
	autoInstallProgram(auto_programe1,Arch_config)
	
	global auto_programe2
	auto_programe2 = NovProgram()
	autoInstallProgram(auto_programe2,Gimp)
	
	global auto_programe3
	auto_programe3 = NovProgram()
	autoInstallProgram(auto_programe3,audacity)
	
	global auto_programe4
	auto_programe4 = NovProgram()
	autoInstallProgram(auto_programe4,Thunar)
	
	global auto_programe5
	auto_programe5 = NovProgram()
	autoInstallProgram(auto_programe5,Thunar_samba)
	
	global auto_programe6
	auto_programe6 = NovProgram()
	autoInstallProgram(auto_programe6,qCAD)
	
	global auto_programe7
	auto_programe7 = NovProgram()
	autoInstallProgram(auto_programe7,LibreOffice)

	global auto_programe8
	auto_programe8 = NovProgram()
	autoInstallProgram(auto_programe8,Terminator)

	global auto_programe9
	auto_programe9 = NovProgram()
	autoInstallProgram(auto_programe9,FreeFileSync)

	global auto_programe10
	auto_programe10 = NovProgram()
	autoInstallProgram(auto_programe10,Fritzing)

	global auto_programe11
	auto_programe11 = NovProgram()
	autoInstallProgram(auto_programe11,Arduino)

	global auto_programe12
	auto_programe12 = NovProgram()
	autoInstallProgram(auto_programe12,Skype)

	global auto_programe13
	auto_programe13 = NovProgram()
	autoInstallProgram(auto_programe13,GoogleChrome)

def autoInstallProgram(destination, coppied):
	destination.program_name = coppied.program_name
	destination.arch_pacman_cmds = coppied.arch_pacman_cmds
	destination.arch_yaourt_cmds = coppied.arch_yaourt_cmds
	destination.arch_zsh_cmds = coppied.arch_zsh_cmds
	destination.check_version_cmd = coppied.check_version_cmd
	destination.category = 'Auto'

Install_programms()
# find programs and categorize them
#Force Auto and System as first
all_categorys = ['Auto','System']
category_programs = [0,0]
all_program_manes = []
for program in NovProgram.getinstances():
	all_program_manes.append(program.program_name)
	if program.category in all_categorys:
		i = all_categorys.index(program.category)
		category_programs[i] += 1
	else:
		all_categorys.append(program.category)
		category_programs.append(1)

def makeAllProgramForms():
	global allForms
	allForms = []
	global editProgramms
	editProgramms = []
	global colons
	x = 4
	#y = 4
	dx = 28 # max od program name
	#terminal = os.get_terminal_size()
	#width = terminal.columns
	#colons = width//
	
	colons = 3
	if colons == 1:
		dy = category_programs[0] +4
	else:
		dy = max(category_programs)+4 # max od category_programs
	global programID
	programID = 0
	for category in all_categorys:
		col = len(allForms)%colons
		row = len(allForms)//colons
		x = col * (dx + 1) + 4
		if len(allForms)>colons:
			#smo že v 1.,2.,3.. vrsti
			y = allForms[len(allForms)-colons].y +allForms[len(allForms)-colons].dy
		else:
			#smo še v 0. vrsti
			y = (dy * row) + 4
		dy = 4+ max( category_programs[n] for n in range((row*colons),((row*colons)+colons)))
		allForms.append(Form(category,x,y,dx,dy))
		#filaj programe po kategorijah
		nthCategoryProgram = 0
		for program in NovProgram.getinstances():
			if program.category == all_categorys[len(allForms)-1]:
				programID += 1
				nthCategoryProgram +=1
				program.index = programID
				editX = allForms[len(allForms)-1].x +2
				editY = allForms[len(allForms)-1].y + nthCategoryProgram +1
				editText = '(' + str(programID) + ')'
				editProgramms.append(Edit(editText, editX, editY))
				editProgramms[programID-1].new_value(program.program_name)

def MakeHelpForm():
	HotKeys = [	'--Menu------------------',
				'n      - inst. program',
				'[u]    - Update & Upgrade',
				'[ENTER]- MAIN MENU',
				'[q]    - EXIT'
				]

	x = allForms[0].x + (allForms[0].dx +1) * colons 
	y = allForms[0].y
	dx = allForms[0].dx
	dy = 0
	col = len(allForms)%colons
	row = len(allForms)//colons
	for n in range(0, row):
		dy += allForms[n*colons].dy
	allForms.append(Form('Auto',x,y,dx,dy))

	nthCategoryProgram = 0
	for program in NovProgram.getinstances():
			if program.category == 'Auto':
				global programID
				programID += 1
				nthCategoryProgram +=1
				program.index = programID
				editX = allForms[len(allForms)-1].x + 2
				editY = allForms[len(allForms)-1].y + nthCategoryProgram +1 
				editText = '(' + str(programID) + ')'
				editProgramms.append(Edit(editText, editX, editY))
				editProgramms[programID-1].new_value(program.program_name)

	t_Keys = []
	x = allForms[len(allForms)-1].x
	y = allForms[len(allForms)-1].y + allForms[len(allForms)-1].dy - len(HotKeys)-2
	for n in range(0, len(HotKeys)):
		t_Keys.append(Text(HotKeys[n], x + 2 ,y+n+1))
	

# MAIN PROGRAM ##############################################
def Main():
	#remove category Auto
	all_categorys.remove('Auto')
	num_of_auto_programs = category_programs.pop(0)

	makeAllProgramForms()
	MakeHelpForm()
	
	all_categorys.insert(0,'Auto')
	category_programs.insert(0,num_of_auto_programs)

	y = allForms[len(allForms)-1].dy +4
	setCursor(1,y)

key = ''
cls()
Main()
Main()
#while (editCmd.value != 'q'):
while (key != 'q'):
	key = input('Cmd::')
	programe_index=(i for i in range(50))
	next(programe_index)
	if key == '':
		cls()
		Main()
	else:
		# preglej vse programe...
		for obj in NovProgram.getinstances():
			if key == str(obj.index):
				obj.install()
				key = ''
		if key == 'u' :
			os.system('sudo pacman -Syu')
			os.system('yaourt -Syua')
		elif key in all_categorys:
			for program in NovProgram.getinstances():
				if program.category == key:
					program.install()
		else:	
			os.system(key)	
cls()