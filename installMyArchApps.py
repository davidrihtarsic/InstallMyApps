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
				dummy_file = os.popen('sudo pacman -Qs '+yaourt_cmd)
				is_installed = dummy_file.read()
				if self.category == 'Auto':
					if len(is_installed)>1 :
						#it is alredy installed... skip it!
						sys.stdout.write(thisAppOutput+'Paket : '+ yaourt_cmd +' je ze namescen.' +escapeColorDefault+'\n' )
						sys.stdout.write(escapeColorInstalled + is_installed+escapeColorDefault+'\n' )
						key='n'
					else:
						#it is not installed... install it!
						key = 'y'
				else:
					key = input(thisAppOutput+'execute:'+yaourt_cmd+ confirmText)
				if key == 'y':
					os.system('yaourt -S --noconfirm '+yaourt_cmd)

	def arch_pacman_install(self):
		## install from terminal pacman command
		if len(self.arch_pacman_cmds) != 0:
			for pacman_install in self.arch_pacman_cmds:
				dummy_file = os.popen('sudo pacman -Qs '+pacman_install)
				is_installed = dummy_file.read()
				if self.category == 'Auto':
					if len(is_installed)>1 :
						#it is alredy installed... skip it!
						sys.stdout.write(thisAppOutput+'Paket : '+ pacman_install +' je ze namescen.' +escapeColorDefault+'\n' )
						sys.stdout.write(escapeColorInstalled + is_installed+escapeColorDefault+'\n' )
						key='n'
					else:
						#it is not installed... install it!
						key = 'y'
				else:
					key = input(thisAppOutput+'execute:'+pacman_install+ confirmText)
				if key == 'y':
					os.system('sudo pacman -S --noconfirm ' + pacman_install)

	def arch_run_zsh_cmds(self):
		## Post INSTALL operations #####################################################
		if len(self.arch_zsh_cmds) != 0:
			for arch_zsh_cmds in self.arch_zsh_cmds:
				if self.category == 'Auto':
					key='y'
				else:
					key = input(thisAppOutput+'execute:'+arch_zsh_cmds+ confirmText)
				if key == 'y':
					os.system(arch_zsh_cmds)

	def install_apt_cmd(self):
		## Instal from special apt-get command ... #####################################
		if len(self.pre_install_cmds) != 0:
			for pre_cmd in self.pre_install_cmds:
				key = input(thisAppOutput+'execute:'+pre_cmd+ confirmText)
				if key == 'y':
					os.system(pre_cmd)
		if self.apt_get_name != '':
		## Instal from clasical apt-get commend... #####################################
			#ce smo vpisali apt-get podatke potem...
			sys.stdout.write(thisAppOutput+'Preverjam apt-get paket: ' + self.apt_get_name +escapeColorDefault+'\n' )
			os.system('apt-cache policy ' + self.apt_get_name)
			key = input(thisAppOutput+'Namestim preko apt-get... ?'+confirmText)
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
				key = input(thisAppOutput+'Prenesi v '+download_dir+ confirmText)
				if key == 'y':
					os.system('wget '+ temp_deb_package_path + temp_deb_package_file + ' --directory-prefix='+download_dir )
			#pokazi direktorij Download
			if os.path.isfile(download_dir+temp_deb_package_file):
				sys.stdout.write(thisAppOutput+'Nasel:'+escapeColorDefault+'\n')
				os.system('ls -all ' + download_dir + ' | grep ' + temp_deb_package_file)
				key = input(thisAppOutput+'Namesti DEB package: ' + temp_deb_package_file + confirmText)
				if key == 'y':
					os.system('sudo dpkg -i ' + download_dir + temp_deb_package_file)
					sys.stdout.write(thisAppOutput+'Namestitev koncana...'+escapeColorDefault+'\n')	
				key = input(thisAppOutput+'Izbrisi datoteko:'
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
				key = input(thisAppOutput+'Prenesi v '+download_dir+ '?'+confirmText)
				if key == 'y':
					os.system('wget '+ temp_tar_package_path + temp_tar_package_file + ' --directory-prefix='+download_dir )
			#pokazi direktorij Download
			if os.path.isfile(download_dir+temp_tar_package_file):
				sys.stdout.write(thisAppOutput+'Nasel:'+escapeColorDefault+'\n')
				os.system('ls -all ' + download_dir + ' | grep ' + temp_tar_package_file)
				if self.tar_destination == '':
					key = input(thisAppOutput+'Razpakiraj TAR package: '
									+ temp_tar_package_file +
									' v ' + download_dir + '?'+confirmText)
					if key == 'y':
						os.system('tar -xvf '+ download_dir+temp_tar_package_file 
								+' --directory '+ download_dir)
				else:
					key = input(thisAppOutput+'Razpakiraj TAR package: '
									+ temp_tar_package_file +
									' v ' + self.tar_destination + '?'+confirmText)
					if key == 'y':
						if not os.path.isdir(self.tar_destination):
							#ce dir se ne obstaja ga ustvari...
							os.system('sudo mkdir ' + self.tar_destination)
						os.system('sudo tar -xvf '+download_dir+temp_tar_package_file
									+' --directory '+ self.tar_destination)
				# Izbrisi kar smo zloadali... da pocistimo za seboj...
				key = input(thisAppOutput+'Izbrisi datoteko:'
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
					key = input(thisAppOutput+'execute:'+extra_cmd+confirmText)
					if key == 'y':
						os.system(extra_cmd)

	def add_PATH_parameter(self):
		## dodajanje v path script #######################################################			
		#sudo sh -c 'echo "export PATH=\$PATH:/opt/arduino-1.8.1" >> /etc/profile.d/arduino_path.sh'	
		if len(self.add_path_profile_variable) != 0:
			# ce in nastavljeno pot... to dodamo v $PATH
			key = input(thisAppOutput+'Dodaj pot:'+ self.add_path_profile_variable + ' v $PATH ?'+confirmText)
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
				#key = input(thisAppOutput+'Dodaj text: '+ text + ' v ~/.bashrc ?'+confirmText)
				key = input(thisAppOutput+'Dodaj text: '+ text + ' v ~/.zshrc ?'+confirmText)
				if key == 'y':
					#if (open(user_path + '/.bashrc', 'r').read().find(text)>0):
					if (open(user_path + '/.zshrc', 'r').read().find(text)>0):
						sys.stdout.write(thisAppOutput+'Text: '+ text +' ze dodano v : '+ user_path + '/.zshrc...'+escapeColorDefault+'\n')
					else:
						# tu naj gremo cez vse nize v parametru...
						with open(user_path + '/.zshrc','a') as f:
							f.write(text)
						f.close()

	def run_bash_cmds(self):
		## Post INSTALL operations #####################################################
		if len(self.extra_cmd) != 0:
			for extra_cmd in self.extra_cmd:
				key = input(thisAppOutput+'execute:'+extra_cmd+ confirmText)
				if key == 'y':
					os.system(extra_cmd)
	
	def make_destop_file(self):
		## Dodajanje program.desktop datoteke v /usr/share/applications/ ################
		if len(self.program_desktop) != 0:
			# test ce je kaj not: sys.stdout.write(self.program_desktop[0])
			# sudo sh -c 'echo "export PATH=\$PATH:/opt/arduino-1.8.1" >> /etc/profile.d/arduino_path.sh'
			key = input(thisAppOutput+'Naredi menu:'+ menu_desktop + self.program_name+ '.desktop ?'+confirmText)
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
					#sys.stdout.write('\n new_start at:'+str(new_start))
					#sys.stdout.write('\n new_line at :'+str(new_line))
					#sys.stdout.write('\n presledek at:'+str(presledek))
					#sys.stdout.write('\n lst_presl at:'+str(last_presledek)+'\n')
					print(escapeColorDefault+self.description[new_start:last_presledek])
					new_start = last_presledek + 1 	
				else:
					if (presledek > 0):
					    last_presledek=presledek

			sys.stdout.write(escapeColorDefault+self.description[new_start:]+''+escapeColorDefault+'\n'
							+'###########################################################\n')
		if (self.category=='Auto'):
			key = 'y'
		else:
			key = input(thisAppOutput+'Nadaljuj z namestitvijo?'+confirmText)
		if key == 'y':
			self.arch_yaourt_install()
			self.arch_pacman_install()
			self.arch_run_zsh_cmds()
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
	#Ime_Novega_Programa.pre_install_cmds = []					
	#	PRE_INSTALL_CMDS - niz stringov se izvrsi kakor ce bi jih vpisovali v terminal
	#	eden za drugim. Izvrsijo se pred vsemi ostalimi ukazi (apt-get install, deb, tar).
	#	Med vsakim navedenim nizom nas program tudi vprasa ali zelimo izvrsiti ukaz [y/n].
	#	primer uporabe:
	#	novProgram.pre_install_cmds = [	'sudo apt-get update',
	#									'sudo apt-get upgrade']
	#Ime_Novega_Programa.apt_get_name = ''
	#	APT_GET_NAME - to ime se uporabi v ukazu sudo apt-get install {apt_get_name}.
	#	Predno se izvede ta ukaz gremo pogledat, katera verzija je na razpolago z
	#	ukazom: sudo apt-cache policy. Tako se uporaabnik lahko odloci ali bo namestil
	#	program s tem ukazom ali ne.
	#	primer uporabe:
	#	novProgram.apt_get_name = 'nano'
	#Ime_Novega_Programa.deb_package_path = ''
	#	DEB_PACKAGE_PATH - pot datoteke na kateri se nahaja *deb paket. Ta se uporablja
	#	v primeru, ko vrsta arhitekture ni pomembna ali pa paket ne podpira razlicnih
	#	arhitektur.
	#	primer uporabe:
	#	novProgram.deb_package_path = 'https://download.sublimetext.com/'
	#Ime_Novega_Programa.deb_package_file = ''
	#	DEB_PACKAGE_FILE - ime datoteke, ki se nahaja na prej omenjeni poti {deb_package_path}.
	#	Ta string v tej spremenljivki se uporablja tudi za instalacijo deb paketa:
	#	sudo dpkg -i {deb_package_file}. Presnete datoteke se na koncu postopka tudi izbrisejo.
	#	primer uporabe:
	#	novProgram.deb_package_file = 'sublime-text_build-all.deb'
	#Ime_Novega_Programa.deb_package_path_32 = ''
	#	DEB_PACKAGE_PATH_32 - enako kot pri {deb_package_path}, le da se *.deb paket namesti le
	#	ce imate 32-bitni sistem. 
	#Ime_Novega_Programa.deb_package_file_32 = ''
	#	DEB_PACKAGE_FILE_32 - enako kot pri {deb_package_path}, le da se *.deb paket namesti le
	#	ce imate 32-bitni sistem. 
	#Ime_Novega_Programa.deb_package_path_64 = ''
	#	DEB_PACKAGE_PATH_64 - enako kot pri {deb_package_path}, le da se *.deb paket namesti le
	#	ce imate 64-bitni sistem. 
	#Ime_Novega_Programa.deb_package_file_64 = ''
	#	DEB_PACKAGE_FILE_64 - enako kot pri {deb_package_path}, le da se *.deb paket namesti le
	#	ce imate 64-bitni sistem. 
	#Ime_Novega_Programa.tar_package_path = ''
	#	TAR_PACKAGE_PATH - pot datoteke na kateri se nahaja *.tar.gz ali *.tar.xz paket. Ta se
	#	uporablja v primeru, ko vrsta arhitekture ni pomembna ali pa paket ne podpira razlicnih
	#	arhitektur.
	#	primer uporabe:
	#	novProgram.tar_package_path = 'https://qcad.org/archives/qcad/'
	#Ime_Novega_Programa.tar_package_file = ''
	#	TAR_PACKAGE_FILE - ime datoteke, ki se nahaja na prej omenjeni poti {tar_package_path}.
	#	Ta string v tej spremenljivki se uporablja tudi za razpakiranje *.tar paketa:
	#	tar -xvf '+ download_dir+{tar_package_file}. Datoteke se razpakirajo v ~/Download/, ali
	#	pa pot lahko tudi posebej dolocite v spremenljivki {tar_destination}. Presnete datoteke
	#	se na koncu postopka tudi izbrisejo.
	#	primer uporabe:
	#	novProgram.tar_package_file = 'sublime-text_build-all.tar.gz'
	#Ime_Novega_Programa.tar_package_path_32 = ''
	#	TAR_PACKAGE_PATH_32 - enako kot pri {tar_package_path}, le da se *.tar.* paket namesti le
	#	ce imate 32-bitni sistem. 
	#Ime_Novega_Programa.tar_package_file_32 = ''
	#	TAR_PACKAGE_FILE_32 - enako kot pri {tar_package_file}, le da se *.tar.* paket namesti le
	#	ce imate 32-bitni sistem. 
	#Ime_Novega_Programa.tar_package_path_64 = ''
	#	TAR_PACKAGE_PATH_64 - enako kot pri {tar_package_path}, le da se *.tar.* paket namesti le
	#	ce imate 64-bitni sistem. 
	#Ime_Novega_Programa.tar_package_file_64 = ''
	#	DEB_PACKAGE_FILE_64 - enako kot pri {deb_package_path}, le da se *.deb paket namesti le
	#	ce imate 64-bitni sistem. 
	#Ime_Novega_Programa.tar_destination = ''
	#	TAR_DESTINATION - direktorij, kamor zelite, da se *.tar.* paket od-tara. Ce direktorij se
	#	ne obstaja, da bo instalacija sama ustvarila...
	#	primer uporabe:
	#	novProgram.tar_destiation = '/opt/'
	#Ime_Novega_Programa.tar_extra_cmds = []
	#	TAR_EXTRA_CMDS - Po koncanem razpakiranju TAR datoteke lahko naredite se kake cmd, kot
	# 	bi jih pisali v terminalu: naprimer kake instalacije ali kaj podobnega...
	#	primer uporabe:
	#	novProgram.tar_extra_cmds =['sudo rm /usr/bin/nmon',
	#								'sudo chmod 777 '+opt_dir+'nmon/'+'nmon_x86_debian8',
	#								'sudo ln -s '+opt_dir+'nmon/'+'nmon_x86_debian8 /usr/bin/nmon']
	#Ime_Novega_Programa.program_desktop = []
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
	#Ime_Novega_Programa.add_path_profile_variable  = ''
	#	ADD_PATH_PROFILE_VARIABLE - string, ki ga je potrebno vpisati v $PATH spremenljivko.
	#	primer uporabe:
	#	Arduino.add_path_profile_variable  = '/opt/arduino-nightly/
	#Ime_Novega_Programa.extra_cmd = []
	#	EXTRA_CMD - niz ukazov, ki bi jih morali vtipkati v terminal po instalacijskem postopku.
	#	Na tem mestu lahko dodate link v /usr/bin/ tako, da lahko zazenete program od koderkoli,
	#	kakor smo to naredili za program thunderbird...
	#	primer uporabe:
	#	Thunderbird.extra_cmd = ['sudo ln -s /opt/thunderbird/thunderbird /usr/bin/thunderbird'] 
	#Ime_Novega_Programa.add_bash_parameter = []
	#	ADD_BASH_PARAMETER - niz stringov (besedila), ki ga je potrebno dodati v datoteko:
	#	~/.bashrc. Besedilo se doda na konec dokumenta. Skript vas vprasa za vsak niz posebej,
	#	ce naj ga doda.
	#	primer uporabe:
	#	Keymap.add_bash_parameter = [	'\n#remap tipko [dz] - "/"',
	#									'\nxmodmap -e "keycode 35 = slash"']
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
	#Ime_Novega_Programa.description = ''
	#Ime_Novega_Programa.pre_install_cmds = []					
	#Ime_Novega_Programa.apt_get_name = ''
	#Ime_Novega_Programa.deb_package_path = ''
	#Ime_Novega_Programa.deb_package_file = ''
	#Ime_Novega_Programa.deb_package_path_32 = ''
	#Ime_Novega_Programa.deb_package_file_32 = ''
	#Ime_Novega_Programa.deb_package_path_64 = ''
	#Ime_Novega_Programa.deb_package_file_64 = ''
	#Ime_Novega_Programa.tar_package_path = ''
	#Ime_Novega_Programa.tar_package_file = ''
	#Ime_Novega_Programa.tar_package_path_32 = ''
	#Ime_Novega_Programa.tar_package_file_32 = ''
	#Ime_Novega_Programa.tar_package_path_64 = ''
	#Ime_Novega_Programa.tar_package_file_64 = ''
	#Ime_Novega_Programa.tar_destination = ''
	#Ime_Novega_Programa.tar_extra_cmds = []
	#Ime_Novega_Programa.program_desktop = []
	#Ime_Novega_Programa.add_path_profile_variable  = ''
	#Ime_Novega_Programa.extra_cmd = []
	#Ime_Novega_Programa.add_bash_parameter = []
	#Ime_Novega_Programa.check_version_cmd = ''
	#Ime_Novega_Programa.notes = ''
	#
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

## NMON ########################################################
	global nmon
	nmon = NovProgram()
	nmon.program_name = 'nmon'
	nmon.category = 'System'
	nmon.description = 'Spremljanje procesov, diska...'
	nmon.arch_pacman_cmds = ['pacman -S nmon']
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
	nmap.arch_pacman_cmds = ['sudo pacman -S nmap']
## ADB  to-do ##################################################
## Keymap ######################################################
#	global Keymap
#	Keymap = NovProgram()
#	Keymap.description='remap tipke [dz] v "/"'
#	Keymap.program_name = 'Keymap'
#	Keymap.category = 'System'
#	Keymap.add_bash_parameter = ['\n#remap tipko [dz] - "/"','\nxmodmap -e "keycode 35 = slash"']			#text ki je za dodat v .bash 
## BunsenLab personal settings #################################
	#	global bunsenLabSettings
	#	bunsenLabSettings = NovProgram()
	#	bunsenLabSettings.program_name = '_to_do_myBunsenLabSettings'					#ime naj bo brez presledkov
	#	bunsenLabSettings.category = 'System'
	#	bunsenLabSettings.description = 'V datoteki "~/.config/openbox/rc.xml" je vpisanih kar nekaj bliznjic, ki jih lahko uporabljate v OS BunsenLab linuxu. Tej datoteki je dodano se nekaj osebnih nastavitev. Naprimer:\n + [Ctrl]+[Space] => Run Linux CMD\n + [S]+[A]+[Up] => Maximize Window... '#neko besedilo za opis
	#	bunsenLabSettings.extra_cmd = ['mv ~/.config/openbox/rc.xml ~/.config/openbox/rc.xml_original',\
	#						'wget "https://github.com/davidrihtarsic/BunsenLab/raw/master/rc.xml" -O ~/.config/openbox/rc.xml',\
	#						'openbox --restart']#se ene extra cmd ... ce je se kaj...
	#	# obmenu.notes = ''
## ARCH config files ###########################################
	global Arch_config
	Arch_config = NovProgram()
	Arch_config.program_name = 'Upadate .config'
	Arch_config.category = 'System'
	Arch_config.description = 'Moji .config fili iz GitHuba...'
	Arch_config.arch_zsh_cmds = ['cp -r -v ~/Files/GitHub_noSync/ArchLabs/MyDotFiles/. ~'
							]
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
 	#
## python-serial ###############################################
	#test OK @ BL 64bit (David)
	#global python_serial
	#python_serial = NovProgram()
	#python_serial.program_name = '_to_do_python-serial'
	#python_serial.category = 'System'
	#python_serial.description = 'This module encapsulates the access for the serial port. It provides backends for Python running on Windows, OSX, Linux, BSD (possibly any POSIX compliant system) and IronPython. The module named "serial" automatically selects the appropriate backend.'
	#python_serial.apt_get_name = 'python-serial'
	##python-serial.notes = ''
 	#
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
	#64 bit BL tested
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
	destination.category = 'Auto'




Install_programms()
# find programs and categorize them
#Force System as first
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
#remove category Auto
all_categorys.remove('Auto')
category_programs.pop(0)

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
		#input()

makeAllProgramForms()
#key = input()

def MakeHelpForm():
	HotKeys = [	'--Menu------------------',
				'n      - inst. program',
				'Update - Update & Upgrade',
				'ENTER  - MAIN MENU',
				'q      - EXIT'
				]

	x = allForms[0].x + (allForms[0].dx +1) * colons 
	y = allForms[0].y
	dx = allForms[0].dx
	#if colons == 1:
	#	dy = allForms[len(allForms)-1].y + allForms[len(allForms)-1].dy -4
	#else:
	#	dy = allForms[0].dy * len(allForms)//colons 
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
	makeAllProgramForms()
	MakeHelpForm()
	#y = allForms[0].dy * len(allForms)//colons + 5
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
	# preglej vse programe...
	for obj in NovProgram.getinstances():
		if key == str(obj.index):
			obj.install()	
	if key == 'all':
		for obj in NovProgram.getinstances():
			obj.install()	
	elif key == 'Update':
		os.system('sudo pacman -Syu')
	elif key in all_categorys:
		for program in NovProgram.getinstances():
			if program.category == key:
				program.install()
	elif key == 'tit':	
		Arduino.install()
		qCAD.install()
		FreeCAD.install()
		Sublime.install()
		stellarium.install()
		Fritzing.install()
	elif key == 'System':
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
		#f = os.popen(key)
		#text = f.read()
		#print(text)
		#input()
		os.system(key)
	#Main()
			
cls()
