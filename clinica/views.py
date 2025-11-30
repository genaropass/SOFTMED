from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from funciones.db import (
    agregar_paciente as db_agregar_paciente, 
    listar_pacientes as db_listar_pacientes, 
    buscar_pacientes, 
    crear_base_de_datos, 
    calcular_edad,
    obtener_paciente_por_id,
    obtener_historial_clinico,
    agregar_historial_clinico,
    eliminar_paciente
)
import sqlite3
from datetime import datetime

# Asegurar que la base de datos existe
crear_base_de_datos()

# Decorador simple para verificar autenticación de médico
def requiere_medico(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('medico_autenticado'):
            messages.warning(request, 'Debe iniciar sesión como médico para acceder a esta sección.')
            return redirect('login_medico')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper

def inicio(request):
    mensaje = None
    tipo_mensaje = None
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        fecha_nacimiento = request.POST.get('fecha_nacimiento', '').strip()
        genero = request.POST.get('genero', '').strip()
        servicio_medico = request.POST.get('servicio_medico', '').strip()
        obra_social = request.POST.get('obra_social', '').strip()
        
        if nombre and fecha_nacimiento and genero:
            try:
                conn = sqlite3.connect('historial_clinico.db')
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO pacientes (nombre, fecha_nacimiento, genero, servicio_medico, obra_social) 
                    VALUES (?,?,?,?,?)
                """, (nombre, fecha_nacimiento, genero, servicio_medico or None, obra_social or None))
                paciente_id = cursor.lastrowid
                edad = calcular_edad(fecha_nacimiento)
                conn.commit()
                conn.close()
                
                mensaje = f"Paciente agregado con éxito. ID: {paciente_id}, Nombre: {nombre}, Edad: {edad} años"
                tipo_mensaje = 'success'
            except sqlite3.IntegrityError:
                mensaje = "Error: Ya existe un paciente con ese nombre."
                tipo_mensaje = 'error'
            except Exception as e:
                mensaje = f"Error al agregar paciente: {str(e)}"
                tipo_mensaje = 'error'
        else:
            mensaje = "Por favor, complete todos los campos obligatorios."
            tipo_mensaje = 'error'
    
    return render(request, 'clinica/inicio.html', {
        'mensaje': mensaje,
        'tipo_mensaje': tipo_mensaje
    })

def servicios(request):
    return render(request, 'clinica/servicios.html')

def login_medico(request):
    """
    Página de login para médicos
    """
    if request.method == 'POST':
        password = request.POST.get('password', '').strip()
        # Contraseña simple para el médico (en producción usar Django auth)
        if password == 'medico123':  # Cambiar por una contraseña segura
            request.session['medico_autenticado'] = True
            messages.success(request, 'Sesión iniciada correctamente.')
            return redirect('registro_pacientes')
        else:
            messages.error(request, 'Contraseña incorrecta.')
    
    return render(request, 'clinica/login_medico.html')

def logout_medico(request):
    """
    Cerrar sesión del médico
    """
    request.session.pop('medico_autenticado', None)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('inicio')

@requiere_medico
def registro_pacientes(request):
    pacientes = db_listar_pacientes()
    termino_busqueda = request.GET.get('buscar', '').strip()
    pacientes_filtrados = pacientes
    
    if termino_busqueda:
        pacientes_filtrados = buscar_pacientes(termino_busqueda)
    
    return render(request, 'clinica/registro_pacientes.html', {
        'pacientes': pacientes_filtrados,
        'termino_busqueda': termino_busqueda,
        'total_pacientes': len(pacientes),
        'resultados_encontrados': len(pacientes_filtrados),
        'medico_autenticado': True
    })

def contacto(request):
    return render(request, 'clinica/contacto.html')

@requiere_medico
def agregar_paciente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        fecha_nacimiento = request.POST.get('fecha_nacimiento', '').strip()
        genero = request.POST.get('genero', '').strip()
        servicio_medico = request.POST.get('servicio_medico', '').strip()
        obra_social = request.POST.get('obra_social', '').strip()
        
        if nombre and fecha_nacimiento and genero:
            try:
                conn = sqlite3.connect('historial_clinico.db')
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO pacientes (nombre, fecha_nacimiento, genero, servicio_medico, obra_social) 
                    VALUES (?,?,?,?,?)
                """, (nombre, fecha_nacimiento, genero, servicio_medico or None, obra_social or None))
                paciente_id = cursor.lastrowid
                conn.commit()
                conn.close()
                
                messages.success(request, f'Paciente agregado con éxito. ID: {paciente_id}')
                return redirect('registro_pacientes')
            except sqlite3.IntegrityError:
                messages.error(request, 'Ya existe un paciente con ese nombre.')
            except Exception as e:
                messages.error(request, f'Error al agregar paciente: {str(e)}')
        else:
            messages.error(request, 'Por favor, complete todos los campos obligatorios.')
    
    return redirect('registro_pacientes')

@requiere_medico
def ver_paciente(request, paciente_id):
    """
    Vista para ver los detalles de un paciente y su historial clínico
    """
    paciente = obtener_paciente_por_id(paciente_id)
    if not paciente:
        messages.error(request, 'Paciente no encontrado.')
        return redirect('registro_pacientes')
    
    historial = obtener_historial_clinico(paciente_id)
    today = datetime.now().date()
    
    return render(request, 'clinica/ver_paciente.html', {
        'paciente': paciente,
        'historial': historial,
        'today': today
    })

@requiere_medico
def agregar_historial(request, paciente_id):
    """
    Agregar una entrada al historial clínico de un paciente
    """
    if request.method == 'POST':
        fecha = request.POST.get('fecha', '').strip()
        notas = request.POST.get('notas', '').strip()
        diagnostico = request.POST.get('diagnostico', '').strip()
        tratamiento = request.POST.get('tratamiento', '').strip()
        observaciones = request.POST.get('observaciones', '').strip()
        
        if fecha and notas:
            try:
                agregar_historial_clinico(
                    paciente_id, 
                    fecha, 
                    notas, 
                    diagnostico or None, 
                    tratamiento or None, 
                    observaciones or None
                )
                messages.success(request, 'Historial clínico agregado correctamente.')
            except Exception as e:
                messages.error(request, f'Error al agregar historial: {str(e)}')
        else:
            messages.error(request, 'Fecha y notas son obligatorios.')
    
    return redirect('ver_paciente', paciente_id=paciente_id)

@requiere_medico
def eliminar_paciente_view(request, paciente_id):
    """
    Elimina un paciente y todo su historial clínico
    """
    if request.method == 'POST':
        try:
            paciente = obtener_paciente_por_id(paciente_id)
            if paciente:
                nombre_paciente = paciente[1]
                if eliminar_paciente(paciente_id):
                    messages.success(request, f'Paciente "{nombre_paciente}" eliminado correctamente junto con su historial clínico.')
                else:
                    messages.error(request, 'Error al eliminar el paciente.')
            else:
                messages.error(request, 'Paciente no encontrado.')
        except Exception as e:
            messages.error(request, f'Error al eliminar paciente: {str(e)}')
    
    return redirect('registro_pacientes')

def listar_pacientes(request):
    pacientes = db_listar_pacientes()
    return render(request, 'clinica/listar_pacientes.html', {
        'pacientes': pacientes
    })

