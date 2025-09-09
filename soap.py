import zeep

wsdl = 'https://172.25.32.31:21032/?wsdl=SetCardStatusRq'
client = zeep.Client(wsdl=wsdl)


data = '''
<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
	<SOAP-ENV:Header>
		<cpi:RequestHeader xmlns:cpi="http://schemas.compassplus.com/twcms/1.0/omsi.xsd">
		<Cpimode timeout="20">Sync</Cpimode>
			<Branch>1</Branch>
			<Station>905</Station>
			<RType>Do</RType>
		</cpi:RequestHeader>
	</SOAP-ENV:Header>
	<SOAP-ENV:Body>
		<cpi:Request xmlns:cpi="http://schemas.compassplus.com/twcms/1.0/omsi.xsd">
			<Request>
				<Transaction>
				<CARD PAN="4391330000536581" MBR="0">
					 <Command Action="Update"/>
					 <STATUSFO>4</STATUSFO>
					 <STATUSBO>1</STATUSBO>
				</CARD>
				</Transaction>
			</Request>
		</cpi:Request>
	</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
'''