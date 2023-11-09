import hashlib,socket,base64,time
from cachehandler import retrieve_data_from_memcached

def sendto_destincation(identifier:str,dest,port,start=1):
    time.sleep(5)
    while True:
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.settimeout(25)
            s.connect((dest,int(port)))
            data=retrieve_data_from_memcached(f"{identifier}_{start}")
            if data:
               
                decodeddata=base64.b85decode(data)
                hashh=hashlib.md5(decodeddata).hexdigest()
                s.sendall(decodeddata)
                start+=1
                #recvhash=s.recv(512)

                #if recvhash.decode==hashh:
                #    start+=1
                #    continue
            else:
                s.close()
                break

        