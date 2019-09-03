# This program extracts a list of all Sentinel-1 GRD files for the specified lat/lon extent and dates defined in 'TestURL' from the Sentinel-1 Australasia Regional Access data hub (https://copernicus.nci.org.au/sara.client/#/home ). The product type of GRD is defined in 'TestURL'.

# Written by Catherine Ticehurst (CSIRO) 2018/2019. Code adapted from https://github.com/opendatacube/radar

import requests
import os

def quicklook_to_filepath(qlurl):
    fp = "/g/data/fj7/Copernicus/Sentinel-1"+qlurl.split("Sentinel-1")[1].replace(".png",".zip")
    return fp

# SARA URL details providing area of interest, dates, and S1 product. Input the longitude / latitude corner points of area of interest within 'POLYGON(())'

#TestURL = "https://copernicus.nci.org.au/sara.server/1.0/api/collections/S1/search.json?_pretty=1" \
#          "&startDate=2018-09-01&completionDate=2018-10-01&productType=GRD&sensorMode=IW" \
#          "&geometry=POLYGON((150.4 -26.2, 151.5 -26.2, 151.5 -27.0, 150.4 -27.0, 150.4 -26.2))"
		  
#TestURL = "https://copernicus.nci.org.au/sara.server/1.0/api/collections/S1/search.json?_pretty=1" \
#          "&startDate=2016-07-01&completionDate=2016-07-31&productType=GRD&sensorMode=IW" \
#          "&geometry=POLYGON((123.5 -17.5, 124.5 -17.5, 124.5 -18.5, 123.5 -18.5, 123.5 -17.5))"

# McArthur River Mine
TestURL = "https://copernicus.nci.org.au/sara.server/1.0/api/collections/S1/search.json?_pretty=1" \
          "&startDate=2019-06-20&completionDate=2019-08-20&productType=GRD&sensorMode=IW" \
          "&geometry=POLYGON((136.02 -16.36, 136.15 -16.36, 136.15 -16.49, 136.02 -16.49, 136.02 -16.36))"
#TestURL = "https://copernicus.nci.org.au/sara.server/1.0/api/collections/S1/search.json?_pretty=1" \
#          "&startDate=2019-07-01&completionDate=2019-08-20&productType=SLC&sensorMode=IW" \
#          "&geometry=POLYGON((136.02 -16.36, 136.15 -16.36, 136.15 -16.49, 136.02 -16.49, 136.02 -16.36))"

print("TestURL=",TestURL)

filepaths=[]
file_url=[]
SARA_id=[]
TestURL +="&maxRecords=50"
page = 1

r = requests.get(TestURL)
result = r.json()
print("result=",result)
nresult = result["properties"]["itemsPerPage"]
print('nresult=',nresult)

# Read each file name
while nresult>0:
    print("nresult=",nresult)
    #extract list of products (url or filename)
    #filepaths += [i["properties"]["services"]["download"]["url"] for i in result["features"]]
    file_url += [i["properties"]["services"]["download"]["url"] for i in result["features"]]
    filepaths += [quicklook_to_filepath(i["properties"]["quicklook"]) for i in
                  result["features"]]

    # go to next page until nresult=0
    page += 1
    pagedUrl = TestURL + "&page={0}".format(page)
    r = requests.get(pagedUrl)
    result = r.json()
    nresult = result["properties"]["itemsPerPage"]

# write list of S1 filenames into an output text file (provide output filename - including full file path)
# **** Note that the full output filenames are based on their locations within the National Computational Infrastructure. However this
# information is used to create the full filepath for accessing the files on the NCI thredds server ****
print("filepaths =", filepaths[0])

outfile = 'Z:/MRM/S1_filenames_GRD_IW_MRM_wSARAid_lateJunTo20Aug2019.txt'
#outfile = 'Z:/MRM/S1_filenames_SLC_IW_MRM_wSARAid_JulTo20Aug2019.txt'
#outfile = 'Z:/work/cjt/SAR/SAR_Cube/S1_filenames_GRD_IW_Fitzroy_wSARAid.txt'
#outfile = 'Z:/SAR/SAR_Cube/S1_filenames_GRD_IW_Surat_wSARAid.txt'
#outfile = 'C:/Users/tic013/S1_processing/S1_filenames_GRD_IW_Surat_wSARAid.txt'
SARA_id += [file_url[i].split('/')[len(file_url[i].split('/'))-2] for i in range(len(file_url))]
with open(outfile,'w') as op:
    #op.writelines(map(lambda x: x + '\n', filter(None,filepaths)))
    op.writelines(map(lambda x, y: x + ', ' + y + '\n', filter(None,filepaths), filter(None,SARA_id)))

