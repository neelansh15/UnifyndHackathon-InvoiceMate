import boto3
import getbill as gbill

# Document
s3BucketName = "invoice-storage-unifyed"
documentName = "Screenshot20200307135515ScanbotSDKExampleFlutterpng"

# Amazon Textract client
textract = boto3.client('textract')

# Call Amazon Textract
response = textract.detect_document_text(
    Document={
        'S3Object': {
            'Bucket': s3BucketName,
            'Name': documentName
        }
    })

#print(response)

# Print text
# print("\nText\n========")
text = ""
for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        # print ('\033[94m' +  item["Text"] + '\033[0m')
        text = text + " " + item["Text"]

# Amazon Comprehend client
comprehend = boto3.client('comprehend')

# Detect entities
titles = []
organization = ""
other_orgs = []
org_highest = 0
locations = []
quantities = []
other = []
date = []
people = []
commercial_items = []

#Special
invoice_number = []

entities =  comprehend.detect_entities(LanguageCode="en", Text=text)
print("\nEntities\n========")
for entity in entities["Entities"]:
    # print ("{}\t=>\t{}".format(entity["Type"], entity["Text"]))
    if entity["Type"] == "ORGANIZATION":

        # Include only the organization with the highest score
        if entity["Score"] > org_highest:
            org_highest = entity["Score"]
            organization = entity["Text"]
        
        if entity["Score"] > 0.5 and entity["Score"] < 0.8:
            other_orgs.append(entity["Text"])
    
    elif entity["Type"] == "LOCATION":
        if entity["Score"] > 0.3:
            locations.append(entity["Text"])
    elif entity["Type"] == "TITLE":
        titles.append(entity["Text"])
    elif entity["Type"] == "QUANTITY":
        if entity["Score"] > 0.4:
            quantities.append(entity) #The Whole Entity
    elif entity["Type"] == "OTHER":
        other.append(entity["Text"])
    elif entity["Type"] == "DATE":
        date.append(entity["Text"])
    elif entity["Type"] == "PERSON":
        people.append(entity["Text"])
    elif entity["Type"] == "COMMERCIAL_ITEM":
        commercial_items.append(entity["Text"])
    

print()
print(organization)

print("\nLocation: \n{}".format("\n".join(locations)))

print()

print("Date: {}".format(",".join(date)))

print()

print("Items: \n{}".format("\n".join(commercial_items)))
print("\n".join(other_orgs))

print()

#TODO: Use Amazon Textract to specifically get the BILL AMOUNT, using Key:Value pair thing like I was trying earlier
bill = gbill.main('sample.jpg')
print("Bill Amount: {}".format("".join(bill)))
