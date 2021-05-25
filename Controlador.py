# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 15:39:57 2020

@author: Carlos Jose Munoz
"""

from Vista import ventanaUno,ventanaDos,ventanaTres
from Modelo import dicom
import sys

from PyQt5.QtWidgets import QApplication 

class Controlador(object): #objeto que va a recibir los comandos de la interfaz para enviarselos al modelo y desarrollar la accion necesaria 
    def __init__(self, vista,vista2,modelo,vista3): #genera las ventanas 
        self._mi_vista=vista #atributo para la apertura de la primera ventana 
        self._mi_2vista=vista2
        self._mi_3vista=vista3
        self._mi_modelo=modelo
    
    def ventana(self, r):#abre la ventana siguiente dependiendo de las ventanas encontradas 
        if (r==1):
            self._mi_2vista.show()
            self._mi_2vista.limpiarcampos()
            app.exec_()
        if (r==2):
            self._mi_3vista.show()
            self._mi_3vista.limpiarcampos()
            app.exec_()
        self._mi_modelo.ventana(r)
            
    def recibirruta(self, archivo): #recibe la ruta de la interfaz
        return self._mi_modelo.recibirruta(archivo)
        
    def conv(self,archivo,file,name,sex,estudio,medico,serie,date_estudio,time_estudio,id_paciente,nacimiento): #recibe los datos para convertir a dicom 
        self._mi_modelo.conv(archivo,file,name,sex,estudio,medico,serie,date_estudio,time_estudio,id_paciente,nacimiento)
        
    def datos(self): #devuelve los datos para mostrar en la interfaz
        file, name, sex, estudio, medico, serie, date_estudio, time_estudio, id_paciente, nacimiento,n,elemento=self._mi_modelo.datos()
        return file, name, sex, estudio, medico, serie, date_estudio, time_estudio, id_paciente, nacimiento,n,elemento
    
    def graph(self):#grafica los ejes
        
        data=self._mi_modelo.graph()
        return data
    
    def graph_una(self, elemento):#grafica el archivo
        pixel_array,imgdcm=self._mi_modelo.graph_una(elemento)
        return pixel_array,imgdcm
    
    def graf(self, data, rot):
        return self._mi_modelo.graf(data, rot)
    
if __name__ == '__main__': #inicio del programa, es el programa principal que se corre 
    app=QApplication(sys.argv)
    mi_vista=ventanaUno();
    mi_2vista=ventanaDos();
    mi_3vista=ventanaTres();
    mi_modelo=dicom();
    mi_controlador= Controlador(mi_vista, mi_2vista, mi_modelo, mi_3vista)
    mi_3vista.asignarcontrolador(mi_controlador)
    mi_2vista.asignarcontrolador(mi_controlador)    
    mi_vista.asignarcontrolador(mi_controlador)
    mi_vista.show()
            
    sys.exit(app.exec_())