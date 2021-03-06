"""

CODE ADAPTED FROM:

(C) Copyright 2009 Igor V. Custodio

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""


from ISO8583.ISO8583 import ISO8583
from ISO8583.ISOErrors import *
from socket import *

import os

os.system(['clear','cls'][os.name == 'nt'])

# Configure the server
serverIP = "localhost" 
serverPort = 8583
maxConn = 5
bigEndian = True
#bigEndian = False


# Create a TCP socket
s = socket(AF_INET, SOCK_STREAM)    
# bind it to the server port
s.bind((serverIP, serverPort))   
# Configure it to accept up to N simultaneous Clients waiting...
s.listen(maxConn)                        


# Run forever
while 1:
        #wait new Client Connection
        connection, address = s.accept() 
        while 1:
                # receive message
                isoStr = connection.recv(2048) 
                if isoStr:
                        print ("\nInput ASCII |%s|" % isoStr)
                        pack = ISO8583()
                        #parse the iso
                        try:
                                if bigEndian:
                                        pack.setNetworkISO(isoStr)
                                else:
                                        pack.setNetworkISO(isoStr,False)
                        
                                v1 = pack.getBitsAndValues()
                                for v in v1:
                                        print ('Bit %s of type %s with value = %s' % (v['bit'],v['type'],v['value']))
                                        
                                if pack.getMTI() == '2100':
                                        print ("Authorization request received \n")
                                
                                elif pack.getMTI() == '2200':
                                        print ("Request funds received \n")
                                
                                else:
                                        print ("The client sent an invalid message!")  
                                        break
                                        
                                        
                        except InvalidIso8583, ii:
                                print (ii)
                                break
                        except:
                                print ('Something happened!!!!')
                                break
                        
                        #send answer
                        if pack.getMTI() == '2100':
							pack.setMTI('2110')
                        
                        elif pack.getMTI() == '2200':
							pack.setMTI('2210')
                        
                        if bigEndian:
                                ans = pack.getNetworkISO()
                        else:
                                ans = pack.getNetworkISO(False)
                                
                        print ('Sending answer %s' % ans)
                        connection.send(ans)
                        
                else:
                        break
        # close socket          
        connection.close()             
        print ("Closed...")
