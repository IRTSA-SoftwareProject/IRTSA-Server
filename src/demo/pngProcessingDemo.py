# Created on 11/04/2018 edited 30/08/2018
# Example of using the ris_processing package
# @author: James Moran edited by Casper Pikaar

import sys
import asyncio
import ris_processing.image_process_interface

async def printforme(stringtoPrint):
    print(stringtoPrint)
    
#Time variable which has time passed to it from command executing script
time = sys.argv[1]

if __name__ == '__main__':
    ris_processing.image_process_interface.process_image(printforme, 'C:/PNG Dumps/Processing/'+time, 'Final Thermal Hotspot', 0, -1)
    