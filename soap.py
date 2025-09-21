# import zeep

# wsdl = 'https://172.25.32.31:12349/?wsdl=SetCardStatusRq'
# client = zeep.Client(wsdl=wsdl)
# print(client)

from zeep import Client

wsdl_url = "https://udcvdvscuat1.ucb.com.bd:8119/UCBIVRService.svc?singlewsdl"
client = Client(wsdl_url)

# Open a file in write mode
with open("wsdl_doc.txt", "w", encoding="utf-8") as f:
    for service in client.wsdl.services.values():
        f.write(f"Service: {service.name}\n")
        for port in service.ports.values():
            f.write(f"  Port: {port.name}\n")
            for op in port.binding._operations.values():
                f.write(f"    Operation: {op.name}\n")
                f.write(f"      Input: {op.input.signature()}\n")
                f.write(f"      Output: {op.output.signature()}\n")
        f.write("\n")  # add spacing between services




# data = '''
# <?xml version="1.0" encoding="UTF-8"?>
# <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
# 	<SOAP-ENV:Header>
# 		<cpi:RequestHeader xmlns:cpi="http://schemas.compassplus.com/twcms/1.0/omsi.xsd">
# 		<Cpimode timeout="20">Sync</Cpimode>
# 			<Branch>1</Branch>
# 			<Station>905</Station>
# 			<RType>Do</RType>
# 		</cpi:RequestHeader>
# 	</SOAP-ENV:Header>
# 	<SOAP-ENV:Body>
# 		<cpi:Request xmlns:cpi="http://schemas.compassplus.com/twcms/1.0/omsi.xsd">
# 			<Request>
# 				<Transaction>
# 				<CARD PAN="4391330000536581" MBR="0">
# 					 <Command Action="Update"/>
# 					 <STATUSFO>4</STATUSFO>
# 					 <STATUSBO>1</STATUSBO>
# 				</CARD>
# 				</Transaction>
# 			</Request>
# 		</cpi:Request>
# 	</SOAP-ENV:Body>
# </SOAP-ENV:Envelope>
# '''