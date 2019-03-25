# -*- coding: utf-8 -*-

import os

from time import sleep

import python_bitbankcc



class pycolor:

    BLACK = '\033[30m'

    RED = '\033[31m'

    GREEN = '\033[32m'

    YELLOW = '\033[33m'

    BLUE = '\033[34m'

    PURPLE = '\033[35m'

    CYAN = '\033[36m'

    WHITE = '\033[37m'

    END = '\033[0m'

    BOLD = '\038[1m'

    UNDERLINE = '\033[4m'

    INVISIBLE = '\033[08m'

    REVERCE = '\033[07m'



pub = python_bitbankcc.public()



while 1:

	value = pub.get_depth('xrp_jpy')

	value1 = pub.get_ticker('xrp_jpy')

	a1 = sorted([list(map(float,a)) for a in value['bids']])

	a2 = sorted([list(map(float,a)) for a in value['asks']],reverse=True)

	os.system('clear')

	c1 = pycolor.GREEN+'”ƒ'+pycolor.END

	c2 = pycolor.RED+'”„'+pycolor.END

	for i1,i2 in zip(a1,a2):

		b1='{0:<8.3f}{1:>12.4f}'.format(i1[0],i1[1])

		s1='{0:<8.3f}{1:>12.4f}'.format(i2[0],i2[1])	

                if i1[1] >= 10000:

                        b1=pycolor.CYAN+b1+pycolor.END

                if i2[1] >= 10000:

                        s1=pycolor.YELLOW+s1+pycolor.END

		print(c1+b1+' '+c2+s1)

	print "last:%s low:%s hig:%s" % (value1['last'],value1['low'],value1['high'])

	sleep(1)

