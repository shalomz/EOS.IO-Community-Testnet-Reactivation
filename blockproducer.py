import mainConfig
import json
import requests

class BlockProducer:
    def __init__(self, **kwargs):
        self.node_addr=kwargs.get('node_addr')
        self.port_p2p=kwargs.get('port_p2p')
        self.port_http=kwargs.get('port_http')
        self.port_ssl=kwargs.get('port_ssl')
        self.block_signing_key=kwargs.get('block_signing_key')
        self.organisation=kwargs.get('organisation')
        self.account_name=kwargs.get('account_name')
        self.location=kwargs.get('location')

    def setProducerParameters(self,confDic):
        for key in confDic:
            if key in self.__dict__:
                self.__dict__[key] = confDic[key]

    def genP2Pconf(self):
        return "p2p-peer-address = " + ":".join([str(self.node_addr),str(self.port_p2p)])

    def genAddHttpconf(self):
        return ":".join([str(self.node_addr),str(self.port_http)])

    def genBPinfo(self):
        return "|".join([str(self.account_name),str(self.node_addr),str(self.port_http),str(self.port_p2p),str(self.location),str(self.organisation)])


    def getBPjson(self):
        bpdata =   {
                "account_name": str(self.account_name),
                "organisation": str(self.organisation),
                "location": str(self.location),
                "node_addr": str(self.node_addr),
                "port_http": str(self.port_http),
                "port_ssl": str(self.port_ssl),
                "port_p2p": str(self.port_p2p),
                "block_signing_key": str(self.block_signing_key)
                }

        return json.dumps(bpdata, ensure_ascii=False)

    
    def getInfo(self):
        get_info = r'http://' + self.node_addr + ':' + self.port_http + '/'.join(['/v1','chain','get_info'])
        r = requests.get(get_info)
        if r.ok:
            return r.json()
        else:
            return None

class eosNet():
    def __init__(self,producers):
        self.producers = producers



def bP2PFile(fileName,producersParametersList):
    
    with open(fileName,'w') as f:
        for producerParameter in producersParametersList:
            bp = BlockProducer()
            bp.setProducerParameters(producerParameter)
            
            #print(bp.genP2Pconf())
            f.write(bp.genP2Pconf())
            f.write("\n")
    f.close()

def bHttpFile(fileName,producersParametersList):
    producersParametersList = mainConfig.blockProducerList
    with open(fileName,'w') as f:
        for producerParameter in producersParametersList:
            bp = BlockProducer()
            bp.setProducerParameters(producerParameter)
            
            #print(bp.genAddHttpconf())
            f.write(bp.genAddHttpconf())
            f.write("\n")
    f.close()

def bGetInfoFile(fileName,producersParametersList):
    producersParametersList = mainConfig.blockProducerList
    with open(fileName,'w') as f:
        for producerParameter in producersParametersList:
            bp = BlockProducer()
            bp.setProducerParameters(producerParameter)
            
            #print(bp.getInfo())
            json.dump(bp.getInfo(), f, ensure_ascii=False)
            f.write("\n")
    f.close()


def bBPInfoFile(fileName,producersParametersList):
    producersParametersList = mainConfig.blockProducerList
    with open(fileName,'w') as f:
        for producerParameter in producersParametersList:
            bp = BlockProducer()
            bp.setProducerParameters(producerParameter)
            
            #print(bp.getInfo())
            f.write(bp.genBPinfo())
            f.write("\n")
    f.close()

if __name__ == '__main__': 
    prParList = mainConfig.blockProducerList

    fp2p = "testnet_p2p.ini"
    bP2PFile(fp2p,prParList)
    fhttp = "testnet_http.ini"
    bHttpFile(fhttp,prParList)
    #fgetinfo = "testnet_getinfo.ini"
    #bGetInfoFile(fgetinfo,prParList)
    fbpinfo = "testnet_bpinfo.ini"
    bBPInfoFile(fbpinfo,prParList)