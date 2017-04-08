#!/usr/bin/env python
from myTUI import Form, Edit, Text, cls, systemCmd, putText, setCursor
import sys
import os

cls()
# PROGRAMI ##################################################
# ImePrograma - AptCommand - DEB pachage - InstallFromSource
#  todo...

user = os.path.expanduser('~')
download_dir = user + '/Downloads/'
opt_dir = '/opt/'
menu_desktop = '/usr/share/applications/'
profile_dir = '/etc/profile.d/'
VsiProgrami = []

## REVISION ####################################################
version = 3.3
		# dodan alias ll za ls -alF
		# install funkcija razbita na podfunkcije...
	## version = 3.1
		# dodano arduino.desktop
	##version = 3.0
		# dodan concky :)
	## version = 2.9.1
		# dodan program za avtomatsko kreiranje menuja
		# v OpenBox okolju (za BunsenLab) 
	## version = 2.9
		# dodana pot za 32 bit ... ker se nekateri programi
		# programi razlikujejo... tako za TAR in DEB.
	## version = 2.8
		# program.desktop se naredi le ce se ni tega file-a	
	## version = 2.7
		## popravljeno dodajanje v $PATH tako,
		# da se to doda v ~/.bashrc in se prej pregledamo
		# ce besedilo slucajno ze obstaja
		## popravljeno vnasanje program.desktop tako,
		# da te sedaj vprasa po SUDO... in ni potrebno vec
		# cele skripte zaganjati s sudo ukazom...
	## version = 2.6
		# popravljen link 32bit za sublime...	
	## version = 2.5
		# popravljene so bile nastavitve za instalacijo Arduinota
		# sedaj se odTara v /opt/ in doda PATR... in to = to
	## version = 2.4
		# dodani 32 paketi za nekatere programe...
	## version = 2.3
		# narejena podpora za tar tako, da uposteva 64 in 32 bit arhitekturo
	## version = 2.2
		# narejena podpora za 64 / 32 bit za DEB packages...
## BUGS REPORT #################################################
	## issue:35
		# lahko bi preverjal katera verzija Linuxsa je namescena
		# cat /etc/*ease
	## issue:34 SOLVED!
		# skripto je potrebno zagnati kot "root", ker te za nekatere
		# ukaze ne vprasa po sudo geslu... to se da resiti.. navodila
		# na : hm/ne/vem/vec.kje
	## issue: 33
		# ni se programa LibreOffice
	## issue: 32 
		# ni se programa neofetch
		#	

## POSTOPEK INSTALACIJE ########################################
class NovProgram(object):
	"""docstring for NovProgram"""
	def __init__(self):
		super(NovProgram, self).__init__()
		self.program_name = ''
		self.description = ''
		self.apt_get_cmd = ''
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
		self.tar_extra_cmd = [] 	#extra commande, ce je se kaj za narest...
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
		if self.apt_get_cmd != '':
			#ce je kaka komanda prej za izvrsit naj to naredi...
			os.system('sudo apt-get ' + self.apt_get_cmd)
		if self.apt_get_name != '':
		## Instal from clasical apt-get commend... #####################################
			#ce smo vpisali apt-get podatke potem...
			sys.stdout.write('--> Preverjam apt-get paket: ' + self.apt_get_name +'\n' )
			os.system('apt-cache policy ' + self.apt_get_name)
			key = raw_input('--> Namestim preko apt-get... ? [y/n]')
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
				sys.stdout.write('--> Kaze, da imate 64bit arhitekturo...\n')
				temp_deb_package_path = self.deb_package_path_64
				temp_deb_package_file = self.deb_package_file_64
			elif (self.deb_package_file_32 != '' and self.arhitecture_32bit):
				sys.stdout.write('--> Kaze, da imate 32bit arhitekturo...\n')
				temp_deb_package_path = self.deb_package_path_32
				temp_deb_package_file = self.deb_package_file_32
			else:
				sys.stdout.write('--> Ne glede na arhitekturo...\n')
				temp_deb_package_path = self.deb_package_path
				temp_deb_package_file = self.deb_package_file
				#-------------------------------------------------
			#ce je vpisan deb paket potem ...
			#najprej preveri, ce ga slucajno ze imamo v Downloadu...
			#ce ne pojdi na internet...
			if not os.path.isfile(download_dir+temp_deb_package_file):
				#ce file ne obstaja gremo gledat na internet...
				sys.stdout.write('--> Preverjam DEB package...\n')
				os.system('wget --spider -v '+temp_deb_package_path+temp_deb_package_file)
				key = raw_input('--> Prenesi v '+download_dir+ '? [y/n]:')
				if key == 'y':
					os.system('wget '+ temp_deb_package_path + temp_deb_package_file + ' --directory-prefix='+download_dir )
			#pokazi direktorij Download
			if os.path.isfile(download_dir+temp_deb_package_file):
				sys.stdout.write('--> Nasel:\n')
				os.system('ls -all ' + download_dir)
				key = raw_input('--> Namesti DEB package: ' + temp_deb_package_file + ' [y/n]:')
				if key == 'y':
					os.system('sudo dpkg -i ' + download_dir + temp_deb_package_file)
					sys.stdout.write('--> Namestitev koncana...\n')	
				key = raw_input('--> Izbrisi datoteko:'
								+ download_dir + temp_deb_package_file
								+ ' [y/n]:')
				if key == 'y':
					os.system('rm ' + download_dir + temp_deb_package_file)
					sys.stdout.write('--> Izprisano:\n')
					os.system('ls -all ' + download_dir)
			else:
				sys.stdout.write('--> Paketa: '+ temp_deb_package_file +' nismo nasli...\n')

	def install_TAR_package(self):
		## Install form TAR **** special !!! ###########################################
		if (self.tar_package_file !='' or
		(self.tar_package_file_64 != '' and self.arhitecture_64bit ) or
		(self.tar_package_file_32 != '' and self.arhitecture_32bit )):
			#Najprej poglejmo kaksno arhitekturo imamo
			if (self.tar_package_file_64 != '' and self.arhitecture_64bit ):
				sys.stdout.write('--> Kaze, da imate 64bit arhitekturo...\n')
				temp_tar_package_path = self.tar_package_path_64
				temp_tar_package_file = self.tar_package_file_64
			elif (self.tar_package_file_32 != '' and self.arhitecture_32bit):
				sys.stdout.write('--> Kaze, da imate 32bit arhitekturo...\n')
				temp_tar_package_path = self.tar_package_path_32
				temp_tar_package_file = self.tar_package_file_32
			else:
				sys.stdout.write('--> Ne glede na arhitekturo...\n')
				temp_tar_package_path = self.tar_package_path
				temp_tar_package_file = self.tar_package_file
			#Najprej zloadas tar file ... izi bizi...
			if not os.path.isfile(download_dir+self.tar_package_file):
				#ce file ne obstaja gremo gledat na internet...
				sys.stdout.write('--> Preverjam TAR package...\n')
				os.system('wget --spider -v '+temp_tar_package_path+temp_tar_package_file)
				key = raw_input('--> Prenesi v '+download_dir+ '? [y/n]:')
				if key == 'y':
					os.system('wget '+ temp_tar_package_path + temp_tar_package_file + ' --directory-prefix='+download_dir )
			#pokazi direktorij Download
			if os.path.isfile(download_dir+temp_tar_package_file):
				sys.stdout.write('--> Nasel:\n')
				os.system('ls -all ' + download_dir)
				if self.tar_destination == '':
					key = raw_input('--> Razpakiraj TAR package: '
									+ temp_tar_package_file +
									' v ' + download_dir + '?  [y/n]:')
					if key == 'y':
						os.system('tar -xvf '+ download_dir+temp_tar_package_file 
								+' --directory '+ download_dir)
				else:
					key = raw_input('--> Razpakiraj TAR package: '
									+ temp_tar_package_file +
									' v ' + self.tar_destination + '?  [y/n]:')
					if key == 'y':
						if not os.path.isdir(self.tar_destination):
							#ce dir se ne obstaja ga ustvari...
							os.system('sudo mkdir ' + self.tar_destination)
						os.system('sudo tar -xvf '+download_dir+temp_tar_package_file
									+' --directory '+ self.tar_destination)
				# Izbrisi kar smo zloadali... da pocistimo za seboj...
				key = raw_input('--> Izbrisi datoteko:'
									+ download_dir + temp_tar_package_file
									+ ' [y/n]:')
				if key == 'y':
					os.system('rm ' + download_dir + temp_tar_package_file)
					sys.stdout.write('--> Izbrisano:\n')
					os.system('ls -all ' + download_dir)
			else:
				sys.stdout.write('--> Datoteke: '+download_dir+temp_tar_package_file+' nismo nasli...\n')

			## INSTALATION SOURCE CODE #######################################################
				# ok sedaj naj bi bilo razpakirano... kjerkoli pac ze...
				#ja nic zej pa ce je treba se kako EXTRA CMD narest!!!
				#naprimer kak make, make install, itd
				#skratka izvrsimo komande, ki jih najdemo v :
				#self.tar_extra_cmd = ['make','make install']
			if len(self.tar_extra_cmd) != 0:	
				for extra_cmd in self.tar_extra_cmd:
					key = raw_input('--> execute:'+extra_cmd+ ' [y/n]')
					if key == 'y':
						os.system(extra_cmd)

	def add_PATH_parameter(self):
		## dodajanje v path script #######################################################			
		#sudo sh -c 'echo "export PATH=\$PATH:/opt/arduino-1.8.1" >> /etc/profile.d/arduino_path.sh'	
		if len(self.add_path_profile_variable) != 0:
			# ce in nastavljeno pot... to dodamo v $PATH
			key = raw_input('--> Dodaj pot:'+ self.add_path_profile_variable + ' v $PATH ? [y/n]')
			if key == 'y':
				if (open(user + '/.bashrc', 'r').read().find(self.add_path_profile_variable)>0):
					sys.stdout.write('--> Pot: '+ self.add_path_profile_variable +' ze dodana v : '+ user + '/.bashrc...\n')
				else:
					with open(user + '/.bashrc','a') as f:
						f.write('\n#dodajanje '+self.program_name+' poti v path\n')
						f.write('export PATH=$PATH:'+self.add_path_profile_variable+'\n')
						f.close()

	def add_BASH_parameter(self):
		if len(self.add_bash_parameter) != 0:
			# ce in nastavljeno pot... to dodamo v $PATH
			for text in self.add_bash_parameter:
				key = raw_input('--> Dodaj text: '+ text + ' v ~/.bashrc ? [y/n]')
				if key == 'y':
					if (open(user + '/.bashrc', 'r').read().find(text)>0):
						sys.stdout.write('--> Text: '+ text +' ze dodano v : '+ user + '/.bashrc...\n')
					else:
						# tu naj gremo cez vse nize v parametru...
						with open(user + '/.bashrc','a') as f:
							f.write(text)
						f.close()

	def run_bash_cmds(self):
		## Post INSTALL operations #####################################################
		if len(self.extra_cmd) != 0:
			for extra_cmd in self.extra_cmd:
				key = raw_input('--> execute:'+extra_cmd+ ' [y/n]')
				if key == 'y':
					os.system(extra_cmd)
	
	def make_destop_file(self):
		## Dodajanje program.desktop datoteke v /usr/share/applications/ ################
		if len(self.program_desktop) != 0:
			# test ce je kaj not: sys.stdout.write(self.program_desktop[0])
			# sudo sh -c 'echo "export PATH=\$PATH:/opt/arduino-1.8.1" >> /etc/profile.d/arduino_path.sh'
			key = raw_input('--> Naredi menu:'+ menu_desktop + self.program_name+ '.desktop [y/n]')
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
			sys.stdout.write('--> Preverjam verzijo...\n')
			os.system(self.check_version_cmd)
		
	def show_notes(self):
		if self.notes != '':
			sys.stdout.write(self.notes+'\n')

	def install(self):
		sys.stdout.write(	 '###########################################################\n'
							+'## Postopek instalacije programa \n'
							+'## ' + self.program_name+'\n'
							+'-----------------------------------------------------------\n')
		if self.description != '':
			sys.stdout.write(self.description+'\n'
							+'###########################################################\n')
		key = raw_input('--> Nadaljuj z namestitvijo? [y/n]')
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
			sys.stdout.write('--> Pritisni [ENTER] za nadaljevanje...\n')

## DEFINICIJA PROGRAMOV ZA INSTALACIJO #########################
def Install_programms():
## PRIMER PROGRAMA #############################################
	# global Primer_programa
	# Primer_programa = NovProgram()
	# Primer_programa.program_name = ''					#ime naj bo brez presledkov
	# Primer_programa.description = ''					#neko besedilo za opis
	# Primer_programa.apt_get_cmd = ''					#ce je kaka komanda prej za narest
	# Primer_programa.apt_get_name = ''					#ime za apt-get
	# Primer_programa.check_version_cmd = ''			#cmd za preverjanje verzije
	# Primer_programa.deb_package_path = ''				#url ua BED (brez fila)
	# Primer_programa.deb_package_file = ''				#file za katerikoli sistem
	# Primer_programa.deb_package_file_32 = ''			#file za 32bit
	# Primer_programa.deb_package_file_64 = ''			#file za 64bit
	# Primer_programa.tar_package_path = ''				#url (brez fila)
	# Primer_programa.tar_package_file = ''				#file za katerikoli sistem
	# Primer_programa.tar_package_file_32 = ''			#file za 32bit
	# Primer_programa.tar_package_file_64 = ''			#file za 64bit
	# Primer_programa.tar_destination = ''				#kam naj od tara.. TAR paket
	# Primer_programa.tar_extra_cmd = []				#extra commande, ce je se kaj za narest...
	# Primer_programa.extra_cmd = []					#se ene extra cmd ... ce je se kaj...
	# Primer_programa.program_desktop = []				#vsebina v program.desktop
	# Primer_programa.add_path_profile_variable  = '' 
	# Primer_programa.add_bash_parameter = []			#text ki je za dodat v .bash 
	# Primer_programa.notes = ''
	# VsiProgrami.append(Primer_programa.program_name)
## UPDATE & UPGRADE ############################################
	global Update_Upgrade
	Update_Upgrade = NovProgram()
	Update_Upgrade.program_name = 'Update & Upgrade'
	Update_Upgrade.description = 'Posodobite sistemske knjiznice...'
	Update_Upgrade.apt_get_cmd = 'update && sudo apt-get upgrade'
	VsiProgrami.append(Update_Upgrade.program_name)
## ARDUINO #####################################################
	global Arduino
	Arduino = NovProgram()
	Arduino.program_name = 'ArduinoIDE'
	Arduino.description = 'Arduino je mikrokrmilnik na maticni plosci, ki je zasnovan\n'\
						'tako da bi bil postopek z uporabo elektronike v multidisci-\n'\
						'plinarnih projektih, bolj dostopen. Strojno opremo sestavljajo\n'\
						'odprtokodna oblika plosce in 8-bitni mikrokrmilnik Atmel AVR\n'\
						'ali 32-bitni Atmel ARM. Programska oprema je sestavljena iz\n'\
						'standardnega programskega jezika, prevajalnika in zagonskega\n'\
						'nalagalnika, ki se izvaja na mikrokrmilniku. Razvojne plosce\n'\
						'Arduino so naprodaj ze sestavljene ali pa v sestavi sam izvedbi.\n'\
						'Mikrokrmilnik so razvili na soli oblikovanja v italijanskem\n'\
						'mestu Ivrea in predstavlja enega zgodnjih mejnikov v gibanju\n'\
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
	#Arduino.tar_extra_cmd = ['sudo ' + Arduino.tar_destination + 'arduino-1.8.1/install.sh']
	Arduino.add_path_profile_variable  = Arduino.tar_destination + 'arduino-nightly/'
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
	qCAD.description = 'Qcad je racunalnisko podprto orodje za 2D nacrtovanje in\n'\
						'risanje. Zacetki razvoja segajo v leto 1999, ko je programsko\n'\
						'orodje nastalo kot rezultat spinoff projekta izdelave CAD\n'\
						'sistema. Z njim izdelamo tehnicne risbe (nacrti zgradb,\n'\
						'njihovih notranjosti, mehanski deli, sheme, diagrami ipd.).\n'\
						'Uporaben je na razlicnih tehniskih podrocjih: strojnistvo,\n'\
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
	Sublime.description = 'Sublime Text is a sophisticated text editor\n'\
						'for code, markup and prose. You\'ll love the\n'\
						'slick user interface, extraordinary features and\n'\
						'amazing performance.'
	Sublime.apt_get_name =''
	Sublime.check_version_cmd = ''
	Sublime.deb_package_path_64 = 'https://download.sublimetext.com/'
	Sublime.deb_package_file_64 = 'sublime-text_build-3126_amd64.deb'
	Sublime.deb_package_path_32 = 'https://download.sublimetext.com/'
	Sublime.deb_package_file_32 = 'sublime-text_build-3126_i386.deb'
	VsiProgrami.append(Sublime.program_name)
## Terminator ##################################################
	global Terminator
	Terminator = NovProgram()
	Terminator.program_name = 'Terminator'
	Terminator.description = 'Lep, eleganten terminal...'
	Terminator.apt_get_name ='terminator'
	Terminator.check_version_cmd = ''
	Terminator.deb_package_path = ''
	Terminator.deb_package_file = ''
	VsiProgrami.append(Terminator.program_name)
## Htop ########################################################
	global Htop
	Htop = NovProgram()
	Htop.program_name = 'Htop'
	Htop.description = 'Spremljanje procesov...'
	Htop.apt_get_name ='htop'
	Htop.check_version_cmd = ''
	Htop.deb_package_path = ''
	Htop.deb_package_file = ''
	VsiProgrami.append(Htop.program_name)
## NMON ########################################################
	global nmon
	nmon = NovProgram()
	nmon.program_name = 'nmon'
	nmon.description = 'Spremljanje procesov... za DEBIAN!'
	nmon.apt_get_name =''
	nmon.tar_package_file = 'nmon16d_x86.tar.gz'
	nmon.tar_package_path = 'http://sourceforge.net/projects/nmon/files/'
	nmon.tar_destination =  opt_dir+'nmon/'
	nmon.tar_extra_cmd =['sudo rm /usr/bin/nmon',
						'sudo chmod 777 '+opt_dir+'nmon/'+'nmon_x86_debian8',
						'sudo ln -s '+opt_dir+'nmon/'+'nmon_x86_debian8 /usr/bin/nmon']
	nmon.program_desktop = ['[Desktop Entry]',
							'Version=1.0',
							'Name=nmon',
							'Exec=terminator -e nmon',
							'Icon=nmon',
							'Terminal=true',
							'Type=Application',
							'Categories=System;Development;Programming;'
							]
	#nmon.tar_extra_cmd = ['sudo mv ' + download_dir + 'nmon/nmon_x86_64_ubuntu15 /usr/bin/nmon',
	#					'sudo rm -R ' + download_dir+'nmon/',
	#					'sudo chmod 777 /usr/bin/nmod']
	#nmon.tar_extra_cmd = ['sudo chmod 777 '+ download_dir + 'nmon/nmon_x86_debian8',
	#					'sudo mv ' + download_dir + 'nmon/nmon_x86_debian8 /usr/bin/nmon',
	#					'sudo rm -R ' + download_dir+'nmon/']
	VsiProgrami.append(nmon.program_name)
## WAVEMON #############################################
	global wavemon
	wavemon = NovProgram()
	wavemon.program_name = 'wavemon'					#ime naj bo brez presledkov
	wavemon.description = 'Program za monitoring wireless omrezj'					#neko besedilo za opis
	#wavemon.apt_get_cmd = ''					#ce je kaka komanda prej za narest
	wavemon.apt_get_name = 'wavemon'					#ime za apt-get
	# wavemon.check_version_cmd = ''			#cmd za preverjanje verzije
	# wavemon.deb_package_path = ''				#url ua BED (brez fila)
	# wavemon.deb_package_file = ''				#file za katerikoli sistem
	# wavemon.deb_package_file_32 = ''			#file za 32bit
	# wavemon.deb_package_file_64 = ''			#file za 64bit
	# wavemon.tar_package_path = ''				#url (brez fila)
	# wavemon.tar_package_file = ''				#file za katerikoli sistem
	# wavemon.tar_package_file_32 = ''			#file za 32bit
	# wavemon.tar_package_file_64 = ''			#file za 64bit
	# wavemon.tar_destination = ''				#kam naj od tara.. TAR paket
	# wavemon.tar_extra_cmd = []				#extra commande, ce je se kaj za narest...
	# wavemon.extra_cmd = []					#se ene extra cmd ... ce je se kaj...
	wavemon.program_desktop = ['[Desktop Entry]',
							'Version=1.0',
							'Name=WaveMon',
							'Exec=terminator -e sudo wavemon',
							'Icon=wifi',
							'Terminal=true',
							'Type=Application',
							'Categories=Network;'
							]				#vsebina v program.desktop
	# wavemon.add_path_profile_variable  = '' 
	# wavemon.add_bash_parameter = []			#text ki je za dodat v .bash 
	# wavemon.notes = ''
	VsiProgrami.append(wavemon.program_name)
## Neofetch ####################################################
	global Neofetch
	Neofetch = NovProgram()
	Neofetch.program_name = 'Neofetch'
	Neofetch.description = 'Logo in nekaj podatkov o racunaniku...!'
	Neofetch.apt_get_add_ppa ='add-apt-repository ppa:dawidd0811/neofetch'
	Neofetch.apt_get_cmd = ''
	Neofetch.apt_get_name ='neofetch'
	Neofetch.check_version_cmd = 'neofetch'
	Neofetch.notes = 'Notes... to do...'
	VsiProgrami.append(Neofetch.program_name)
## Fortune #####################################################
	global Fortune
	Fortune = NovProgram()
	Fortune.program_name = 'Fortune'
	Fortune.description = 'Znani reki in pregovori...'
	Fortune.apt_get_name ='fortune-mod'
	Fortune.check_version_cmd = 'fortune -v'
	Fortune.deb_package_path = ''
	Fortune.deb_package_file = ''
	VsiProgrami.append(Fortune.program_name)
## COWSAY ######################################################
	global Cowsay
	Cowsay = NovProgram()
	Cowsay.program_name = 'Cowsay'
	Cowsay.description = 'To do...'
	Cowsay.apt_get_name ='cowsay'
	Cowsay.check_version_cmd = 'cowsay -help'
	Cowsay.deb_package_path = ''
	Cowsay.deb_package_file = ''
	Cowsay.notes = 'V terminatorju nastavite:\nPreferences -> Profiles -> Command\ncustom command: [ neofetch;fortune|cowsay;bash ]'
	VsiProgrami.append(Cowsay.program_name)
## Keymap ######################################################
	global Keymap
	Keymap = NovProgram()
	Keymap.description='remap tipke [dz] v "/"'
	Keymap.program_name = 'Keymap'
	Keymap.add_bash_parameter = ['\n #remap tipko [dz] - "/"','\n xmodmap -e "keycode 35 = slash"']			#text ki je za dodat v .bash 
	VsiProgrami.append(Keymap.program_name)
## LibreOffice #################################################
	global LibreOffice
	LibreOffice = NovProgram()
	LibreOffice.program_name = 'LibreOffice'
	LibreOffice.description = 'Office suit for linux and other OS...'
	LibreOffice.apt_get_name =''
	LibreOffice.check_version_cmd = ''
	LibreOffice.deb_package_path_64 = ''
	LibreOffice.deb_package_file_64 = ''
	LibreOffice.tar_package_path_64 = 'http://mirror.ba/tdf/libreoffice/stable/5.3.2/deb/x86_64/'
	LibreOffice.tar_package_file_64 = 'LibreOffice_5.3.2_Linux_x86-64_deb.tar.gz'
	LibreOffice.tar_destination =''
	LibreOffice.tar_extra_cmd = ['sudo dpkg -i '+ download_dir +'LibreOffice_5.3.2.2_Linux_x86-64_deb/DEBS/*.deb']
	LibreOffice.deb_package_path_32 = ''
	LibreOffice.deb_package_file_32 = ''
	VsiProgrami.append(LibreOffice.program_name)
## Thunderbird #################################################
	global Thunderbird
	Thunderbird = NovProgram()
	Thunderbird.program_name = 'Thunderbird'
	Thunderbird.description = 'Postni odjemalec...'
	Thunderbird.apt_get_name ='thunderbird'
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
	# W3M.apt_get_cmd = ''					#ce je kaka komanda prej za narest
	W3M.apt_get_name = 'w3m'					#ime za apt-get
	W3M.check_version_cmd = 'w3m -v'			#cmd za preverjanje verzije
	# W3M.extra_cmd = []					#se ene extra cmd ... ce je se kaj..
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
	# obmenugen.tar_extra_cmd = ['sudo cp '+download_dir+'obmenugen/bin/obmenugen /usr/bin/',
	# 							'obmenugen -p',
	# 							'openbox --reconfigure',
	# 							'rm -R '+download_dir+'obmenugen']				#extra commande, ce je se kaj za narest...
	# obmenugen.notes = 'Najverjetneje boste morali sami urediti tudi nekaj podatkov v:\n'\
	# 					'~/.config/obmenugen/obmenugen.cfg\n'\
	# 					'Kot naprimer kateri terminalni simulator uporabljate in\n'\
	# 					'vas priljubljen urejevalnik besedil...'
	#VsiProgrami.append(obmenugen.program_name)
## conky #######################################################
	global conky
	conky = NovProgram()
	conky.program_name = 'conky'					#ime naj bo brez presledkov
	conky.description = 'Prikaz nekaterih osnovnih podatkov sistema'					#neko besedilo za opis
	conky.apt_get_cmd = ''					#ce je kaka komanda prej za narest
	conky.apt_get_name = 'conky-all'					#ime za apt-get
	conky.extra_cmd = ['mkdir '+user+'/.config/conky',
						'ls -alF '+user+'/.config/conky']					#se ene extra cmd ... ce je se kaj...
	conky.program_desktop = []				#vsebina v program.desktop
	conky.add_path_profile_variable  = '' 
	conky.notes = ''
	VsiProgrami.append(conky.program_name)
## dave's conky ################################################
	global dave_s_conky
	dave_s_conky = NovProgram()
	dave_s_conky.program_name = 'dave_s_conky_v3_cfg'					#ime naj bo brez presledkov
	dave_s_conky.description = 'my conky config file'					#neko besedilo za opis
	dave_s_conky.extra_cmd = ['wget "https://github.com/davidrihtarsic/BunsenLab/raw/master/dave_s_conky.conkyrc" -O ~/.config/conky/dave_s_conky.conkyrc',\
							  'bl-conkyzen']					#se ene extra cmd ... ce je se kaj...
	dave_s_conky.program_desktop = []				#vsebina v program.desktop
	dave_s_conky.add_path_profile_variable  = ''
	dave_s_conky.add_bash_parameter = 	['\n# zazeni conky ob zagomu racunalnika...',
										'\nconky --config='+user+'/.config/conky/dave_s_conky.conkyrc']
	#add to .bashrc file =>'conky -config='+user+'/.config/conky/dave_s_conky.conkyrc' 
	dave_s_conky.notes = ''
	VsiProgrami.append(dave_s_conky.program_name)
## alias ll -> ls -alF #########################################
	global ll
	ll = NovProgram()
	ll.program_name = 'alias ll -> ls -alF'					#ime naj bo brez presledkov
	ll.description = 'priredi ll namesto uporabe ls -alF\n'\
					'nato so direktoriji videti takole:\n'\
					'drwxr-xr-x 31 david david   4096 Apr  5 09:33 ./\n'\
					'drwxr-xr-x  3 root  root    4096 Apr  1 18:08 ../\n'\
					'drwxr-xr-x  3 david david   4096 Apr  3 19:05 Arduino/\n'\
					'drwxr-xr-x  2 david david   4096 Apr  3 19:05 .arduino15/\n'\
					'-rw-r--r--  1 david david      0 Jul 11  2015 .bash_aliases\n'
					#neko besedilo za opis
	ll.add_bash_parameter = ['\n#alias',"\nalias ll='ls -alF'"]			#text ki je za dodat v .bash 
	ll.notes = ''
	VsiProgrami.append(ll.program_name)
## GIT #########################################################
	global git
	git = NovProgram()
	git.program_name = 'git'					#ime naj bo brez presledkov
	git.description = 'Protokol za skrbno spremljanje verzij\n'\
					'razvojnih programov.'					#neko besedilo za opis
	git.apt_get_cmd = ''					#ce je kaka komanda prej za narest
	git.apt_get_name = 'git-core'					#ime za apt-get
	#git.check_version_cmd = ''			#cmd za preverjanje verzije
	#git.deb_package_path = ''				#url ua BED (brez fila)
	#git.deb_package_file = ''				#file za katerikoli sistem
	#git.deb_package_file_32 = ''			#file za 32bit
	#git.deb_package_file_64 = ''			#file za 64bit
	#git.tar_package_path = ''				#url (brez fila)
	#git.tar_package_file = ''				#file za katerikoli sistem
	#git.tar_package_file_32 = ''			#file za 32bit
	#git.tar_package_file_64 = ''			#file za 64bit
	#git.tar_destination = ''				#kam naj od tara.. TAR paket
	#git.tar_extra_cmd = []				#extra commande, ce je se kaj za narest...
	#git.extra_cmd = []					#se ene extra cmd ... ce je se kaj...
	#git.program_desktop = []				#vsebina v program.desktop
	#git.add_path_profile_variable  = '' 
	#git.add_bash_parameter = []			#text ki je za dodat v .bash 
	git.notes = ''
	VsiProgrami.append(git.program_name)
## Java 8 ######################################################
	global java_8
	java_8 = NovProgram()
	java_8.program_name = 'java8'					#ime naj bo brez presledkov
	java_8.description = ''					#neko besedilo za opis
	# java_8.apt_get_cmd = ''					#ce je kaka komanda prej za narest
	# java_8.apt_get_name = ''					#ime za apt-get
	java_8.check_version_cmd = 'java -version'			#cmd za preverjanje verzije
	# java_8.deb_package_path = ''				#url ua BED (brez fila)
	# java_8.deb_package_file = ''				#file za katerikoli sistem
	# java_8.deb_package_file_32 = ''			#file za 32bit
	# java_8.deb_package_file_64 = ''			#file za 64bit
	# java_8.tar_package_path = ''				#url (brez fila)
	# java_8.tar_package_file = ''				#file za katerikoli sistem
	# java_8.tar_package_file_32 = ''			#file za 32bit
	# http://download.oracle.com/otn-pub/java/jdk/8u121-b13/e9e7ea248e2c4826b92b3f075a80e441/jre-8u121-linux-x64.tar.gz
	# asdf 
	java_8.tar_package_path_64 = 'http://javadl.oracle.com/webapps/download/'				#url (brez fila)
	java_8.tar_package_file_64 = 'AutoDL?BundleId=218823_e9e7ea248e2c4826b92b3f075a80e441'			#file za 64bit
	java_8.tar_destination = '/usr/lib/jvm/'				#kam naj od tara.. TAR paket
	java_8.extra_cmd = ['sudo update-alternatives --install /usr/bin/java java /usr/lib/jvm/jre1.8.0_121/bin/java 1',
						'sudo update-alternatives --config java']					#se ene extra cmd ... ce je se kaj...
	# java_8.program_desktop = []				#vsebina v program.desktop
	# java_8.add_path_profile_variable  = '' 
	# java_8.add_bash_parameter = []			#text ki je za dodat v .bash 
	# java_8.notes = ''
	VsiProgrami.append(java_8.program_name)
## SmartGIT ####################################################
	global smartGit
	smartGit = NovProgram()
	smartGit.program_name = 'smartgit'					#ime naj bo brez presledkov
	smartGit.description = 'Git GUI client'					#neko besedilo za opis
	# smartGit.apt_get_cmd = ''					#ce je kaka komanda prej za narest
	# smartGit.apt_get_name = ''					#ime za apt-get
	# smartGit.check_version_cmd = ''			#cmd za preverjanje verzije
	# smartGit.deb_package_path = ''				#url ua BED (brez fila)
	# smartGit.deb_package_file = ''				#file za katerikoli sistem
	# smartGit.deb_package_file_32 = ''			#file za 32bit
	# smartGit.deb_package_file_64 = ''			#file za 64bit
	smartGit.tar_package_path = 'https://www.syntevo.com/static/smart/download/smartgit/'				#url (brez fila)
	smartGit.tar_package_file = 'smartgit-linux-17_0_3.tar.gz'				#file za katerikoli sistem
	# smartGit.tar_package_file_32 = ''			#file za 32bit
	# smartGit.tar_package_file_64 = ''			#file za 64bit
	smartGit.tar_destination = opt_dir				#kam naj od tara.. TAR paket
	# smartGit.tar_extra_cmd = []				#extra commande, ce je se kaj za narest...
	smartGit.extra_cmd = ['sudo ln -s /opt/smartgit/bin/smartgit.sh /usr/bin/smartgit']					#se ene extra cmd ... ce je se kaj...
	smartGit.program_desktop = ['[Desktop Entry]',
							'Version=1.0',
							'Name=SmartGit',
							'Exec=smartgit',
							'Icon=/opt/smartgit/bin/smartgit-32.png',
							'Terminal=false',
							'Type=Application',
							'Categories=Development;'
							]					#vsebina v program.desktop
	# smartGit.add_path_profile_variable  = '' 
	# smartGit.add_bash_parameter = []			#text ki je za dodat v .bash 
	# smartGit.notes = ''
	VsiProgrami.append(smartGit.program_name)
## OpenBox menu ################################################
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

Install_programms()

def MakeProgrammsForm():
	global formProgramms
	formProgramms = Form('Izberi program',3,2 ,28,len(VsiProgrami)+4)
	global editPrigramms
	editPrigramms =[]
	for n in range(0, len(VsiProgrami)):
		editPrigramms.append(Edit('(' + str(n+1) + ')', formProgramms.x+3 ,formProgramms.y + n + 2))
		editPrigramms[n].new_value(VsiProgrami[n])
MakeProgrammsForm()

def MakeHelpForm():
	HotKeys = [	'1..16      - Izberi posamezni program',
				'all        - Izberi vse programe',
				'tehnika    - Izbere programe za tehniko:',
				'           Arduino, qCAD, FreeCAD in Sublime',
				'sistem     - Izbere sistemske programe:',
				'           Terminator in Htop',
				'----------------------------------------',
				'ENTER      - Ta zaslon',
				'q - exit',
				]
	formHelp = Form('MENU',40,2,55,formProgramms.dy)
	t_Keys = []
	for n in range(0, len(HotKeys)):
		t_Keys.append(Text(HotKeys[n],formHelp.x+3,formHelp.y+n+2))

# MAIN PROGRAM ##############################################
def Main():
	MakeHelpForm()
	MakeProgrammsForm()
	setCursor(1,formProgramms.y + formProgramms.dy + 4)
	#global editCmd
	#editCmd = Edit('Cmd',1,20)
	#editCmd.value = ''

key = ''
cls()
Main()
#while (editCmd.value != 'q'):
while (key != 'q'):
	key = raw_input('Cmd::')
	programe_index=(i for i in xrange(30))
	programe_index.next()
	if key == '':
		cls()
		Main()
	elif key == str(programe_index.next()):	Update_Upgrade.install()	
	elif key == str(programe_index.next()):	Arduino.install()
	elif key == str(programe_index.next()):	qCAD.install()
	elif key == str(programe_index.next()):	FreeCAD.install()
	elif key == str(programe_index.next()):	Sublime.install()
	elif key == str(programe_index.next()):	Terminator.install()
	elif key == str(programe_index.next()):	Htop.install()
	elif key == str(programe_index.next()):	nmon.install()
	elif key == str(programe_index.next()):	wavemon.install()
	elif key == str(programe_index.next()):	Neofetch.install()
	elif key == str(programe_index.next()):	Fortune.install()
	elif key == str(programe_index.next()):	Cowsay.install()
	elif key == str(programe_index.next()):	Keymap.install()
	elif key == str(programe_index.next()):	LibreOffice.install()
	elif key == str(programe_index.next()):	Thunderbird.install()
	elif key == str(programe_index.next()):	GoogleChrome.install()
	elif key == str(programe_index.next()):	W3M.install()
	elif key == str(programe_index.next()):	Skype.install()
	#elif key == str(programe_index.next()):	obmenugen.install()
	elif key == str(programe_index.next()):	conky.install()
	elif key == str(programe_index.next()):	dave_s_conky.install()
	elif key == str(programe_index.next()):	ll.install()
	elif key == str(programe_index.next()):	git.install()
	elif key == str(programe_index.next()):	java_8.install()
	elif key == str(programe_index.next()):	smartGit.install()
	elif key == str(programe_index.next()):	obmenu.install()
	#elif key == 'str(programe_index.next()):	.install()
	elif key == 'all':
		Update_Upgrade.install()	
		Arduino.install()
		qCAD.install()
		FreeCAD.install()
		Sublime.install()
		Terminator.install()
		Htop.install()
		nmon.install()
		Neofetch.install()
		Fortune.install()
		Cowsay.install()
		Keymap.install()
		LibreOffice.install()
		Thunderbird.install()
		GoogleChrome.install()
		W3M.install()
		Skype.install()
		#obmenugen.install()
		conky.install()
		dave_s_conky.install()
		ll.install()
		git.install()
		java_8.install()
		smartGit.install()
		obmenu.install()
	elif key == 'tehnika':	
		Arduino.install()
		qCAD.install()
		FreeCAD.install()
		Sublime.install()
	elif key == 'sistem':
		Update_Upgrade.install()	
		Terminator.install()
		Htop.install()
		nmon.install()
	else:	
		os.system(key)
	#Main()
			
cls()
