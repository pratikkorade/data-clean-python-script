# import the mysql client for python
import pymysql
import pandas as pd
import os.path
from os import path,makedirs
import shutil
from PIL import Image

# Create a connection object
dbServerName    = "127.0.0.1"
dbUser          = "root"
dbPassword      = ""
dbName          = "dump-petmate_db-201907131931.sql"
cusrorType      = pymysql.cursors.DictCursor
connectionObject   = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword,
                                     db=dbName,cursorclass=cusrorType)
try:

    # Create a cursor object
    cursorObject = connectionObject.cursor()      

    #get Image from pet_phpto folder
    # SQL query string
    sqlQuery = "SELECT photo as photos FROM pet_photos WHERE photo !='';"
    # Execute the sqlQuery
    cursorObject.execute(sqlQuery)
    #Fetch all the rows
    rows= cursorObject.fetchall()
    pet_photosData = pd.DataFrame(rows) 
    pet_photosData['From'] = 'pet_photos'

    #get primary photo from pets folder
    sqlQuery1 = "SELECT primary_photo as photos FROM `pets` WHERE primary_photo !='';"
    # Execute the sqlQuery
    cursorObject.execute(sqlQuery1)
    #Fetch all the rows
    rows2= cursorObject.fetchall()
    petsData = pd.DataFrame(rows2)
    petsData['From'] = 'primary_photo'

    #get health_certificate photo from pets folder
    healthSqlQuert = "SELECT `health_certificate` as photos  FROM `pets` WHERE health_certificate !='';"
    # Execute the sqlQuery
    cursorObject.execute(healthSqlQuert)
    #Fetch all the rows
    rows3= cursorObject.fetchall()
    healthCertificateData = pd.DataFrame(rows3)
    healthCertificateData['From'] = 'health_certificate'

    #merge pet_phpto , primary photos & health_certificate photos
    pet_primaryPhoto = pet_photosData.append(petsData)
    allImageDF = pet_primaryPhoto.append(healthCertificateData)
    imageExist=[]

    #orignal path of image folder
    originalDIR = '/home/pratik/Desktop/images/'
    #new move path of image folder
    imageMoveDIR = '/home/pratik/Desktop/NewImages/'
    defaultImage = '/home/pratik/Downloads/Alaskan-Malamutes-dogs.jpg'

    def imageThubnail(image,size):
        image.thumbnail((size, size))
        folder = '/500X500/' if size == 500 else '/200X200/'
        if not os.path.exists(NewimagePath.replace("/original", folder)):
            os.makedirs(NewimagePath.replace("/original", folder))
        image.save(NewimagePath.replace("/original", folder)+imagename)
        print(imagename, ' folder' ,folder, ' created')

    for index, row in allImageDF.iterrows():
        # print(type(row['photos']))
        imageFullPath = originalDIR+row['photos']
        print('imageFullPath',imageFullPath)
        newImageFullPath = imageMoveDIR+row['photos']
        print('newImageFullPath',newImageFullPath)
        imagename = imageFullPath.rsplit('/', 1)[-1]
        NewimagePath = newImageFullPath.rsplit('/', 1)[0]
        if(path.exists(imageFullPath)):
            # 200X200 image
            print(3)
            originalImage200 = Image.open(imageFullPath)
            imageThubnail(originalImage200,200)
    
            # 500X500 image
            originalImage500 = Image.open(imageFullPath)
            imageThubnail(originalImage500,500)

            #move original image
            if not os.path.exists(newImageFullPath.rsplit('/', 1)[0]):
                os.makedirs(newImageFullPath.rsplit('/', 1)[0])
            shutil.move(imageFullPath, newImageFullPath.rsplit('/', 1)[0]+'/'+imagename)
            print('file move',imagename)
            imageExist.append(1)
        else:
            if(row['From']=='primary_photo'):
                #original image

                defImage= Image.open(defaultImage)
                if not os.path.exists(NewimagePath):
                    os.makedirs(NewimagePath)
                defImage.save(newImageFullPath)

                # 500X500 image
                defImage500 = Image.open(defaultImage)
                imageThubnail(defImage500,500)

                # 200X200 image
                defImage200 = Image.open(defaultImage)
                imageThubnail(defImage200,200) 
                
            imageExist.append(0)
    # print('find column',imageExist)
    allImageDF['find'] = imageExist 

    # print('final Result',allImageDF)
    # writer = pd.ExcelWriter('final_result.xlsx', engine='xlsxwriter')

    allImageDF.to_excel('final_result.xlsx',sheet_name = 'result') #  engine='xlsxwriter' ,
except Exception as e:

    print("Exeception occured:{}".format(e))

finally:
    connectionObject.close()

 