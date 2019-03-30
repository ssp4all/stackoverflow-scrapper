# -*- coding: utf-8 -*-
import time
from yaspin import yaspin

def loader(res):
	""" Loading function """
	with yaspin(text="Checking... ", color='blue') as sp:
		if res == 0:
			time.sleep(3)
			sp.write('✔ Done')
		else:
			time.sleep(3)
			sp.write('❌ Failed')

# loader()
