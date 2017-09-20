#!/usr/bin/env python
from myTUI import Form, Edit, Text, cls, setCursor
import sys
import os

cls()

user_path = os.path.expanduser('~')
user = user_path[user_path.rfind("/")+1:]
download_dir = user_path + '/Downloads/'
opt_dir = '/opt/'
menu_desktop = '/usr/share/applications/'
profile_dir = '/etc/profile.d/'
escapeColorDefault = '\x1B[39m'
escapeColorCmd = '\x1B[38;5;130m'
thisAppOutput = escapeColorCmd+'--> '
confirmText = escapeColorDefault+' [y/n]:'
VsiProgrami = []
n_systemPrograms = 19
## POSTOPEK INSTALACIJE ########################################
class NovProgram(object):
	"""docstring for NovProgram"""
	def __init__(self):
		super(NovProgram, self).__init__()
		self.program_name = ''
		self.description = ''
		self.pre_install_cmds = []
		self.apt_get_name = ''
		self.check_version_cmd = ''
		self.deb_package_path = ''
		self.deb_package_file = ''
		self.deb_package_path_32 = ''
		self.deb_package_file_32 = ''
		self.deb_package_path_64 = ''
		self.deb_package_file_64 = ''
		self.tar_package_path = ''
		self.tar_package_file = ''
		self.tar_package_path_32 = ''
		self.tar_package_file_32 = ''
		self.tar_package_path_64 = ''
		self.tar_package_file_64 = ''
		self.tar_destination = ''
		self.tar_extra_cmds = [] 	#extra commande, ce je se kaj za narest...
		self.extra_cmd = []			#se ene extra cmd ... ce je se kaj...
		self.program_desktop = []	#vsebina v program.desktop
		self.add_path_profile_variable  = '' 
		self.add_bash_parameter= []
		self.notes = ''
		self.arhitecture_64bit = False
		self.arhitecture_32bit = False
		self.arhitecture_bit_num = 0
		if sys.maxsize > 2**32 :
			self.arhitecture_64bit = True
			self.arhitecture_bit_num = 64
		else:
			self.arhitecture_32bit = True
			self.arhitecture_bit_num = 32

	def install_apt_cmd(self):
		## Instal from special apt-get command ... #####################################
		if len(self.pre_install_cmds) != 0:
			for pre_cmd in self.pre_install_cmds:
				key = raw_input(thisAppOutput+'execute:'+pre_cmd+ confirmText)
				if key == 'y':
					os.system(pre_cmd)
		if self.apt_get_name != '':
		## Instal from clasical apt-get commend... #####################################
			#ce smo vpisali apt-get podatke potem...
			sys.stdout.write(thisAppOutput+'Preverjam apt-get paket: ' + self.apt_get_name +escapeColorDefault+'\n' )
			os.system('apt-cache policy ' + self.apt_get_name)
			key = raw_input(thisAppOutput+'Namestim preko apt-get... ?'+confirmText)
			if key == 'y':
				os.system('sudo apt-get install ' + self.apt_get_name)

	def install_DEB_package(self):
		## Install form DEB package ###################################################
		#if self.deb_package_file != '':
		if (self.deb_package_file !='' or
		(self.deb_package_file_64 != '' and self.arhitecture_64bit ) or
		(self.deb_package_file_32 != '' and self.arhitecture_32bit )):
			#Najprej poglejmo kaksno arhitekturo imamo
			if (self.deb_package_file_64 != '' and self.arhitecture_64bit ):
				sys.stdout.write(thisAppOutput+'Kaze, da imate 64bit arhitekturo...'+escapeColorDefault+'\n')
				temp_deb_package_path = self.deb_package_path_64
				temp_deb_package_file = self.deb_package_file_64
			elif (self.deb_package_file_32 != '' and self.arhitecture_32bit):
				sys.stdout.write(thisAppOutput+'Kaze, da imate 32bit arhitekturo...'+escapeColorDefault+'\n')
				temp_deb_package_path = self.deb_package_path_32
				temp_deb_package_file = self.deb_package_file_32
			else:
				sys.stdout.write(thisAppOutput+'Ne glede na arhitekturo...'+escapeColorDefault+'\n')
				temp_deb_package_path = self.deb_package_path
				temp_deb_package_file = self.deb_package_file
				#-------------------------------------------------
			#ce je vpisan deb paket potem ...
			#najprej preveri, ce ga slucajno ze imamo v Downloadu...
			#ce ne pojdi na internet...
			if not os.path.isfile(download_dir+temp_deb_package_file):
				#ce file ne obstaja gremo gledat na internet...
				sys.stdout.write(thisAppOutput+'Preverjam DEB package...'+escapeColorDefault+'\n')
				os.system('wget --spider -v '+temp_deb_package_path+temp_deb_package_file)
				key = raw_input(thisAppOutput+'Prenesi v '+download_dir+ confirmText)
				if key == 'y':
					os.system('wget '+ temp_deb_package_path + temp_deb_package_file + ' --directory-prefix='+download_dir )
			#pokazi direktorij Download
			if os.path.isfile(download_dir+temp_deb_package_file):
				sys.stdout.write(thisAppOutput+'Nasel:'+escapeColorDefault+'\n')
				os.system('ls -all ' + download_dir)
				key = raw_input(thisAppOutput+'Namesti DEB package: ' + temp_deb_package_file + confirmText)
				if key == 'y':
					os.system('sudo dpkg -i ' + download_dir + temp_deb_package_file)
					sys.stdout.write(thisAppOutput+'Namestitev koncana...'+escapeColorDefault+'\n')	
				key = raw_input(thisAppOutput+'Izbrisi datoteko:'
								+ download_dir + temp_deb_package_file+'*'
								+ confirmText)
				if key == 'y':
					os.system('rm -v ' + download_dir + temp_deb_package_file)
					#sys.stdout.write(thisAppOutput+'Izprisano:'+escapeColorDefault+'\n')
					#os.system('ls -all ' + download_dir)
			else:
				sys.stdout.write(thisAppOutput+'Paketa: '+ temp_deb_package_file +' nismo nasli...'+escapeColorDefault+'\n')

	def install_TAR_package(self):
		## Install form TAR **** special !!! ###########################################
		if (self.tar_package_file !='' or
		(self.tar_package_file_64 != '' and self.arhitecture_64bit ) or
		(self.tar_package_file_32 != '' and self.arhitecture_32bit )):
			#Najprej poglejmo kaksno arhitekturo imamo
			if (self.tar_package_file_64 != '' and self.arhitecture_64bit ):
				sys.stdout.write(thisAppOutput+'Kaze, da imate 64bit arhitekturo...'+escapeColorDefault+'\n')
				temp_tar_package_path = self.tar_package_path_64
				temp_tar_package_file = self.tar_package_file_64
			elif (self.tar_package_file_32 != '' and self.arhitecture_32bit):
				sys.stdout.write(thisAppOutput+'Kaze, da imate 32bit arhitekturo...'+escapeColorDefault+'\n')
				temp_tar_package_path = self.tar_package_path_32
				temp_tar_package_file = self.tar_package_file_32
			else:
				sys.stdout.write(thisAppOutput+'Ne glede na arhitekturo...'+escapeColorDefault+'\n')
				temp_tar_package_path = self.tar_package_path
				temp_tar_package_file = self.tar_package_file
			#Najprej zloadas tar file ... izi bizi...
			if not os.path.isfile(download_dir+temp_tar_package_file):
				#ce file ne obstaja gremo gledat na internet...
				sys.stdout.write(thisAppOutput+'Preverjam TAR package...'+escapeColorDefault+'\n')
				os.system('wget --spider -v '+temp_tar_package_path+temp_tar_package_file)
				key = raw_input(thisAppOutput+'Prenesi v '+download_dir+ '?'+confirmText)
				if key == 'y':
					os.system('wget '+ temp_tar_package_path + temp_tar_package_file + ' --directory-prefix='+download_dir )
			#pokazi direktorij Download
			if os.path.isfile(download_dir+temp_tar_package_file):
				sys.stdout.write(thisAppOutput+'Nasel:'+escapeColorDefault+'\n')
				os.system('ls -all ' + download_dir)
				if self.tar_destination == '':
					key = raw_input(thisAppOutput+'Razpakiraj TAR package: '
									+ temp_tar_package_file +
									' v ' + download_dir + '?'+confirmText)
					if key == 'y':
						os.system('tar -xvf '+ download_dir+temp_tar_package_file 
								+' --directory '+ download_dir)
				else:
					key = raw_input(thisAppOutput+'Razpakiraj TAR package: '
									+ temp_tar_package_file +
									' v ' + self.tar_destination + '?'+confirmText)
					if key == 'y':
						if not os.path.isdir(self.tar_destination):
							#ce dir se ne obstaja ga ustvari...
							os.system('sudo mkdir ' + self.tar_destination)
						os.system('sudo tar -xvf '+download_dir+temp_tar_package_file
									+' --directory '+ self.tar_destination)
				# Izbrisi kar smo zloadali... da pocistimo za seboj...
				key = raw_input(thisAppOutput+'Izbrisi datoteko:'
									+ download_dir + temp_tar_package_file+'*'
									+ confirmText)
				if key == 'y':
					os.system('rm -v ' + download_dir + temp_tar_package_file+'*')
					#sys.stdout.write(thisAppOutput+'Izbrisano:'+escapeColorDefault+'\n')
					#os.system('ls -all ' + download_dir)
			else:
				sys.stdout.write(thisAppOutput+'Datoteke: '+download_dir+temp_tar_package_file+' nismo nasli...'+escapeColorDefault+'\n')

			## INSTALATION SOURCE CODE #######################################################
				# ok sedaj naj bi bilo razpakirano... kjerkoli pac ze...
				#ja nic zej pa ce je treba se kako EXTRA CMD narest!!!
				#naprimer kak make, make install, itd
				#skratka izvrsimo komande, ki jih najdemo v :
				#self.tar_extra_cmds = ['make','make install']
			if len(self.tar_extra_cmds) != 0:	
				for extra_cmd in self.tar_extra_cmds:
					key = raw_input(thisAppOutput+'execute:'+extra_cmd+confirmText)
					if key == 'y':
						os.system(extra_cmd)

	def add_PATH_parameter(self):
		## dodajanje v path script #######################################################			
		#sudo sh -c 'echo "export PATH=\$PATH:/opt/arduino-1.8.1" >> /etc/profile.d/arduino_path.sh'	
		if len(self.add_path_profile_variable) != 0:
			# ce in nastavljeno pot... to dodamo v $PATH
			key = raw_input(thisAppOutput+'Dodaj pot:'+ self.add_path_profile_variable + ' v $PATH ?'+confirmText)
			if key == 'y':
				if (open(user_path + '/.bashrc', 'r').read().find(self.add_path_profile_variable)>0):
					sys.stdout.write(thisAppOutput+'Pot: '+ self.add_path_profile_variable +' ze dodana v : '+ user_path + '/.bashrc...'+escapeColorDefault+'\n')
				else:
					with open(user_path + '/.bashrc','a') as f:
						f.write('\n#dodajanje '+self.program_name+' poti v path\n')
						f.write('export PATH=$PATH:'+self.add_path_profile_variable+'\n')
						f.close()

	def add_BASH_parameter(self):
		if len(self.add_bash_parameter) != 0:
			# ce in nastavljeno pot... to dodamo v $PATH
			for text in self.add_bash_parameter:
				key = raw_input(thisAppOutput+'Dodaj text: '+ text + ' v ~/.bashrc ?'+confirmText)
				if key == 'y':
					if (open(user_path + '/.bashrc', 'r').read().find(text)>0):
						sys.stdout.write(thisAppOutput+'Text: '+ text +' ze dodano v : '+ user_path + '/.bashrc...'+escapeColorDefault+'\n')
					else:
						# tu naj gremo cez vse nize v parametru...
						with open(user_path + '/.bashrc','a') as f:
							f.write(text)
						f.close()

	def run_bash_cmds(self):
		## Post INSTALL operations #####################################################
		if len(self.extra_cmd) != 0:
			for extra_cmd in self.extra_cmd:
				key = raw_input(thisAppOutput+'execute:'+extra_cmd+ confirmText)
				if key == 'y':
					os.system(extra_cmd)
	
	def make_destop_file(self):
		## Dodajanje program.desktop datoteke v /usr/share/applications/ ################
		if len(self.program_desktop) != 0:
			# test ce je kaj not: sys.stdout.write(self.program_desktop[0])
			# sudo sh -c 'echo "export PATH=\$PATH:/opt/arduino-1.8.1" >> /etc/profile.d/arduino_path.sh'
			key = raw_input(thisAppOutput+'Naredi menu:'+ menu_desktop + self.program_name+ '.desktop ?'+confirmText)
			if key == 'y':
				#naredi le ce fajl ne obstaja...
				if not os.path.isfile(menu_desktop + self.program_name+ '.desktop'):
					for menu in self.program_desktop:
						sudo_txt=[]
						sudo_txt.append('sudo sh -c ')
						sudo_txt.append("'echo ")
						sudo_txt.append('"'+ menu + '"')
						sudo_txt.append(" >> "+ menu_desktop + self.program_name + ".desktop'")
						#sys.stdout.write(sudo_txt[0]+sudo_txt[1]+sudo_txt[2]+sudo_txt[3])
						os.system(sudo_txt[0]+sudo_txt[1]+sudo_txt[2]+sudo_txt[3])
	
	def version_check(self):
		## KONEC INSTALACIJE samo se navodila in verzija check! ########################		
		if self.check_version_cmd != '':
			#ce smo vpisali preverjanje verzije -> POTEM
			sys.stdout.write(thisAppOutput+'Preverjam verzijo...'+escapeColorDefault+'\n')
			os.system(self.check_version_cmd)
		
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
				if (presledek > new_start + 59):
					print(escapeColorDefault+self.description[new_start:last_presledek])
					new_start = last_presledek +1	
				else:
					if (presledek > 0):
					    last_presledek=presledek		
			sys.stdout.write(escapeColorDefault+self.description[new_start:]+''+escapeColorDefault+'\n'
							+'###########################################################\n')
		key = raw_input(thisAppOutput+'Nadaljuj z namestitvijo?'+confirmText)
		if key == 'y':
			self.install_apt_cmd()
			self.install_DEB_package()	
			self.install_TAR_package()
			self.make_destop_file()
			self.add_PATH_parameter()
			self.run_bash_cmds()
			self.add_BASH_parameter()
			self.version_check()
			self.show_notes()		
			sys.stdout.write(thisAppOutput+'Pritisni [ENTER] za nadaljevanje...'+escapeColorDefault+'\n')

## DEFINICIJA PROGRAMOV ZA INSTALACIJO #########################
def Install_programms():
## HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP ######
	#global Primer_programa
	#Primer_programa = NovProgram()
	#Primer_programa.program_name = ''
	# 	PROGRAME_NAME - ime programa, priporoca se, da je brez presledkov,
	# 	ta besedlni niz se uporabi za prikaz imena programa v menu-ju in
	# 	tudi za ime datoteke *.desktop (/usr/share/applications/ime_programa.desktop).
	#	primer uporabe:
	#	novProgram.program_name='firefox'					
	#Primer_programa.description = ''
	# 	DESCRIPTON - string se uporablja za nekaj uvodnega besedila v menuju.
	#	primer uporabe:
	#	novProgram.description=	'Ta program se uporablja za pisanje besedil.\n Uporabljamo'\
	#				'pa ga lahko tudi ta urejanje nastavitev...' 
	#Primer_programa.pre_install_cmds = []					
	#	PRE_INSTALL_CMDS - niz stringov se izvrsi kakor ce bi jih vpisovali v terminal
	#	eden za drugim. Izvrsijo se pred vsemi ostalimi ukazi (apt-get install, deb, tar).
	#	Med vsakim navedenim nizom nas program tudi vprasa ali zelimo izvrsiti ukaz [y/n].
	#	primer uporabe:
	#	novProgram.pre_install_cmds = [	'sudo apt-get update',
	#									'sudo apt-get upgrade']
	#Primer_programa.apt_get_name = ''
	#	APT_GET_NAME - to ime se uporabi v ukazu sudo apt-get install {apt_get_name}.
	#	Predno se izvede ta ukaz gremo pogledat, katera verzija je na razpolago z
	#	ukazom: sudo apt-cache policy. Tako se uporaabnik lahko odloci ali bo namestil
	#	program s tem ukazom ali ne.
	#	primer uporabe:
	#	novProgram.apt_get_name = 'nano'
	#Primer_programa.deb_package_path = ''
	#	DEB_PACKAGE_PATH - pot datoteke na kateri se nahaja *deb paket. Ta se uporablja
	#	v primeru, ko vrsta arhitekture ni pomembna ali pa paket ne podpira razlicnih
	#	arhitektur.
	#	primer uporabe:
	#	novProgram.deb_package_path = 'https://download.sublimetext.com/'
	#Primer_programa.deb_package_file = ''
	#	DEB_PACKAGE_FILE - ime datoteke, ki se nahaja na prej omenjeni poti {deb_package_path}.
	#	Ta string v tej spremenljivki se uporablja tudi za instalacijo deb paketa:
	#	sudo dpkg -i {deb_package_file}. Presnete datoteke se na koncu postopka tudi izbrisejo.
	#	primer uporabe:
	#	novProgram.deb_package_file = 'sublime-text_build-all.deb'
	#Primer_programa.deb_package_path_32 = ''
	#	DEB_PACKAGE_PATH_32 - enako kot pri {deb_package_path}, le da se *.deb paket namesti le
	#	ce imate 32-bitni sistem. 
	#Primer_programa.deb_package_file_32 = ''
	#	DEB_PACKAGE_FILE_32 - enako kot pri {deb_package_path}, le da se *.deb paket namesti le
	#	ce imate 32-bitni sistem. 
	#Primer_programa.deb_package_path_64 = ''
	#	DEB_PACKAGE_PATH_64 - enako kot pri {deb_package_path}, le da se *.deb paket namesti le
	#	ce imate 64-bitni sistem. 
	#Primer_programa.deb_package_file_64 = ''
	#	DEB_PACKAGE_FILE_64 - enako kot pri {deb_package_path}, le da se *.deb paket namesti le
	#	ce imate 64-bitni sistem. 
	#Primer_programa.tar_package_path = ''
	#	TAR_PACKAGE_PATH - pot datoteke na kateri se nahaja *.tar.gz ali *.tar.xz paket. Ta se
	#	uporablja v primeru, ko vrsta arhitekture ni pomembna ali pa paket ne podpira razlicnih
	#	arhitektur.
	#	primer uporabe:
	#	novProgram.tar_package_path = 'https://qcad.org/archives/qcad/'
	#Primer_programa.tar_package_file = ''
	#	TAR_PACKAGE_FILE - ime datoteke, ki se nahaja na prej omenjeni poti {tar_package_path}.
	#	Ta string v tej spremenljivki se uporablja tudi za razpakiranje *.tar paketa:
	#	tar -xvf '+ download_dir+{tar_package_file}. Datoteke se razpakirajo v ~/Download/, ali
	#	pa pot lahko tudi posebej dolocite v spremenljivki {tar_destination}. Presnete datoteke
	#	se na koncu postopka tudi izbrisejo.
	#	primer uporabe:
	#	novProgram.tar_package_file = 'sublime-text_build-all.tar.gz'
	#Primer_programa.tar_package_path_32 = ''
	#	TAR_PACKAGE_PATH_32 - enako kot pri {tar_package_path}, le da se *.tar.* paket namesti le
	#	ce imate 32-bitni sistem. 
	#Primer_programa.tar_package_file_32 = ''
	#	TAR_PACKAGE_FILE_32 - enako kot pri {tar_package_file}, le da se *.tar.* paket namesti le
	#	ce imate 32-bitni sistem. 
	#Primer_programa.tar_package_path_64 = ''
	#	TAR_PACKAGE_PATH_64 - enako kot pri {tar_package_path}, le da se *.tar.* paket namesti le
	#	ce imate 64-bitni sistem. 
	#Primer_programa.tar_package_file_64 = ''
	#	DEB_PACKAGE_FILE_64 - enako kot pri {deb_package_path}, le da se *.deb paket namesti le
	#	ce imate 64-bitni sistem. 
	#Primer_programa.tar_destination = ''
	#	TAR_DESTINATION - direktorij, kamor zelite, da se *.tar.* paket od-tara. Ce direktorij se
	#	ne obstaja, da bo instalacija sama ustvarila...
	#	primer uporabe:
	#	novProgram.tar_destiation = '/opt/'
	#Primer_programa.tar_extra_cmds = []
	#	TAR_EXTRA_CMDS - Po koncanem razpakiranju TAR datoteke lahko naredite se kake cmd, kot
	# 	bi jih pisali v terminalu: naprimer kake instalacije ali kaj podobnega...
	#	primer uporabe:
	#	novProgram.tar_extra_cmds =['sudo rm /usr/bin/nmon',
	#								'sudo chmod 777 '+opt_dir+'nmon/'+'nmon_x86_debian8',
	#								'sudo ln -s '+opt_dir+'nmon/'+'nmon_x86_debian8 /usr/bin/nmon']
	#Primer_programa.program_desktop = []
	#	PROGRAM_DESKTOP - niz stringov, ki se bo vpisal v {program_name}.desktop file.
	#	primer uporabe:
	#	Arduino.program_desktop = [	'[Desktop Entry]',
	#								'Version=1.0',
	#								'Name=Arduino IDE',
	#								'Exec=/opt/arduino-nightly/arduino',
	#								'Icon=/opt/arduino-nightly/lib/icons/64x64/apps/arduino.png',
	#								'Terminal=false',
	#								'Type=Application',
	#								'Categories=Development;Programming;'
	#								]
	#Primer_programa.add_path_profile_variable  = ''
	#	ADD_PATH_PROFILE_VARIABLE - string, ki ga je potrebno vpisati v $PATH spremenljivko.
	#	primer uporabe:
	#	Arduino.add_path_profile_variable  = '/opt/arduino-nightly/
	#Primer_programa.extra_cmd = []
	#	EXTRA_CMD - niz ukazov, ki bi jih morali vtipkati v terminal po instalacijskem postopku.
	#	Na tem mestu lahko dodate link v /usr/bin/ tako, da lahko zazenete program od koderkoli,
	#	kakor smo to naredili za program thunderbird...
	#	primer uporabe:
	#	Thunderbird.extra_cmd = ['sudo ln -s /opt/thunderbird/thunderbird /usr/bin/thunderbird'] 
	#Primer_programa.add_bash_parameter = []
	#	ADD_BASH_PARAMETER - niz stringov (besedila), ki ga je potrebno dodati v datoteko:
	#	~/.bashrc. Besedilo se doda na konec dokumenta. Skript vas vprasa za vsak niz posebej,
	#	ce naj ga doda.
	#	primer uporabe:
	#	Keymap.add_bash_parameter = [	'\n#remap tipko [dz] - "/"',
	#									'\nxmodmap -e "keycode 35 = slash"']
	#Primer_programa.check_version_cmd = ''
	#	CHECK_VERSION_CMD - string se izvrsi kot cmd ukaz v ternimalu in je namenjen
	#	preverjanju verzije. Ta ukaz se izvede po instalaciji.
	#	primer uporabe:
	#	novProgram = 'nano --version' 
	#Primer_programa.notes = ''
	#	NOTES - ko se instalacijski postopek zakljuci se izpise neko besedilo, ki sporoci
	#	uporabniku kaka nadaljna navodila. Naprimer, ce program potrebuje kake dodatne
	#	nastavitve, kot v primeru terminatorja za prikaz podatkov o racunalniku z neofetch.
	#VsiProgrami.append(Primer_programa.program_name)
## Primer_programa #############################################
	#global Primer_programa
	#Primer_programa = NovProgram()
	#Primer_programa.program_name = ''
	#Primer_programa.description = ''
	#Primer_programa.pre_install_cmds = []					
	#Primer_programa.apt_get_name = ''
	#Primer_programa.deb_package_path = ''
	#Primer_programa.deb_package_file = ''
	#Primer_programa.deb_package_path_32 = ''
	#Primer_programa.deb_package_file_32 = ''
	#Primer_programa.deb_package_path_64 = ''
	#Primer_programa.deb_package_file_64 = ''
	#Primer_programa.tar_package_path = ''
	#Primer_programa.tar_package_file = ''
	#Primer_programa.tar_package_path_32 = ''
	#Primer_programa.tar_package_file_32 = ''
	#Primer_programa.tar_package_path_64 = ''
	#Primer_programa.tar_package_file_64 = ''
	#Primer_programa.tar_destination = ''
	#Primer_programa.tar_extra_cmds = []
	#Primer_programa.program_desktop = []
	#Primer_programa.add_path_profile_variable  = ''
	#Primer_programa.extra_cmd = []
	#Primer_programa.add_bash_parameter = []
	#Primer_programa.check_version_cmd = ''
	#Primer_programa.notes = ''
	#VsiProgrami.append(Primer_programa.program_name)
#------------------------------------------------SYSTEM PROGRAMS
## UPDATE & UPGRADE ###########################################1
	global Update_Upgrade
	Update_Upgrade = NovProgram()
	Update_Upgrade.program_name = 'Update & Upgrade'
	Update_Upgrade.description = 'Posodobite sistemske knjiznice...'
	Update_Upgrade.pre_install_cmds = [	'sudo apt-get update',
										'sudo apt-get upgrade']
	VsiProgrami.append(Update_Upgrade.program_name)
## GIT ########################################################2
	global git
	git = NovProgram()
	git.program_name = 'git'					#ime naj bo brez presledkov
	git.description = 'Protokol za skrbno spremljanje verzij'\
					'razvojnih programov.'					#neko besedilo za opis
	git.apt_get_name = 'git-core'					#ime za apt-get
	git.notes = ''
	git.extra_cmd = ['git clone https://github.com/davidrihtarsic/InstallMyApps.git ~/Files/GitHub_noSync/InstallMyApps',
					 'git clone https://github.com/davidrihtarsic/myLinuxNotes.git ~/Files/GitHub_noSync/myLinuxNotes',
					 'git clone https://github.com/davidrihtarsic/Korad3005p.git ~/Files/GitHub_noSync/Korad3005p',
					 'git clone https://github.com/davidrihtarsic/BunsenLab.git ~/Files/GitHub_noSync/BunsenLab',
					 'git clone https://github.com/davidrihtarsic/RobDuino.git ~/Files/GitHub_noSync/RobDuino',
					 'git clone https://github.com/davidrihtarsic/ArduinoCNC-DCmotors.git ~/Files/GitHub_noSync/ArduinoCNC-DCmotors'
					 ]
	VsiProgrami.append(git.program_name)
## Java 8 #####################################################3
	global java_8
	java_8 = NovProgram()
	java_8.program_name = 'java8'					#ime naj bo brez presledkov
	java_8.description = 'Namesti novejso verzijo java 8'					#neko besedilo za opis
	java_8.check_version_cmd = 'java -version'			#cmd za preverjanje verzije
	java_8.tar_package_path_64 = 'http://javadl.oracle.com/webapps/download/'				#url (brez fila)
	java_8.tar_package_file_64 = 'AutoDL?BundleId=218823_e9e7ea248e2c4826b92b3f075a80e441'			#file za 64bit
	java_8.tar_destination = '/usr/lib/jvm/'				#kam naj od tara.. TAR paket
	java_8.extra_cmd = ['sudo update-alternatives --install /usr/bin/java java /usr/lib/jvm/jre1.8.0_121/bin/java 1',
						'sudo update-alternatives --config java']					#se ene extra cmd ... ce je se kaj...
	VsiProgrami.append(java_8.program_name)
## OpenBox menu ###############################################4
	global obmenu
	obmenu = NovProgram()
	obmenu.program_name = 'openbox-menu'					#ime naj bo brez presledkov
	obmenu.description = 'Naredi nov menu v OpenBox UI'		#neko besedilo za opis
	obmenu.extra_cmd = ['mv ~/.config/openbox/menu.xml ~/.config/openbox/menu_original.xml',\
						'wget "https://github.com/davidrihtarsic/BunsenLab/raw/master/OpenBox_menu.xml" -O ~/.config/openbox/menu.xml',\
						'sudo git clone https://github.com/woho/openbox-menu.git '+opt_dir+'openbox-menu',\
						'/opt/openbox-menu/obmenu.py']#se ene extra cmd ... ce je se kaj...
	obmenu.program_desktop = ['[Desktop Entry]',
							'Version=1.0',
							'Name=openbox-menu',
							'Exec=terminator -e /opt/openbox-menu/obmenu.py',
							'Icon=openbox.png',
							'Terminal=true',
							'Type=Application',
							'Categories=Settings;'
							] 
	# obmenu.notes = ''
	VsiProgrami.append(obmenu.program_name)
## Terminator #################################################5
	global Terminator
	Terminator = NovProgram()
	Terminator.program_name = 'Terminator'
	Terminator.description = 'Lep, eleganten terminal...'
	Terminator.apt_get_name ='terminator'
	Terminator.check_version_cmd = ''
	Terminator.deb_package_path = ''
	Terminator.deb_package_file = ''
	VsiProgrami.append(Terminator.program_name)
## Htop #######################################################6
	global Htop
	Htop = NovProgram()
	Htop.program_name = 'Htop'
	Htop.description = 'Spremljanje procesov...'
	Htop.apt_get_name ='htop'
	Htop.check_version_cmd = ''
	Htop.deb_package_path = ''
	Htop.deb_package_file = ''
	VsiProgrami.append(Htop.program_name)
## NMON #######################################################7
	global nmon
	nmon = NovProgram()
	nmon.program_name = 'nmon'
	nmon.description = 'Spremljanje procesov... za DEBIAN!'
	nmon.apt_get_name =''
	nmon.tar_package_file = 'nmon16d_x86.tar.gz'
	nmon.tar_package_path = 'http://sourceforge.net/projects/nmon/files/'
	nmon.tar_destination =  opt_dir+'nmon/'
	nmon.tar_extra_cmds =['sudo rm -v /usr/bin/nmon',
						'sudo chmod 777 '+opt_dir+'nmon/'+'nmon_x86_64_debian8',
						'sudo ln -s '+opt_dir+'nmon/'+'nmon_x86_64_debian8 /usr/bin/nmon']
	nmon.program_desktop = ['[Desktop Entry]',
							'Version=1.0',
							'Name=nmon',
							'Exec=terminator -e nmon',
							'Icon=nmon',
							'Terminal=true',
							'Type=Application',
							'Categories=System;Development;Programming;'
							]
	#nmon.tar_extra_cmds = ['sudo mv ' + download_dir + 'nmon/nmon_x86_64_ubuntu15 /usr/bin/nmon',
	#					'sudo rm -R ' + download_dir+'nmon/',
	#					'sudo chmod 777 /usr/bin/nmod']
	#nmon.tar_extra_cmds = ['sudo chmod 777 '+ download_dir + 'nmon/nmon_x86_debian8',
	#					'sudo mv ' + download_dir + 'nmon/nmon_x86_debian8 /usr/bin/nmon',
	#					'sudo rm -R ' + download_dir+'nmon/']
	VsiProgrami.append(nmon.program_name)
## WAVEMON ####################################################8
	global wavemon
	wavemon = NovProgram()
	wavemon.program_name = 'wavemon'					#ime naj bo brez presledkov
	wavemon.description = 'Program za monitoring wireless omrezj'					#neko besedilo za opis
	wavemon.apt_get_name = 'wavemon'					#ime za apt-get
	wavemon.program_desktop = ['[Desktop Entry]',
							'Version=1.0',
							'Name=WaveMon',
							'Exec=terminator -e sudo wavemon',
							'Icon=wifi',
							'Terminal=true',
							'Type=Application',
							'Categories=Network;'
							]
	VsiProgrami.append(wavemon.program_name)
## Neofetch ###################################################9
	global Neofetch
	Neofetch = NovProgram()
	Neofetch.program_name = 'Neofetch'
	Neofetch.description = 'Logo in nekaj podatkov o racunaniku...!'
	Neofetch.apt_get_add_ppa ='add-apt-repository ppa:dawidd0811/neofetch'
	Neofetch.apt_get_name ='neofetch'
	Neofetch.check_version_cmd = 'neofetch'
	Neofetch.notes = 'Notes... to do...'
	VsiProgrami.append(Neofetch.program_name)
## Fortune ###################################################10
	global Fortune
	Fortune = NovProgram()
	Fortune.program_name = 'Fortune'
	Fortune.description = 'Znani reki in pregovori...'
	Fortune.apt_get_name ='fortune-mod'
	Fortune.check_version_cmd = 'fortune -v'
	Fortune.deb_package_path = ''
	Fortune.deb_package_file = ''
	VsiProgrami.append(Fortune.program_name)
## COWSAY ####################################################11
	global Cowsay
	Cowsay = NovProgram()
	Cowsay.program_name = 'Cowsay'
	Cowsay.description = 'Namesti pametno kravo...'
	Cowsay.apt_get_name ='cowsay'
	Cowsay.check_version_cmd = 'cowsay -help'
	Cowsay.deb_package_path = ''
	Cowsay.deb_package_file = ''
	Cowsay.add_bash_parameter = ["\nalias cls='clear;neofetch;fortune|cowsay'"]
	Cowsay.notes = 'V terminatorju nastavite:\nPreferences -> Profiles -> Command\ncustom command: [ neofetch;fortune|cowsay;bash ]'
	VsiProgrami.append(Cowsay.program_name)
## Keymap ####################################################12
	global Keymap
	Keymap = NovProgram()
	Keymap.description='remap tipke [dz] v "/"'
	Keymap.program_name = 'Keymap'
	Keymap.add_bash_parameter = ['\n#remap tipko [dz] - "/"','\nxmodmap -e "keycode 35 = slash"']			#text ki je za dodat v .bash 
	VsiProgrami.append(Keymap.program_name)
## conky #####################################################13
	global conky
	conky = NovProgram()
	conky.program_name = 'conky'					#ime naj bo brez presledkov
	conky.description = 'Prikaz nekaterih osnovnih podatkov sistema'					#neko besedilo za opis
	conky.apt_get_name = 'conky-all'					#ime za apt-get
	conky.extra_cmd = ['mkdir '+ user_path +'/.config/conky',
						'ls -alF '+ user_path +'/.config/conky']					#se ene extra cmd ... ce je se kaj...
	conky.program_desktop = []				#vsebina v program.desktop
	conky.add_path_profile_variable  = '' 
	conky.notes = ''
	VsiProgrami.append(conky.program_name)
## dave's conky ##############################################14
	global dave_s_conky
	dave_s_conky = NovProgram()
	dave_s_conky.program_name = 'dave_s_conky_v3_cfg'					#ime naj bo brez presledkov
	dave_s_conky.description = 'my conky config file'					#neko besedilo za opis
	dave_s_conky.extra_cmd = ['wget "https://github.com/davidrihtarsic/BunsenLab/raw/master/dave_s_conky.conkyrc" -O ~/.config/conky/dave_s_conky.conkyrc',\
							  'bl-conkyzen']					#se ene extra cmd ... ce je se kaj...
	dave_s_conky.program_desktop = []				#vsebina v program.desktop
	dave_s_conky.add_path_profile_variable  = ''
	#dave_s_conky.add_bash_parameter = 	['\n# zazeni conky ob zagomu racunalnika...',
	#									'\nconky --config='+ user_path +'/.config/conky/dave_s_conky.conkyrc']
	#add to .bashrc file =>'conky -config='+ user_path +'/.config/conky/dave_s_conky.conkyrc' 
	dave_s_conky.notes = ''
	VsiProgrami.append(dave_s_conky.program_name)
## alias ll -> ls -alF #######################################15
	global ll
	ll = NovProgram()
	ll.program_name = 'alias ll'					#ime naj bo brez presledkov
	ll.description = 'priredi ll namesto uporabe ls -alF - ukaz se uporablja za bolj detajlni prikaz vsebine v direktoriju'
						#neko besedilo za opis
	ll.add_bash_parameter = ['\n#alias',"\nalias ll='ls -alF'"]			#text ki je za dodat v .bash 
	ll.notes = ''
	VsiProgrami.append(ll.program_name)
## alias WEATHER #############################################16
	global weather
	weather = NovProgram()
	weather.program_name = 'alias weather'					#ime naj bo brez presledkov
	weather.description = 'izpis vremena za tri dni v terminalnem oknu'
					#neko besedilo za opis
	weather.add_bash_parameter = ["\nalias weather='curl wttr.in/~begunje'"]			#text ki je za dodat v .bash 
	weather.notes = ''
	VsiProgrami.append(weather.program_name)
## FileZilla #################################################17
	# NOT testet yet ... - was preinstalled on BL
	global FileZilla
	FileZilla = NovProgram()
	FileZilla.program_name = 'FileZilla'
	FileZilla.description = 'FileZilla is open source software distributed free of charge under the terms of the GNU General Public License'					
	FileZilla.apt_get_name = 'FileZilla'
	##FileZilla.notes = ''
 	VsiProgrami.append(FileZilla.program_name)
## python-serial #############################################18
	#test OK @ BL 64bit (David)
	global python_serial
	python_serial = NovProgram()
	python_serial.program_name = 'python-serial'
	python_serial.description = 'This module encapsulates the access for the serial port. It provides backends for Python running on Windows, OSX, Linux, BSD (possibly any POSIX compliant system) and IronPython. The module named "serial" automatically selects the appropriate backend.'
	python_serial.apt_get_name = 'python-serial'
	##python-serial.notes = ''
 	VsiProgrami.append(python_serial.program_name)
## FreeFileSync ##############################################19
    #Test INFO @ BL64bit (David desktop comp):
    #	- paket deb najden OK
    #	- download OK
    #	- untar OK
    #	- desktopfile ERROR -> FIX: Categories=(~~Accessories~~)Utility;
    #	- desktopfile ICON added
    #ne dela dobro na 32bit BL: Ni v kategoriji Acesories, pri zapisanju javi da nima dovoljenja, 
    #Test INFO @ LB32bit (David Laptop)
    #	- instalacija OK
    #	- noce shranit nastavitev...
    #	- "permission denided"
    #	- programa nisem usposobil... zato verjetno ne dobim error-ja vsakic ko odprem in zaprem program
    #	- nabrs je resitev v dovoljenu mape.. "sudo chmod g+w /opt/FreeFileSync/"
	global FreeFileSync
	FreeFileSync = NovProgram()
	FreeFileSync.program_name = 'FreeFileSync'
	FreeFileSync.description = 'FreeFileSync is a free Open Source software that helps you synchronize files and synchronize folders for Windows, Linux and macOS. It is designed to save your time setting up and running backup jobs while having nice visual feedback along the way.'
	FreeFileSync.pre_install_cmds = []					
	FreeFileSync.apt_get_name = ''
	FreeFileSync.deb_package_path = ''
	FreeFileSync.deb_package_file = ''
	FreeFileSync.deb_package_path_32 = ''
	FreeFileSync.deb_package_file_32 = ''
	FreeFileSync.deb_package_path_64 = ''
	FreeFileSync.deb_package_file_64 = ''
	FreeFileSync.tar_package_path = ''
	FreeFileSync.tar_package_file = ''
	FreeFileSync.tar_package_path_32 = 'http://download846.mediafireuserdownload.com/t6dkqzhd6ghg/qhpiwpcuhaul3ex/'
	FreeFileSync.tar_package_file_32 = 'FreeFileSync_9.0_Debian_8.7_64-bit.tar.gz'
	FreeFileSync.tar_package_path_64 = 'http://download1523.mediafireuserdownload.com/h8fro3oopifg/a96gf3almx3t2ac/'
	FreeFileSync.tar_package_file_64 = 'FreeFileSync_9.1_Debian_8.8_64-bit.tar.gz'
	FreeFileSync.tar_destination = opt_dir
	FreeFileSync.tar_extra_cmds = [	]
	FreeFileSync.program_desktop = ['[Desktop Entry]',
								'Name=FreeFileSync',
								'Exec=/opt/FreeFileSync/FreeFileSync',
								'Icon=/opt/FreeFileSync/Help/images/basic-step-sync-config.png',
								'Terminal=false',
								'Type=Application',
								'Categories=Utility;'
									]
	FreeFileSync.add_path_profile_variable  = ''
	#FreeFileSync.extra_cmd = [	'sudo touch /opt/FreeFileSync/GlobalSettings.xml',
	#							'sudo chmod ugo+rwx /opt/FreeFileSync/GlobalSettings.xml']
	FreeFileSync.extra_cmd = [	'sudo chown '+ user +' /opt/FreeFileSync/']	
	FreeFileSync.add_bash_parameter = []
	FreeFileSync.check_version_cmd = ''
	FreeFileSync.notes = ''
	VsiProgrami.append(FreeFileSync.program_name)
#-------------------------------------------------OTHER PROGRAMS
## ARDUINO #####################################################
	global Arduino
	Arduino = NovProgram()
	Arduino.program_name = 'ArduinoIDE'
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
	#Arduino.apt_get_name =''
	Arduino.check_version_cmd = 'head -1 /opt/arduino*/revisions.txt'
	Arduino.tar_package_path_64 = 'https://downloads.arduino.cc/'
	Arduino.tar_package_file_64 = 'arduino-nightly-linux64.tar.xz'
	Arduino.tar_package_path_32 = 'https://downloads.arduino.cc/'
	Arduino.tar_package_file_32 = 'arduino-nightly-linux32.tar.xz'
	#Arduino.tar_package_file_32 = 'arduino-1.8.1-linux32.tar.xz'
	Arduino.tar_destination = opt_dir #default = home/$USER/Downloads/
	Arduino.program_desktop = ['[Desktop Entry]',
							'Version=1.0',
							'Name=Arduino IDE',
							'Exec=/opt/arduino-nightly/arduino',
							'Icon=/opt/arduino-nightly/lib/icons/64x64/apps/arduino.png',
							'Terminal=false',
							'Type=Application',
							'Categories=Development;Programming;'
							]
	#Arduino.tar_extra_cmds = ['sudo ' + Arduino.tar_destination + 'arduino-1.8.1/install.sh']
	Arduino.add_path_profile_variable  = Arduino.tar_destination + 'arduino-nightly/'
	Arduino.extra_cmd = ['sudo usermod -a -G dialout '+ user]
	Arduino.notes = 'NASTAVITI JE POTREBNO "SERIAL PORT PERMITIONS"!\n'\
					'poglej na: http://playground.arduino.cc/Linux/All#Permission\n'\
					'1. -> ls -l /dev/ttyUSB* ali ls -l /dev/ttyACM*\n'\
					'	dobimo:\n'\
					'	crw-rw---- 1 root dialout 188, 0  5 apr 23.01 ttyACM0\n'\
					'	kjer je "dailout" - group name\n'\
					'2. -> sudo usermod -a -G group-name username\n'\
					'3. log-OUT & log-IN'
	VsiProgrami.append(Arduino.program_name)
## QCAD ########################################################
	global qCAD
	qCAD = NovProgram()
	qCAD.program_name = 'qcad'
	qCAD.description = 'Qcad je racunalnisko podprto orodje za 2D nacrtovanje in '\
						'risanje. Zacetki razvoja segajo v leto 1999, ko je programsko '\
						'orodje nastalo kot rezultat spinoff projekta izdelave CAD '\
						'sistema. Z njim izdelamo tehnicne risbe (nacrti zgradb, '\
						'njihovih notranjosti, mehanski deli, sheme, diagrami ipd.). '\
						'Uporaben je na razlicnih tehniskih podrocjih: strojnistvo, '\
						'lesarstvo, gradbenistvo, arhitektura, geodezija in elektrotehnika.'

	qCAD.tar_package_path_64 = 'https://qcad.org/archives/qcad/'
	qCAD.tar_package_file_64 = 'qcad-3.16.5-trial-linux-x86_64.tar.gz'
	qCAD.tar_package_path_32 = 'https://qcad.org/archives/qcad/'
	qCAD.tar_package_file_32 = 'qcad-3.16.5-trial-linux-x86_32.tar.gz'
	qCAD.tar_destination = opt_dir
	qCAD.program_desktop = ['[Desktop Entry]',
							'Version=1.0',
							'Name=QCAD',
							'Exec=/opt/qcad-3.16.5-trial-linux-x86_'+str(qCAD.arhitecture_bit_num)+'/qcad',
							'Icon=/opt/qcad-3.16.5-trial-linux-x86_'+str(qCAD.arhitecture_bit_num)+'/qcad_icon.png',
							'Terminal=false',
							'Type=Application',
							'Categories=Graphics;'
							]
	qCAD.add_path_profile_variable = '/opt/qcad-3.16.5-trial-linux-x86_'+str(qCAD.arhitecture_bit_num)+'/'
	VsiProgrami.append(qCAD.program_name)
## FREECAD #####################################################
	global FreeCAD
	FreeCAD = NovProgram()
	FreeCAD.program_name = 'FreeCAD'
	FreeCAD.description = 'Orodje za tehnisko risanje.'
	FreeCAD.apt_get_name ='freecad'
	VsiProgrami.append(FreeCAD.program_name)
## SUBLIME #####################################################
	global Sublime
	Sublime = NovProgram()
	Sublime.program_name = 'Sublime'
	Sublime.description = 'Sublime Text is a sophisticated text editor '\
						'for code, markup and prose. You\'ll love the '\
						'slick user interface, extraordinary features and '\
						'amazing performance.'
	Sublime.pre_install_cmds = [	'wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -',
									'echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list',
									'sudo apt-get update'
								]
	Sublime.apt_get_name ='sublime-text'
	Sublime.check_version_cmd = 'subl --version'
	#Sublime.deb_package_path_64 = 'https://download.sublimetext.com/'
	#Sublime.deb_package_file_64 = 'sublime-text_build-3126_amd64.deb'
	#Sublime.deb_package_path_32 = 'https://download.sublimetext.com/'
	#Sublime.deb_package_file_32 = 'sublime-text_build-3126_i386.deb'
	#Sublime.extra_cmd = [	'sudo update-alternatives --install /usr/bin/bl-text-editor bl-text-editor /usr/bin/subl 50',
	#						'sudo update-alternatives --set bl-text-editor /usr/bin/subl',
	#						'update-alternatives --display bl-text-editor'
	#									]
	VsiProgrami.append(Sublime.program_name)
## LibreOffice #################################################
	global LibreOffice
	LibreOffice = NovProgram()
	LibreOffice.program_name = 'LibreOffice'
	LibreOffice.description = 'Office suit for linux and other OS...'
	LibreOffice.apt_get_name =''
	LibreOffice.check_version_cmd = ''
	LibreOffice.tar_package_path_32 = 'http://mirrors.uniri.hr/tdf/libreoffice/stable/5.3.2/deb/x86/'
	LibreOffice.tar_package_file_32 = 'LibreOffice_5.3.2_Linux_x86_deb.tar.gz'
	LibreOffice.deb_package_path_64 = ''
	LibreOffice.deb_package_file_64 = ''
	LibreOffice.tar_package_path_64 = 'http://ftp.igh.cnrs.fr/pub/tdf/libreoffice/stable/5.4.0/deb/x86_64/'
	LibreOffice.tar_package_file_64 = 'LibreOffice_5.4.0_Linux_x86-64_deb.tar.gz'
	LibreOffice.tar_destination =''
	LibreOffice.tar_extra_cmds = ['sudo dpkg -i '+ download_dir +'LibreOffice_*_Linux_*_deb/DEBS/*.deb']
	VsiProgrami.append(LibreOffice.program_name)
## Thunderbird #################################################
	global Thunderbird
	Thunderbird = NovProgram()
	Thunderbird.program_name = 'Thunderbird'
	Thunderbird.description = 'Postni odjemalec...'
	Thunderbird.apt_get_name ='thunderbird'
	Thunderbird.tar_package_path_32 = 'https://download-installer.cdn.mozilla.net/pub/thunderbird/releases/52.0/linux-i686/sl/'
	Thunderbird.tar_package_file_32 = 'thunderbird-52.0.tar.bz2'
	Thunderbird.tar_package_path_64 = 'https://download-installer.cdn.mozilla.net/pub/thunderbird/releases/45.8.0/linux-x86_64/en-US/'
	Thunderbird.tar_package_file_64 = 'thunderbird-45.8.0.tar.bz2'
	Thunderbird.tar_destination = '/opt/'
	Thunderbird.program_desktop = ['[Desktop Entry]',
							'Version=1.0',
							'Name=Thunderbird',
							'Exec=/opt/thunderbird/thunderbird',
							'Icon=/usr/share/icons/Faenza/apps/32/thunderbird.png',
							'Terminal=false',
							'Type=Application',
							'Categories=Network;'
							]
	Thunderbird.extra_cmd = ['sudo ln -s /opt/thunderbird/thunderbird /usr/bin/thunderbird']
	Thunderbird.check_version_cmd = 'thunderbird -v'
	VsiProgrami.append(Thunderbird.program_name)
## GoogleChrome ################################################
	global GoogleChrome
	GoogleChrome = NovProgram()
	GoogleChrome.program_name = 'Google Chrome'
	GoogleChrome.description = 'spletni brsklalnik'
	GoogleChrome.apt_get_name =''
	GoogleChrome.check_version_cmd = ''
	GoogleChrome.deb_package_path_64 = 'https://dl.google.com/linux/direct/'
	GoogleChrome.deb_package_file_64 = 'google-chrome-stable_current_amd64.deb'
	GoogleChrome.deb_package_path_32 = 'https://archive.org/download/google-chrome-stable_48.0.2564.116-1_i386/'
	GoogleChrome.deb_package_file_32 = 'google-chrome-stable_48.0.2564.116-1_i386.deb'
	VsiProgrami.append(GoogleChrome.program_name)
## W3M #########################################################
	global W3M
	W3M = NovProgram()
	W3M.program_name = 'w3m'					#ime naj bo brez presledkov
	W3M.description = 'Terminalni spletni brskalnik'		#neko besedilo za opis
	W3M.apt_get_name = 'w3m'					#ime za apt-get
	W3M.check_version_cmd = 'w3m -v'			#cmd za preverjanje verzije
	W3M.program_desktop = ['[Desktop Entry]',
							'Version=1.0',
							'Name=w3m',
							'Exec=terminator -e w3m www.duckduckgo.com',
							'Icon=w3m',
							'Terminal=true',
							'Type=Application',
							'Categories=Network;'
							]				#vsebina v program.desktop
	W3M.add_bash_parameter = ["\n #alias w3mm da odpre duckduckgo.com","\n alias w3mm='w3m www.google.com'"]
	VsiProgrami.append(W3M.program_name)
## Skype #######################################################
	global Skype
	Skype = NovProgram()
	Skype.program_name = 'Skype'
	Skype.description = 'Komunikacija preko interneta...'
	Skype.apt_get_name =''
	Skype.check_version_cmd = ''
	Skype.deb_package_path_64 = 'https://repo.skype.com/latest/'
	Skype.deb_package_file_64 = 'skypeforlinux-64.deb'
	Skype.deb_package_path_32 = 'https://repo.skype.com/latest/'
	Skype.deb_package_file_32 = 'skypeforlinux-32.deb'
	VsiProgrami.append(Skype.program_name)
## OpenBoxMENU generatoe  ######################################
	# global obmenugen
	# obmenugen = NovProgram()
	# obmenugen.program_name = 'obmenugen'		#ime naj bo brez presledkov
	# obmenugen.description = 'Namenjeno avtomatskemu generiranju menuja v okolju OpenBox,\n'\
	# 						'katerega uporablja tudi BunsenLab. Program zgenerira menu\n'\
	# 						'iz vsebine datotek, ki jih najde v /usr/share/applications/*'
	# obmenugen.tar_package_path = 'https://netcologne.dl.sourceforge.net/project/obmenugen/obmenugen/obmenugen-0.2beta/'				#url (brez fila)
	# obmenugen.tar_package_file = 'obmenugen-0.2beta.tar.bz2'				#file za katerikoli sistem
	# obmenugen.tar_extra_cmds = ['sudo cp '+download_dir+'obmenugen/bin/obmenugen /usr/bin/',
	# 							'obmenugen -p',
	# 							'openbox --reconfigure',
	# 							'rm -R '+download_dir+'obmenugen']				#extra commande, ce je se kaj za narest...
	# obmenugen.notes = 'Najverjetneje boste morali sami urediti tudi nekaj podatkov v:\n'\
	# 					'~/.config/obmenugen/obmenugen.cfg\n'\
	# 					'Kot naprimer kateri terminalni simulator uporabljate in\n'\
	# 					'vas priljubljen urejevalnik besedil...'
	#VsiProgrami.append(obmenugen.program_name)
## SmartGIT ####################################################
	# global smartGit
	# smartGit = NovProgram()
	# smartGit.program_name = 'smartgit'					#ime naj bo brez presledkov
	# smartGit.description = 'Git GUI client'					#neko besedilo za opis
	# smartGit.tar_package_path = 'https://www.syntevo.com/static/smart/download/smartgit/'				#url (brez fila)
	# smartGit.tar_package_file = 'smartgit-linux-17_0_3.tar.gz'				#file za katerikoli sistem
	# smartGit.tar_destination = opt_dir				#kam naj od tara.. TAR paket
	# smartGit.extra_cmd = ['sudo ln -s /opt/smartgit/bin/smartgit.sh /usr/bin/smartgit']					#se ene extra cmd ... ce je se kaj...
	# smartGit.program_desktop = ['[Desktop Entry]',
	# 						'Version=1.0',
	# 						'Name=SmartGit',
	# 						'Exec=smartgit',
	# 						'Icon=/opt/smartgit/bin/smartgit-32.png',
	# 						'Terminal=false',
	# 						'Type=Application',
	# 						'Categories=Development;'
	# 						]
	# VsiProgrami.append(smartGit.program_name)
## Stellarium ##################################################
	global stellarium
	stellarium = NovProgram()
	stellarium.program_name = 'stellarium'
	stellarium.description = 'Zvezvde...'
	#stellarium.pre_install_cmds = []					
	stellarium.apt_get_name = 'stellarium'
	
	#stellarium.program_desktop = []
	#stellarium.extra_cmd = []
	#stellarium.add_bash_parameter = []
	#stellarium.check_version_cmd = ''
	#stellarium.notes = ''
	VsiProgrami.append(stellarium.program_name)
## Foxitreader #################################################
	global Foxitreader
	Foxitreader = NovProgram()
	Foxitreader.program_name = 'Foxitreader'
	Foxitreader.description = 'Program za urejanje PDF dokumentov'
	Foxitreader.pre_install_cmds = []					
	Foxitreader.apt_get_name = ''
	Foxitreader.deb_package_path = ''
	Foxitreader.deb_package_file = ''
	Foxitreader.deb_package_path_32 = ''
	Foxitreader.deb_package_file_32 = ''
	Foxitreader.deb_package_path_64 = ''
	Foxitreader.deb_package_file_64 = ''
	Foxitreader.tar_package_path = ''
	Foxitreader.tar_package_file = ''
	Foxitreader.tar_package_path_32 = 'http://cdn09.foxitsoftware.com/pub/foxit/reader/desktop/linux/2.x/2.3/en_us/'
	Foxitreader.tar_package_file_32 = 'FoxitReader2.3.0.2174_Server_x86_enu_Setup.run.tar.gz'
	Foxitreader.tar_package_path_64 = 'http://cdn09.foxitsoftware.com/pub/foxit/reader/desktop/linux/2.x/2.3/en_us/'
	Foxitreader.tar_package_file_64 = 'FoxitReader2.3.1.2182_Server_x64_enu_Setup.run.tar.gz'
	Foxitreader.tar_destination = ''
	Foxitreader.tar_extra_cmds = ["~/Downloads/FoxitReader*"]
	Foxitreader.program_desktop = []
	Foxitreader.add_path_profile_variable  = ''
	Foxitreader.extra_cmd = ['sudo ln -s ~/opt/foxitsoftware/foxitreader/FoxitReader.sh /usr/bin/foxitreader']
	Foxitreader.add_bash_parameter = []
	Foxitreader.check_version_cmd = ''
	Foxitreader.notes = ''
	VsiProgrami.append(Foxitreader.program_name)
## Fritzing ####################################################
    #32 bit BL tested
	global Fritzing
	Fritzing = NovProgram()
	Fritzing.program_name = 'Fritzing'
	Fritzing.description = 'Program za risanje vezij oziroma elektrotehniskih shem'
	Fritzing.pre_install_cmds = []					
	Fritzing.apt_get_name = ''
	Fritzing.deb_package_path = ''
	Fritzing.deb_package_file = ''
	Fritzing.deb_package_path_32 = ''
	Fritzing.deb_package_file_32 = ''
	Fritzing.deb_package_path_64 = ''
	Fritzing.deb_package_file_64 = ''
	Fritzing.tar_package_path = ''
	Fritzing.tar_package_file = ''
	Fritzing.tar_package_path_32 = 'http://fritzing.org/media/downloads/'
	Fritzing.tar_package_file_32 = 'fritzing-0.9.3b.linux.i386.tar.bz2'
	Fritzing.tar_package_path_64 = 'http://fritzing.org/download/0.9.3b/linux-64bit/'
	Fritzing.tar_package_file_64 = 'fritzing-0.9.3b.linux.AMD64.tar.bz2'
	Fritzing.tar_destination = opt_dir
	Fritzing.tar_extra_cmds = [	'sudo mv /opt/fritzing-0.9.3b* /opt/fritzing-0.9.3b',
								'sudo ln -s /opt/fritzing-0.9.3b/Fritzing /usr/bin/fritzing' 
								]
	Fritzing.program_desktop = ['[Desktop Entry]',
								'Name=Fritzing',
								'Exec=/opt/fritzing-0.9.3b/Fritzing',
								'Icon=/opt/fritzing-0.9.3b/icons/fritzing_icon.png',
								'Terminal=false',
								'Type=Application',
								'Categories=Science;Development;'
									]
	Fritzing.add_path_profile_variable  = ''
	Fritzing.extra_cmd = []
	Fritzing.add_bash_parameter = []
	Fritzing.check_version_cmd = ''
	Fritzing.notes = ''
	VsiProgrami.append(Fritzing.program_name)
## Texmaker ####################################################
	global texmaker
	texmaker = NovProgram()
	texmaker.program_name = 'texmaker'
	texmaker.description = 'Program za pisanje besedil v TeX formatu.'
	#texmaker.pre_install_cmds = ['sudo apt-get -f install texlive-full texmaker']					
	texmaker.apt_get_name = 'texlive-full texmaker'
	#texmaker.program_desktop = []
	#texmaker.extra_cmd = []
	#texmaker.add_bash_parameter = []
	#texmaker.check_version_cmd = ''
	#texmaker.notes = ''
	VsiProgrami.append(texmaker.program_name)
## INKSCAPE ####################################################
	global inkscape
	inkscape = NovProgram()
	inkscape.program_name = 'inkscape'
	inkscape.description = 'Program za risanje vektorske grafike.'
	inkscape.apt_get_name = 'inkscape'
	#inkscape.notes = ''
	VsiProgrami.append(inkscape.program_name)
## GIMP ########################################################
	global gimp
	gimp = NovProgram()
	gimp.program_name = 'gimp'
	gimp.description = 'Program za risanje, obdelavo slik, ...'
	gimp.apt_get_name = 'gimp'
	#gimp.notes = ''
	VsiProgrami.append(gimp.program_name)
## MyPaint #####################################################
	global mypaint
	mypaint = NovProgram()
	mypaint.program_name = 'mypaint'
	mypaint.description = 'Program za prostorocno risanje.'
	mypaint.apt_get_name = 'mypaint'
	#mypaint.notes = ''
	VsiProgrami.append(mypaint.program_name)
## Audacity ####################################################
	global audacity
	audacity = NovProgram()
	audacity.program_name = 'audacity'
	audacity.description = 'Audacity is free, open source, cross-platform audio software for multi-track recording and editing.'					
	audacity.apt_get_name = 'audacity'
	#audacity.notes = ''
	VsiProgrami.append(audacity.program_name)
## Evince PDF  #################################################
	global evince
	evince = NovProgram()
	evince.program_name = 'evince'
	evince.description = 'Evince is a document viewer for multiple document formats. The goal of evince is to replace the multiple document viewers that exist on the GNOME Desktop with a single simple application. Evince is specifically designed to support the file following formats: PDF, Postscript, djvu, tiff, dvi, XPS, SyncTex support with gedit, comics books (cbr,cbz,cb7 and cbt).'					
	evince.apt_get_name = 'evince'
	#evince.notes = ''
	VsiProgrami.append(evince.program_name)
## K3b  ########################################################
	#32 bit BL tested
	global k3b
	k3b = NovProgram()
	k3b.program_name = 'k3b'
	k3b.description = 'K3b is a simple, yet powerful and highly-configurable graphical optical disk burning application for audio, video, data projects and more!'					
	k3b.apt_get_name = 'k3b'
	##k3b.notes = ''
 	VsiProgrami.append(k3b.program_name)
## bCNC ########################################################
	#test OK @ BL 64-bit (David)
	global bCNC
	bCNC = NovProgram()
	bCNC.program_name = 'bCNC'
	bCNC.description = 'An advanced fully featured g-code sender for GRBL. bCNC is a cross platform program (Windows, Linux, Mac) written in python. The sender is robust and fast able to work nicely with old or slow hardware like Rasperry PI (As it was validated by the GRBL mainter on heavy testing).'
	bCNC.tar_extra_cmds = []
	bCNC.program_desktop = []
	bCNC.add_path_profile_variable  = '/opt/bCNC/'
	bCNC.extra_cmd = [	'wget --spider -v https://github.com/vlachoudis/bCNC/archive/master.zip',
						'wget "https://github.com/vlachoudis/bCNC/archive/master.zip" -O ~/Downloads/bCNC.zip',
					 	'unzip ~/Downloads/bCNC.zip -d ~/Downloads/',
					 	'rm -v ~/Downloads/bCNC.zip',
					 	'sudo mv ~/Downloads/bCNC-master /opt/bCNC',
					 	#'sudo ln -s /opt/bCNC/bCNC /usr/bin/bCNC',
					 	'sudo printf "\nCategories=Development;" >> /opt/bCNC/bCNC.desktop',
					 	'sudo printf "\nExec=/opt/bCNC/bCNC" >> /opt/bCNC/bCNC.desktop',
					 	'sudo printf "\nIcon=/opt/bCNC/bCNC.png" >> /opt/bCNC/bCNC.desktop',
					 	'sudo cp /opt/bCNC/bCNC.desktop /usr/share/applications/bCNC.desktop'
					 ]
	bCNC.add_bash_parameter = []
	bCNC.check_version_cmd = ''
	bCNC.notes = 'Najverjetneje se boste morali narediti log-out in nato log-in, da bodo nastavitve zacele veljati.'
	VsiProgrami.append(bCNC.program_name)
## lmms  #######################################################
	#32 bit BL tested
	global lmms
	lmms = NovProgram()
	lmms.program_name = 'lmms'
	lmms.description = 'Open source digital audio workstation'					
	lmms.apt_get_name = 'lmms'
	lmms.notes ="Dokumentacija za program se nahaja na naslovu: https://lmms.io/documentation/"
 	VsiProgrami.append(lmms.program_name)
## ECLIPSEC ####################################################
	#testing...  @ BL 64-bit (David)
	# instalacija dela...
	global eclipse
	eclipse = NovProgram()
	eclipse.program_name = 'eclipse'
	eclipse.description = 'Programsko okolje ...'
	eclipse.tar_package_path_32 = 'http://ftp-stud.fht-esslingen.de/pub/Mirrors/eclipse/oomph/epp/oxygen/R/'
	eclipse.tar_package_file_32 = 'eclipse-inst-linux32.tar.gz'
	eclipse.tar_package_path_64 = 'http://ftp-stud.fht-esslingen.de/pub/Mirrors/eclipse/oomph/epp/oxygen/R/'
	eclipse.tar_package_file_64 = 'eclipse-inst-linux64.tar.gz'
	eclipse.tar_extra_cmds = [	'sudo ~/Downloads/eclipse-installer/eclipse-inst',
								'sudo chown '+ user +' -R /opt/eclipse/']
	eclipse.program_desktop = []
	#eclipse.add_path_profile_variable  = '/opt/eclipse/'
	eclipse.program_desktop = ['[Desktop Entry]',
						'Version=1.0',
						'Name=eclipse IDE',
						'Exec=sudo /opt/eclipse/eclipse/eclipse',
						'Icon=/opt/eclipse/eclipse/icon.xpm',
						'Terminal=false',
						'Type=Application',
						'Categories=Development;Programming;'
						]
	eclipse.extra_cmd = []
	eclipse.add_bash_parameter = []
	eclipse.check_version_cmd = ''
	eclipse.notes = ''
	VsiProgrami.append(eclipse.program_name)
## GUVCview - program za snemanje z WEB camero #################
	# sudo apt-get install guvcview
## SIRIL - leplenje slik/video v fotografijo - za astronomijo ##
	# download https://free-astro.org/download/siril_0.9.6-2_amd64-jessie.deb


Install_programms()

def MakeSystemProgrammsForm():
	dy = max(n_systemPrograms,len(VsiProgrami)-n_systemPrograms)
	global formSystemPrograms
	formSystemPrograms = Form('System Programs',3,2 ,28,dy+4)
	global editPrigramms
	editPrigramms =[]
	global NthProgram
	for NthProgram in range(0, n_systemPrograms):
		editPrigramms.append(Edit('(' + str(NthProgram+1) + ')', formSystemPrograms.x+3 ,formSystemPrograms.y + NthProgram + 2))
		editPrigramms[NthProgram].new_value(VsiProgrami[NthProgram])

def MakeOtherProgrammsForm():
	dx = formSystemPrograms.x+formSystemPrograms.dx
	dy = max(n_systemPrograms,len(VsiProgrami)-n_systemPrograms)
	global formOtherPrograms
	formOtherPrograms = Form('Other Programs', dx+3,2 ,28,dy+4)
	for NthProgram in range(n_systemPrograms, len(VsiProgrami)):
		editPrigramms.append(Edit('(' + str(NthProgram+1) + ')', formOtherPrograms.x+3 ,formOtherPrograms.y + NthProgram - n_systemPrograms + 2))
		editPrigramms[NthProgram].new_value(VsiProgrami[NthProgram])

MakeSystemProgrammsForm()
MakeOtherProgrammsForm()

def MakeHelpForm():
	HotKeys = [	'n      - CHOOSE PROGRAM',
				'all    - INSTALL ALL',
				'tit    - INSTALL:',
				'		+ Arduino',
				'		+ qCAD',
				'		+ FreeCAD',
				'		+ Sublime',
				'system - INSTALL:',
				'		+ Htop',
				'		+ Terminator',
				'pef 	- INSTALL:',
				'		+ Arduino IDE',
				'		+ Fritzing',
				'		+ Sublime',
				"		+ dave's conky",
				'		+ openbox-menu',
				'--------------------------',
				'ENTER  - MAIN MENU',
				'q      - EXIT',
				]
	x = formOtherPrograms.x + formOtherPrograms.dx + 3
	formHelp = Form('MENU',x,2,33,formSystemPrograms.dy)
	t_Keys = []
	for n in range(0, len(HotKeys)):
		t_Keys.append(Text(HotKeys[n],formHelp.x+3,formHelp.y+n+2))

# MAIN PROGRAM ##############################################
def Main():
	MakeHelpForm()
	MakeSystemProgrammsForm()
	MakeOtherProgrammsForm()
	y1 = formSystemPrograms.y + formSystemPrograms.dy + 4
	y2 = formOtherPrograms.y + formOtherPrograms.dy + 4
	setCursor(1,max(y1,y2))
	#global editCmd
	#editCmd = Edit('Cmd',1,20)
	#editCmd.value = ''

key = ''
cls()
Main()
Main()
#while (editCmd.value != 'q'):
while (key != 'q'):
	key = raw_input('Cmd::')
	programe_index=(i for i in xrange(50))
	programe_index.next()
	if key == '':
		cls()
		Main()
	#---------------------------------------SYSTEM PROGRAMS	
	elif key == str(programe_index.next()):	Update_Upgrade.install()	
	elif key == str(programe_index.next()):	git.install()
	elif key == str(programe_index.next()):	java_8.install()
	elif key == str(programe_index.next()):	obmenu.install()
	elif key == str(programe_index.next()):	Terminator.install()
	elif key == str(programe_index.next()):	Htop.install()
	elif key == str(programe_index.next()):	nmon.install()
	elif key == str(programe_index.next()):	wavemon.install()
	elif key == str(programe_index.next()):	Neofetch.install()
	elif key == str(programe_index.next()):	Fortune.install()
	elif key == str(programe_index.next()):	Cowsay.install()
	elif key == str(programe_index.next()):	Keymap.install()
	elif key == str(programe_index.next()):	conky.install()
	elif key == str(programe_index.next()):	dave_s_conky.install()
	elif key == str(programe_index.next()):	ll.install()
	elif key == str(programe_index.next()):	weather.install()
	elif key == str(programe_index.next()):	FileZilla.install()
	elif key == str(programe_index.next()):	python_serial.install()
	elif key == str(programe_index.next()):	FreeFileSync.install()
	#---------------------------------------OTHET PROGRAMS
	elif key == str(programe_index.next()):	Arduino.install()
	elif key == str(programe_index.next()):	qCAD.install()
	elif key == str(programe_index.next()):	FreeCAD.install()
	elif key == str(programe_index.next()):	Sublime.install()
	elif key == str(programe_index.next()):	LibreOffice.install()
	elif key == str(programe_index.next()):	Thunderbird.install()
	elif key == str(programe_index.next()):	GoogleChrome.install()
	elif key == str(programe_index.next()):	W3M.install()
	elif key == str(programe_index.next()):	Skype.install()
	elif key == str(programe_index.next()):	stellarium.install()
	elif key == str(programe_index.next()):	Foxitreader.install()
	elif key == str(programe_index.next()):	Fritzing.install()
	elif key == str(programe_index.next()):	texmaker.install()
	elif key == str(programe_index.next()):	inkscape.install()
	elif key == str(programe_index.next()):	gimp.install()
	elif key == str(programe_index.next()):	mypaint.install()
	elif key == str(programe_index.next()):	audacity.install()
	elif key == str(programe_index.next()):	evince.install()
	elif key == str(programe_index.next()):	k3b.install()
	elif key == str(programe_index.next()):	bCNC.install()
	elif key == str(programe_index.next()):	lmms.install()
	elif key == str(programe_index.next()):	eclipse.install()
	elif key == 'all':
		#---SYSTEM PROGRAMS
		Update_Upgrade.install()	
		git.install()
		java_8.install()
		obmenu.install()
		Terminator.install()
		Htop.install()
		nmon.install()
		wavemon.install()
		Neofetch.install()
		Fortune.install()
		Cowsay.install()
		Keymap.install()
		conky.install()
		dave_s_conky.install()
		ll.install()
		weather.install()
		FileZilla.install()
		python_serial.install()
		FreeFileSync.install()
		#---OTHER PROGRAMS
		Arduino.install()
		qCAD.install()
		FreeCAD.install()
		Sublime.install()
		LibreOffice.install()
		Thunderbird.install()
		GoogleChrome.install()
		W3M.install()
		Skype.install()
		stellarium.install()
		Foxitreader.install()
		texmaker.install()
		inkscape.install()
		gimp.install()
		mypaint.install()
		audacity.install()
		evince.install()
		k3b.install()
		bCNC.install()
		lmms.install()
		eclipse.install()
	elif key == 'tit':	
		Arduino.install()
		qCAD.install()
		FreeCAD.install()
		Sublime.install()
		stellarium.install()
		Fritzing.install()
	elif key == 'system':
		Update_Upgrade.install()	
		Terminator.install()
		Htop.install()
		nmon.install()
	elif key == 'pef':
		Arduino.install()
		Fritzing.install()
		Sublime.install()
		dave_s_conky.install()
		obmenu.install()
	else:	
		os.system(key)
	#Main()
			
cls()
