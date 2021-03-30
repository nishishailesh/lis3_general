#!/usr/bin/python3
STX=b'\x02'
ETX=b'\x03'
EOT=b'\x04'
ETB=b'\x17'
FS=b'\x1c'
GS=b'\x1d'
RS=b'\x1e'
ACK=b'\x06'

import socket,fcntl,os


def get_checksum(data):
  checksum=0
  for x in data:
    checksum=(checksum+x)
  checksum=checksum%256
  two_digit_checksum_string='{:X}'.format(checksum).zfill(2)
  return two_digit_checksum_string.encode()


magic=b''

id_req=STX+b'ID_REQ'+FS+RS+ETX+get_checksum(STX+b'ID_REQ'+FS+RS+ETX)+EOT
ack_msg=STX+ACK+ETX+get_checksum(STX+ACK+ETX)+EOT
#exit()

pre_smp_req= STX+b'SMP_REQ' +FS+RS+b'aMOD'+GS+b'0500'+GS+GS+GS+FS+b'iIID'+GS+b'45064'+GS+GS+GS+FS+b'rSEQ'+GS+b'4'+GS+GS+GS+FS+RS+ETX
smp_req=pre_smp_req+get_checksum(pre_smp_req)+EOT

pre_time_req=STX+b'TIME_REQ'+FS+RS+b'aMOD'+GS+b'0500'+GS+GS+GS+FS+b'iIID'+GS+b'45064'+GS+GS+GS+FS+RS+ETX
time_req=pre_time_req+get_checksum(pre_time_req)+EOT

#pre_ack=STX+ACK+ETX
#ack=pre_ack+get_checksum(pre_ack)+EOT
pre_id_data=STX+b'ID_DATA'+FS+RS+b'aMOD'+GS+b'LIS'+GS+GS+GS+FS+b'iIID'+GS+b'333'+GS+GS+GS+FS+RS+ETX
id_data=pre_id_data+get_checksum(pre_id_data)+EOT

pre_cal_req= STX+b'CAL_REQ' +FS+RS+b'aMOD'+GS+b'0500'+GS+GS+GS+FS+b'iIID'+GS+b'45064'+GS+GS+GS+FS+b'rSEQ'+GS+b'142'+GS+GS+GS+FS+RS+ETX
cal_req=pre_cal_req+get_checksum(pre_cal_req)+EOT

#msgs=(id_req,ack_msg+id_data,ack_msg,time_req,smp_req,cal_req)
str_msgs='0=id_req,1=id_data,2=ack_msg,,3=time_req,4=smp_req,5=cal_req'

HOST = '12.207.3.200'  # The server's hostname or IP address
PORT = 2578        # The port used by the server
#while True:
#  print(str_msgs)
#  x=input('Enter value:')
#  print('You entered:', x)
#  print(msgs[int(x)])

while True:
  print(str_msgs)
  x,y=input('Enter message and rSEQ:').split()
  
  pre_cal_req= STX+b'CAL_REQ' +FS+RS+b'aMOD'+GS+b'0500'+GS+GS+GS+FS+b'iIID'+GS+b'45064'+GS+GS+GS+FS+b'rSEQ'+GS+bytes(y,'utf-8')+GS+GS+GS+FS+RS+ETX
  cal_req=pre_cal_req+get_checksum(pre_cal_req)+EOT

  pre_smp_req= STX+b'SMP_REQ' +FS+RS+b'aMOD'+GS+b'0500'+GS+GS+GS+FS+b'iIID'+GS+b'45064'+GS+GS+GS+FS+b'rSEQ'+GS+bytes(y,'utf-8')+GS+GS+GS+FS+RS+ETX
  smp_req=pre_smp_req+get_checksum(pre_smp_req)+EOT

  msgs=(id_req,ack_msg+id_data,ack_msg,time_req,ack_msg+smp_req,ack_msg+cal_req)

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('SEND:>>>',msgs[int(x)])
    s.sendall(msgs[int(x)])
    data = s.recv(3024)
  print('RECV:<<<', data)
