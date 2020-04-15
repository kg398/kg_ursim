import time
import copy

import sim
from math import pi

class kg_robot_sim():
    def __init__(self, robot, host="127.0.0.1", port=19997):
        self.robot = robot
        self.sim_joints = [0, 0, 0, 0, 0, 0]
        sim.simxFinish(-1)  # just in case, close all opened connections
        self.clientID = sim.simxStart(host, port, True, True, 5000, 5)  # Connect to CoppeliaSim
        if self.clientID != -1:
            print('Connected to remote API server')
        else:
            print("coppeliasim connection failed")
            return

        res, objs = sim.simxGetObjects(self.clientID, sim.sim_handle_all, sim.simx_opmode_blocking)
        if res == sim.simx_return_ok:
            print('Number of objects in the scene: ', len(objs))
        else:
            print('Remote API function call returned with error code: ', res)

        self.jh = [0,0,0,0,0,0]
        for i in range(6):
            res, self.jh[i]=sim.simxGetObjectHandle(self.clientID,'UR5_joint{}'.format(i+1),sim.simx_opmode_blocking)

        sim.simxStartSimulation(self.clientID, sim.simx_opmode_oneshot)

    def close(self):
        sim.simxAddStatusbarMessage(self.clientID, 'Goodbye CoppeliaSim!', sim.simx_opmode_oneshot)
        sim.simxGetPingTime(self.clientID)
        sim.simxStopSimulation(self.clientID, sim.simx_opmode_oneshot)
        time.sleep(2)
        sim.simxFinish(self.clientID)

    def update(self, prog):
        s_prog = prog[1:-2].split(",")
        cmd = int(s_prog[0])
        pose = [float(s_prog[1]),float(s_prog[2]),float(s_prog[3]),float(s_prog[4]),float(s_prog[5]),float(s_prog[6])]
        acc = float(s_prog[7])
        vel = float(s_prog[8])
        t = float(s_prog[9])
        r = float(s_prog[10])
        w = bool(s_prog[11])


        if cmd==0: # joint move cartesian space
            old_joints = self.robot.getj()
            joints = self.robot.get_inverse_kin(pose)
            dj = [0,0,0,0,0,0]
            for i in range(6):
                dj[i] = abs(old_joints[i]-joints[i])
            timestep = max(dj)/vel/100

            pose_list = []
            for i in range(100):
                pose_list.append(self.joint_inter(old_joints,joints,(i+1)/100))
                self.update_joints(pose_list[i])
                time.sleep(timestep)
            self.check(joints)
        elif cmd==2: # linear move cartesian space
            old_pose = self.robot.getl()
            dl = [0,0,0,0,0,0]
            for i in range(6):
                dl[i] = abs(old_pose[i]-pose[i])
            timestep = max(dl)/vel/100

            pose_list = []
            for i in range(100):
                pose_list.append(self.robot.get_inverse_kin(self.joint_inter(old_pose,pose,(i+1)/100)))
                self.update_joints(pose_list[i])
                time.sleep(timestep)
            self.check(pose_list[-1])
        elif cmd==1:# joint move joint space
            old_joints = self.robot.getj()
            dj = [0, 0, 0, 0, 0, 0]
            for i in range(6):
                dj[i] = abs(old_joints[i] - pose[i])
            timestep = max(dj) / vel / 100

            pose_list = []
            for i in range(100):
                pose_list.append(self.joint_inter(old_joints, pose, (i + 1) / 100))
                self.update_joints(pose_list[i])
                time.sleep(timestep)
            self.check(pose)
        elif cmd==3:# tool move
            pose = self.robot.get_pose_trans(pose)
            joints = self.robot.get_inverse_kin(pose)
            self.update_joints(joints)
            self.check(joints)

    def joint_inter(self, start, end, alpha):
        int_pos = [0,0,0,0,0,0]
        for i in range(6):
            int_pos[i] = start[i]+alpha*(end[i]-start[i])
        return int_pos

    def update_joints(self, joints, acc=0.5,vel=0.1):
        joints_copy = copy.deepcopy(joints)
        joints_copy[1]+=pi/2
        joints_copy[3]+=pi/2
        # dj = [0, 0, 0, 0, 0, 0]
        # for i in range(6):
        #     res, self.sim_joints[i] = sim.simxGetJointPosition(self.clientID,self.jh[i],sim.simx_opmode_streaming)
        #     dj[i] = abs(joints_copy[i] - self.sim_joints[i])
        #
        # self.sim_joints[1] -= pi / 2
        # self.sim_joints[3] -= pi / 2
        #
        # max_dj = max(dj)
        # j_vel = [0,0,0,0,0,0]
        # for i in range(6):
        #     j_vel[i] = 0.5*dj[i]/max_dj
        #     res = sim.simxSetJointTargetVelocity(self.clientID, self.jh[i], j_vel[i], sim.simx_opmode_streaming)

        sim.simxPauseCommunication(self.clientID, True)
        for i in range(6):
            res = sim.simxSetJointTargetPosition(self.clientID, self.jh[i], joints_copy[i], sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(self.clientID, False)

    def check(self,pose):
        joints_error = [0,0,0,0,0,0]
        for i in range(6):
            res, self.sim_joints[i] = sim.simxGetJointPosition(self.clientID,self.jh[i],sim.simx_opmode_streaming)

        self.sim_joints[1]-=pi/2
        self.sim_joints[3]-=pi/2

        for i in range(6):
            joints_error[i] = pose[i] - self.sim_joints[i]

        print(joints_error)
        return joints_error