from rest_framework import serializers
from ResourceManagement.models import Deposito, Vehiculo, Demanda, PuntoDeEntrega
import re
class DepositoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposito
        fields = ['id', 'nombre', 'latitud', 'longitud', 'direccion', 'numero_de_telefono']

    def to_internal_value(self, data):
        errors = {}
        
        latitud = data.get('latitud')
        longitud = data.get('longitud')

        # Validar latitud
        if latitud:
            try:
                float_latitud = float(latitud)
                if not (-90 <= float_latitud <= 90):
                    errors['latitud'] = ["La latitud debe estar entre -90 y 90 grados."]
                if not re.match(r'^-?\d{1,2}\.\d{6}$', latitud):
                    errors['latitud'] = ["La latitud debe tener exactamente 6 decimales."]
                if len(latitud) != 10:
                    errors['latitud'] = ["La latitud debe tener exactamente 10 caracteres incluyendo el punto y el signo."]
            except ValueError:
                errors['latitud'] = ["La latitud debe ser un número válido."]
        
        # Validar longitud
        if longitud:
            try:
                float_longitud = float(longitud)
                if not (-180 <= float_longitud <= 180):
                    errors['longitud'] = ["La longitud debe estar entre -180 y 180 grados."]
                if not re.match(r'^-?\d{1,3}\.\d{6}$', longitud):
                    errors['longitud'] = ["La longitud debe tener exactamente 6 decimales."]
                if len(longitud) != 10:
                    errors['longitud'] = ["La longitud debe tener exactamente 10 caracteres incluyendo el punto y el signo."]
            except ValueError:
                errors['longitud'] = ["La longitud debe ser un número válido."]

        if errors:
            raise serializers.ValidationError(errors)

        return super().to_internal_value(data)

class VehiculoSerializer(serializers.ModelSerializer):
    deposito = serializers.PrimaryKeyRelatedField(queryset=Deposito.objects.all())
    
    class Meta:
        model = Vehiculo
        fields = ['matricula', 'capacidad_de_carga', 'deposito', 'estado']
        depth = 1  

class DemandaSerializer(serializers.ModelSerializer):
    deposito = serializers.PrimaryKeyRelatedField(queryset=Deposito.objects.all())
    # deposito = DepositoSerializer()
    class Meta:
        model = Demanda 
        fields = ['id', 'peso_kg', 'fecha_creada', 'descripción', 'estado', 'deposito']
        depth = 1  

    def create(self, validated_data):
        # Ignorar el campo 'estado' si está presente en los datos validados
        validated_data.pop('estado', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Permitir la actualización del campo 'estado'
        return super().update(instance, validated_data)

class PuntoDeEntregaSerializer(serializers.ModelSerializer):
    demanda = serializers.PrimaryKeyRelatedField(queryset=Demanda.objects.all())
    class Meta:
        model = PuntoDeEntrega
        fields = ['id', 'cliente', 'latitud', 'longitud', 'demanda', 'estado', "numero_de_telefono"]
        depth = 1

    def to_internal_value(self, data):
        errors = {}
        
        latitud = data.get('latitud')
        longitud = data.get('longitud')

        # Validar latitud
        if latitud:
            try:
                float_latitud = float(latitud)
                if not (-90 <= float_latitud <= 90):
                    errors['latitud'] = ["La latitud debe estar entre -90 y 90 grados."]
                if not re.match(r'^-?\d{1,2}\.\d{6}$', latitud):
                    errors['latitud'] = ["La latitud debe tener exactamente 6 decimales."]
                if len(latitud) != 10:
                    errors['latitud'] = ["La latitud debe tener exactamente 10 caracteres incluyendo el punto y el signo."]
            except ValueError:
                errors['latitud'] = ["La latitud debe ser un número válido."]
        
        # Validar longitud
        if longitud:
            try:
                float_longitud = float(longitud)
                if not (-180 <= float_longitud <= 180):
                    errors['longitud'] = ["La longitud debe estar entre -180 y 180 grados."]
                if not re.match(r'^-?\d{1,3}\.\d{6}$', longitud):
                    errors['longitud'] = ["La longitud debe tener exactamente 6 decimales."]
                if len(longitud) != 10:
                    errors['longitud'] = ["La longitud debe tener exactamente 10 caracteres incluyendo el punto y el signo."]
            except ValueError:
                errors['longitud'] = ["La longitud debe ser un número válido."]

        if errors:
            raise serializers.ValidationError(errors)

        return super().to_internal_value(data)