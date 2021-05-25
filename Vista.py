# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 15:39:57 2020

@author: Carlos Jose Munoz
"""

from PyQt5.QtWidgets import QMainWindow,QMessageBox,QDialog,QFileDialog,QSlider,QCheckBox
import PyQt5.QtGui
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIntValidator, QMouseEvent
import numpy as np;
import pyqtgraph as pg;


class ventanaUno (QDialog): #venatana de inicio para escoger que se desea hacer 
    def __init__(self): #abre la ventana inicial 
        super(ventanaUno, self).__init__();
        loadUi('inicio.ui',self)
        self.setup();

    def setup(self): #define los procesos que se realizaran si se presiona uno u otro boton conectandolo con su respectiva función  
        self.cargar.clicked.connect(self.carga);
        self.convertir.clicked.connect(self.conver);
        
    def asignarcontrolador(self, c):# se crea el enlace entre esta ventana y el controlador 
        self.__mi_controlador = c
        
    def carga(self):#abre la ventana para carga
        self.__mi_controlador.ventana(1)
        
    def conver(self):#abre la ventana para convertir 
        self.__mi_controlador.ventana(2)
                
        
class ventanaDos(QMainWindow): #Ventana para carga de archivos DICOM
    def __init__(self): #rutina para inicio de la ventana 
        super (ventanaDos,self).__init__();
        loadUi('carga.ui',self)
        self.setup();
        
    def setup (self): #define las funciones según cada btn y los aspectos iniciales
        
        
        self.limpiarcampos() #limpia los campos
        self.gra.ui.histogram.hide() #quita la opción del histograma
        self.gra.ui.roiBtn.hide()#quita la opción del roi
        self.gra.ui.menuBtn.hide()#quita la opción del menu
        self.gra_2.ui.histogram.hide()
        self.gra_2.ui.roiBtn.hide()
        self.gra_2.ui.menuBtn.hide()
        self.gra_3.ui.histogram.hide()
        self.gra_3.ui.roiBtn.hide()
        self.gra_3.ui.menuBtn.hide()
        self.gra_4.ui.histogram.hide()
        self.gra_4.ui.roiBtn.hide()
        self.gra_4.ui.menuBtn.hide()
        self.h_1.setCheckState(2)#limpia la opción del histograma
        self.h_2.setCheckState(2)
        self.h_3.setCheckState(2)
        self.h_1.stateChanged.connect(self.histogram_1)
        self.h_2.stateChanged.connect(self.histogram_2)
        self.h_3.stateChanged.connect(self.histogram_3)
        self.verticalSlider.valueChanged[int].connect(self.slider_cambio)
        self.verticalSlider_2.valueChanged[int].connect(self.slider_cambio_2)
        self.verticalSlider_3.valueChanged[int].connect(self.slider_cambio_3)
        
        self.cargar.clicked.connect(self.charge);#define la funcion de cargar
        self.examinar.clicked.connect(self.examin); #define la funcion de examinar
        self.graficar.clicked.connect(self.graph);#define la funcion  de graficar 
        self.dcmarchivo=0
        self.n=0;
        self.elemento=0
        self.btn_anterior.clicked.connect(self.graph_anterior);#define la función del boton 
        self.btn_siguiente.clicked.connect(self.graph_siguiente);#define la función del boton 
        self.pos_1=0
        self.pos_2=0
        self.pos_3=0
        self.rot_1=0
        self.rot_2=0
        self.rot_3=0
        self.btn_anterior_2.clicked.connect(self.anterior_2)
        self.btn_anterior_3.clicked.connect(self.anterior_3)
        self.btn_anterior_4.clicked.connect(self.anterior_4)
        
        self.btn_siguiente_2.clicked.connect(self.siguiente_2)
        self.btn_siguiente_3.clicked.connect(self.siguiente_3)
        self.btn_siguiente_4.clicked.connect(self.siguiente_4)
        
        self.rot_m1.clicked.connect(self.rotar_m1)
        self.rot_m2.clicked.connect(self.rotar_m2)
        self.rot_m3.clicked.connect(self.rotar_m3)
    
    def histogram_1(self):
        if self.h_1.checkState():
            self.gra.ui.histogram.show()
            self.gra.ui.roiBtn.show()
            self.gra.ui.menuBtn.show()
        else: 
            self.gra.ui.histogram.hide()
            self.gra.ui.roiBtn.hide()
            self.gra.ui.menuBtn.hide()
        
    def histogram_2(self):
        if self.h_2.checkState():
            self.gra_2.ui.histogram.show()
            self.gra_2.ui.roiBtn.show()
            self.gra_2.ui.menuBtn.show()
        else: 
            self.gra_2.ui.histogram.hide()
            self.gra_2.ui.roiBtn.hide()
            self.gra_2.ui.menuBtn.hide()
        
    def histogram_3(self):
        if self.h_3.checkState():
            self.gra_3.ui.histogram.show()
            self.gra_3.ui.roiBtn.show()
            self.gra_3.ui.menuBtn.show()
        else: 
            self.gra_3.ui.histogram.hide()
            self.gra_3.ui.roiBtn.hide()
            self.gra_3.ui.menuBtn.hide()

    def slider_cambio(self,value):
        self.pos_1=value
        self.grafi()
    
    def slider_cambio_2(self,value):
        self.pos_2=value
        self.grafi()
    
    def slider_cambio_3(self,value):
        self.pos_3=value
        self.grafi()
    
    def rotar_m1(self):
        self.rot_1=self.rot_1+1
        if self.rot_1==4:
            self.rot_1=0                
        self.grafi()
    def rotar_m2(self):
        self.rot_2=self.rot_2+1
        if self.rot_2==4:
            self.rot_2=0                
        self.grafi()
    def rotar_m3(self):
        self.rot_3=self.rot_3+1
        if self.rot_3==4:
            self.rot_3=0              
        self.grafi()  
        
        
    def anterior_2(self):
        if self.pos_1!=0:
            self.pos_1=self.pos_1-1
            #self.gra.setImage(self.data[:,:,self.pos_1].T)
        self.grafi()
        self.verticalSlider.setValue(self.pos_1)
    
    def anterior_3(self):
        if self.pos_2!=0:
            self.pos_2=self.pos_2-1
            #self.gra_2.setImage(self.data[:,self.pos_2,:].T)
        self.grafi()
        self.verticalSlider_2.setValue(self.pos_2)
            
    def anterior_4(self):
        if self.pos_3!=0:
            self.pos_3=self.pos_3-1
            #self.gra_3.setImage(self.data[self.pos_3,:,:].T)
        self.grafi()
        self.verticalSlider_3.setValue(self.pos_3)
            
    def siguiente_2(self):
        a=np.shape(self.data)[2]
        if self.pos_1!=a:
            self.pos_1=self.pos_1+1
            #self.gra.setImage(self.data[:,:,self.pos_1].T)
        self.grafi()
        self.verticalSlider.setValue(self.pos_1)
            
    def siguiente_3(self):
        a=np.shape(self.data)[1]
        if self.pos_2!=a:
            self.pos_2=self.pos_2+1
            #self.gra_2.setImage(self.data[:,self.pos_2,:].T)
        self.grafi()
        self.verticalSlider_2.setValue(self.pos_2)
            
    def siguiente_4(self):
        a=np.shape(self.data)[0]
        if self.pos_3!=a:
            self.pos_3=self.pos_3+1
            #self.gra_3.setImage(self.data[self.pos_3,:,:].T)
        self.grafi()
        self.verticalSlider_3.setValue(self.pos_3)
    
    
    def asignarcontrolador(self, c): #asigna el controlador a la ventana 
        self.__mi_controlador=c
    
    
    def charge(self): #funcion para realizar la carga 
        if self.dcmarchivo==0: #genera un mensaje si aún no se selecciona archivo
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText('Message Error')
            msg.setWindowTitle('Message Box')
            msg.setInformativeText('Please, choose a DICOM file.')
            msg.show()
        else: #recibe la información del archivo DICOM y la muestra en la interfaz y gráfica el archivo
            file,name,sex,estudio,medico,serie,date_estudio,time_estudio,id_paciente,nacimiento,n,elemento=self.__mi_controlador.datos()
            self.file.setText(str(file))
            self.name.setText(str(name))
            self.sex.setText(str(sex))
            self.estudio.setText(str(estudio))
            self.medico.setText(str(medico))
            self.serie.setText(str(serie))
            self.date_estudio.setText(str(date_estudio))
            self.time_estudio.setText(str(time_estudio))
            self.id_paciente.setText(str(id_paciente))
            self.nacimiento.setText(str(nacimiento))
            self.dcmarchivo=0
            self.n=n #numero de archivos en la ruta
            self.elemento=elemento #archivo de la ruta 
            pixel_array,file=self.__mi_controlador.graph_una(self.elemento) #recibe la matriz de datos y el archivo 
            self.gra_4.setImage(pixel_array)#grafica el archivo
   
    def graph_anterior(self): #grafica el archivo anterior dentro de la ruta encontrada al presionar el boton 
        if self.elemento!=0: #limita los archivos 
            self.elemento=self.elemento-1
            pixel_array,file=self.__mi_controlador.graph_una(self.elemento) #recibe el archivo y los datos
            self.file.setText(str(file))#modifica el campo de archivo
            self.gra_4.setImage(pixel_array)#grafica la matriz de datos
    
    def graph_siguiente(self):#grafica el elemento siguiente similar a la funcion graph_anterior
        if self.elemento!=(self.n-1):
            self.elemento=self.elemento+1
            pixel_array,file=self.__mi_controlador.graph_una(self.elemento)            
            self.file.setText(str(file))
            self.gra_4.setImage(pixel_array)
            
        
    def examin(self):#limpia los campos y recibe el archivo segun lo escoja el usuario para pasarlos al controlador 
        self.limpiarcampos()
        self.gra_2.clear()
        self.gra.clear()
        self.gra_3.clear()
        archivo,_=QFileDialog.getOpenFileName(self, "Abrir","","Archivos DICOM (*.dcm)*")
        nothing=self.__mi_controlador.recibirruta(archivo)
        self.dcmarchivo=1
    
    def limpiarcampos(self): #limpiar los campos de la ventana 
        self.file.setText("")
        self.name.setText("")
        self.sex.setText("")
        self.estudio.setText("")
        self.medico.setText("")
        self.serie.setText("")
        self.date_estudio.setText("")
        self.time_estudio.setText("")
        self.id_paciente.setText("")
        self.nacimiento.setText("")
        self.gra.clear()
        self.gra_2.clear()
        self.gra_3.clear()
        self.gra_4.clear()
    
    def graph(self): #grafica los planos  y dependiendo de si esta abierto o no el histograma se usa
        #img_shape, img3d=self.__mi_controlador.graph()
        self.data=self.__mi_controlador.graph()
        if self.h_1.checkState():
            self.gra.ui.histogram.show()
            self.gra.ui.roiBtn.show()
            self.gra.ui.menuBtn.show()
        else: 
            self.gra.ui.histogram.hide()
            self.gra.ui.roiBtn.hide()
            self.gra.ui.menuBtn.hide()
        if self.h_2.checkState():
            self.gra_2.ui.histogram.show()
            self.gra_2.ui.roiBtn.show()
            self.gra_2.ui.menuBtn.show()
        else: 
            self.gra_2.ui.histogram.hide()
            self.gra_2.ui.roiBtn.hide()
            self.gra_2.ui.menuBtn.hide()
        if self.h_3.checkState():
            self.gra_3.ui.histogram.show()
            self.gra_3.ui.roiBtn.show()
            self.gra_3.ui.menuBtn.show()
        else: 
            self.gra_3.ui.histogram.hide()
            self.gra_3.ui.roiBtn.hide()
            self.gra_3.ui.menuBtn.hide()
        
        a=np.shape(self.data)[2]
        b=np.shape(self.data)[1]
        c=np.shape(self.data)[0]
        self.verticalSlider.setMaximum(a)
        self.verticalSlider_2.setMaximum(b)
        self.verticalSlider_3.setMaximum(c)
        #self.grafi()
        
        self.gra.setImage(self.data[:,:,self.pos_1].T)
        self.gra_2.setImage(self.data[:,self.pos_2,:].T)
        self.gra_3.setImage(self.data[self.pos_3,:,:].T)
        
        # self.gra.setImage(img3d[:,:, img_shape[2]//2].T)
        # self.gra_2.setImage(img3d[:, img_shape[1]//2, :].T)
        # self.gra_3.setImage(img3d[img_shape[0]//2, :, :].T)
        
    def grafi(self):
        data_1=self.__mi_controlador.graf(self.data[:,:,self.pos_1],self.rot_1)
        data_2=self.__mi_controlador.graf(self.data[:,self.pos_2,:],self.rot_2)
        data_3=self.__mi_controlador.graf(self.data[self.pos_3,:,:],self.rot_3)
        
        
        self.gra.setImage(data_1)
        self.gra_2.setImage(data_2)
        self.gra_3.setImage(data_3)
        
        
class ventanaTres(QMainWindow): #ventana para hacer convertir a DICOM
    def __init__(self):
        super(ventanaTres,self).__init__();
        loadUi('convert.ui',self)
        self.setup()
        
    def setup(self): #define las funciones iniciales 
        self.exam.clicked.connect(self.exa)
        self.conver.clicked.connect(self.conv)
        self.limpiarcampos()
        self.image=0;
        self.gra.clear()  
        self.gra.ui.histogram.hide() #quita la opción del histograma
        self.gra.ui.roiBtn.hide()#quita la opción del roi
        self.gra.ui.menuBtn.hide()#quita la opción del menu
        
    def asignarcontrolador(self, c):#asigna controlador
        self.__mi_controlador=c
    
    def exa(self):#buscar la imágen para agregar al DICOM
        archivo,_=QFileDialog.getOpenFileName(self, "Abrir imagen","","Archivos JPG(*.JPG)*;;Archivos JPEG (*.JPEG)*")
        img=self.__mi_controlador.recibirruta(archivo)
        self.gra.setImage(img[:,:,0].T)
        
        self.image=1
    
    def conv(self):#Convertir usando dcmtk
        if (self.file.text()=="" or self.name.text()=="" or self.sex.text()=="" or self.estudio.text()=="" or self.medico.text()=="" or self.serie.text()=="" or self.date_estudio.text()=="" or self.time_estudio.text()=="" or self.id_paciente.text()=="" or self.file.text()=="" or self.image==0):
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText('Message Error')
            msg.setWindowTitle('Message Box')
            msg.setInformativeText('Please, complete all fields including the image.')
            msg.show()
        else: # Captura de los datos escritos por el usuario y ubicación del archivo
            #archivo,_=QFileDialog.getSaveFileName(self, "Guardar archivo","","Archivos DICOM (*.dcm)*")
            archivo= QFileDialog.getExistingDirectory(self,"Seleccione un directorio",".",QFileDialog.ShowDirsOnly);
            file=self.file.text()
            name=self.name.text()
            sex=self.sex.text()
            estudio=self.estudio.text()
            medico=self.medico.text()
            serie=self.serie.text()
            date_estudio=self.date_estudio.text()
            time_estudio=self.time_estudio.text()
            id_paciente=self.id_paciente.text()
            nacimiento=self.nacimiento.text()
            self.__mi_controlador.conv(archivo,file,name,sex,estudio,medico,serie,date_estudio,time_estudio,id_paciente,nacimiento)
            self.image=0
            self.limpiarcampos()            
            
    def limpiarcampos(self): #limpiar los campos de la ventana 3
        self.file.setText("")
        self.name.setText("")
        self.sex.setText("")
        self.estudio.setText("")
        self.medico.setText("")
        self.serie.setText("")
        self.date_estudio.setText("")
        self.time_estudio.setText("")
        self.id_paciente.setText("")
        self.nacimiento.setText("")
        