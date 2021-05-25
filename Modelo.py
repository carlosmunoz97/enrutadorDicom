# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 15:39:06 2020

@author: Carlos Jose Munoz
"""
import pydicom as dcm
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2

class dicom:
    def __init__(self): #atributos iniciales
        self.changepage=0 #saber en que pagina se encuentra
        self.archivo='' #archivo que se está manejando (ruta)
    
    def ventana(self, r): #modifica la ventana en la que se encuentra
        self.changepage=r
    
    def recibirruta(self, archivo):#recibe la ruta y la asigna al archivo
        self.archivo=archivo
        image=[]
        if self.changepage==2:
            image= Image.open(self.archivo)
            image=np.array(image)
        return image

    def conv(self, saved,file,name,sex,estudio,medico,serie,date_estudio,time_estudio,id_paciente,nacimiento): #convierte imagen a DICOM y le asigna los valores ingresados
        
        
        
        saved=saved+'/'+file+'.dcm'
        cmd='img2dcm.exe "'+self.archivo+'" "'+saved+'"' #uso del dcmtk
        os.system(cmd)
        
        dataset=dcm.dcmread(saved)
        
        pname=dataset[0x0010,0x0010]
        pname.value=name
        
        psex=dataset[0x0010,0x0040]
        psex.value=sex
        
        
        pestudio=dataset[0x0020,0x0010]
        pestudio.value=estudio
        
        
        pmedico=dataset[0x0008,0x0090]
        pmedico.value=medico
        
        
        pserie=dataset[0x0020,0x0011]
        pserie.value=serie
        
        
        pdate_estudio=dataset[0x0008,0x0020]
        pdate_estudio.value=date_estudio
        
        
        ptime_estudio=dataset[0x0008,0x0030]
        ptime_estudio.value=time_estudio
        
        pid_paciente=dataset[0x0010,0x0020]
        pid_paciente.value=id_paciente
        
        
        pnacimiento=dataset[0x0010,0x0030]
        pnacimiento.value=nacimiento
        
        dataset.save_as(saved) #guarda los datos sobre el archivo
    
    def datos(self): #devuelve los datos del DICOM para mostrar en la interfaz
        dataset=dcm.dcmread(self.archivo)
        
        file=os.path.basename(self.archivo)
        file=os.path.splitext(file)[0]
        
        name=dataset.PatientName
        id_paciente=dataset.PatientID    
        date_estudio=dataset.StudyDate
        time_estudio=dataset.StudyTime
        medico=dataset.ReferringPhysicianName
        nacimiento=dataset.PatientBirthDate
        sex=dataset.PatientSex
        estudio=dataset.StudyID
        serie=dataset.SeriesNumber
        
        direct=os.path.dirname(self.archivo)
        numero=len(glob.glob(direct+"/*"))
        lista=glob.glob(direct+"/*")
        self.elementos=[]
        for i in lista:
            b=os.path.splitext(os.path.basename(i))[0]
            self.elementos=np.append(self.elementos,b)
        elemento=int(np.where(self.elementos==file)[0])
        return file, name, sex, estudio, medico, serie, date_estudio, time_estudio, id_paciente, nacimiento,numero,elemento
    
    def graph(self): #grafica los planos 
        files = []
        direct=os.path.dirname(self.archivo)
        for fname in glob.glob(str(direct)+"**/*.dcm", recursive=False):
            files.append(dcm.dcmread(fname))
            
        ref = dcm.read_file(self.archivo)
        self.__rows = int(ref.Rows);
        self.__columns = int(ref.Columns);
        self.__slices = len(files);
        self.__x_space = float(ref.PixelSpacing[0]);
        self.__y_space = float(ref.PixelSpacing[1]);
        self.__thickness = float(ref.SliceThickness);   
        self.__data = np.zeros((self.__rows, self.__columns, self.__slices), 
                               dtype=ref.pixel_array.dtype);
                               
        self.__patient_name = ref.PatientName;
        # print(self.__patient_name);                       
        # loop through all the DICOM files
        counter = 0
        for fname in glob.glob(str(direct)+"**/*.dcm", recursive=False):
            # files.append(dcm.dcmread(fname))
        # for filenameDCM in file:
        #     # read the file
            ds = dcm.read_file(fname)
            # store the raw image data
            self.__data[:, :, counter] = ds.pixel_array;
            counter = counter + 1; 
        return self.__data  
        
    
    def graph_una(self, elemento): #grafica el archivo que se está mirando 
        imgdcm=self.elementos[elemento]
        dataset=dcm.dcmread(os.path.dirname(self.archivo)+"/"+imgdcm+".dcm")
        pixel_array=dataset.pixel_array
        
        return pixel_array,imgdcm
    
    def graf(self, data, rot):
        (h,w)=data.shape[:2]
        center = (w / 2, h / 2)
        
        if rot==0:
            devolver=data
            
        elif rot==1:
            M = cv2.getRotationMatrix2D(center, 90, 1.0)        
            devolver = cv2.warpAffine(data, M, (h, w))
        
        elif rot==2:# 180 grados
            M = cv2.getRotationMatrix2D(center, 180, 1.0)
            devolver = cv2.warpAffine(data, M, (w, h))
     
        elif rot==3:# 270 grados
            M = cv2.getRotationMatrix2D(center, 270, 1.0)
            devolver= cv2.warpAffine(data, M, (h, w))
        
        return devolver