import os

class MainClass():
	def __init__(self, datafolder_path):
		self.datafolder_path = datafolder_path
		try:
			SAFE_folder = os.path.basename(os.path.normpath(self.datafolder_path))
			if len(str(SAFE_folder)) == 65 and SAFE_folder.endswith('.SAFE') == True:
				print('Given folder path is correct and ready to use.')
			else:
				print('Warning! Edited folder path has been given.')
				exit()
		except SyntaxError:
			print('Not a valid datapath.')