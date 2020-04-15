import time
from math import pi
import numpy as np
import socket

import waypoints as wp
import kg_robot as kgr
import orange as ora
import sim


def main():
    print("------------Configuring Burt-------------\r\n")
    burt = kgr.kg_robot(host="127.0.0.1",port=30010,db_host="127.0.0.5",sim_port=19997)
    #burt = kgr.kg_robot(port=30010,ee_port="COM32",db_host="192.168.1.51")
    print("----------------Hi Burt!-----------------\r\n\r\n")

    try:
        while 1:
            ipt = input("cmd: ")
            if ipt == 'close':
                break
            elif ipt == 'home':
                burt.home()

            # sim
            elif ipt == 't':
                burt.translatel_rel([0,0,0.1])
            elif ipt == 'c':
                burt.sim.check(burt.sim.sim_joints)
            elif ipt == 'o':
                ora.orange(burt)

            else:
                var = int(input("var: "))
                burt.serial_send(ipt,var,True)

        
    finally:
        print("Goodbye")
        burt.close()
if __name__ == '__main__': main()
