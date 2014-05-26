import csv
import requests

senate_csv = 'http://www.aph.gov.au/~/media/03%20Senators%20and%20Members/Address%20Labels%20and%20CSV%20files/allsenstate.csv'
house_csv = 'http://www.aph.gov.au/~/media/03%20Senators%20and%20Members/Address%20Labels%20and%20CSV%20files/SurnameRepsCSV.csv'

vic_council_csv = 'http://www.parliament.vic.gov.au/members/list?f=csv&labels=EO-DL14&d=n&d=h&d=s&d=k&d=1&d=0&d=o&d=e&d=p&d=m&d=a&d=t&d=f&d=b&d=A&d=T&d=F&d=w&d=M&house=MLC&gender=&port=&up=YYYY-MM-DD'
vic_assembly_csv = 'http://www.parliament.vic.gov.au/members/list?f=csv&labels=EO-DL14&d=n&d=h&d=s&d=k&d=1&d=0&d=o&d=e&d=p&d=m&d=a&d=t&d=f&d=b&d=A&d=T&d=F&d=w&d=M&house=MLA&gender=&port=&up=YYYY-MM-DD'

class Data(object):
	def __init__(self, link):
		self.link = link
		self.data_fields = self.getData()
		self.headers = self.getHeaders()
		self.data = self.processData()
	def getData(self):
		csvfile = requests.get(self.link, stream=True)
		reader = csv.reader(csvfile.raw)
		header = reader.next()
		return { 'header' : header, 'rows' : reader }
	def getHeaders(self):
		return self.data_fields['header']
	def processData(self):
		members = []
		for row in self.data_fields['rows']:
			members.append(dict(zip(self.data_fields['header'], row)))
		return members

class Senate(Data):
	def field_map(self):
		members = []
		for row in self.data:
			members.append( {
				'first_name' : row['First Name'],
				'second_name' : row['Surname'],
				'Electorate' : row['State'],
				'job' : row['Parliamentary Title'],
				'Party' : row['Political Party'],
				'twitter' : '',
				'website' : '',
				'Address' : {
						'address' : row['ElectorateAddressLine1'] + '\n' + \
						row['ElectorateAddressLine2'] + '\n' + \
						row['ElectorateSuburb'] + '  ' + row['ElectorateState'] + '  ' + row['ElectoratePostCode']
						#, 'ElectorateTelephone', 'ElectorateFax', 'ElectorateTollFree', 'ElectoratePostAddress', 'ElectoratePostSuburb', 'ElectoratePostState', 'ElectoratePostPostCode''
				}
			} )
		return members

senate = Senate(senate_csv)
print senate.headers

# house = Data(house_csv)
# for row in house.data:
# 	print row
#
# vic_council = Data(vic_council_csv)
# for row in vic_council.processData():
# 	print row
#
# vic_assembly = Data(vic_assembly_csv)
# for row in vic_assembly.processData():
# 	print row['Electorate']
