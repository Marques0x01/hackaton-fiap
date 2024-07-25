from flask import request, jsonify
from marshmallow import Schema, fields, ValidationError, validate
from src.services.medico_service import MedicoService
from src.exception.CustomException import EntityNotFoundException, AlreadExistsException

# Schemas de Validação com Marshmallow
class DoctorSchema(Schema):
    doctor = fields.Dict(required=True)
    address = fields.Dict(required=True)

class HorarioSchema(Schema):
    data = fields.Str(required=False)
    hora_inicio = fields.Str(required=True)
    hora_fim = fields.Str(required=True)

class MedicoController:

    def __init__(self, service: MedicoService) -> None:
        self.__service = service

    def _handle_exception(self, e, message, status_code):
        """Método para tratar exceções e retornar respostas padronizadas."""
        return jsonify({
            "status_code": status_code,
            "message": message,
            "errors": str(e)
        }), status_code

    def get_all_doctors(self):
        try:
            doctors = self.__service.list_all_doctors()
            return jsonify({
                "status_code": 200,
                "message": "Doctors retrieved successfully",
                "data": doctors
            }), 200
        except Exception as e:
            return self._handle_exception(e, "Error retrieving doctors", 500)

    def get_doctors_por_especialidade_e_estado(self):
        try:
            especialidade = request.args.get('especialidade')
            estado = request.args.get('estado')
            medicos = self.__service.list_doctors_by_speciality_and_state(especialidade, estado)
            return jsonify({
                "status_code": 200,
                "message": "Doctors retrieved successfully",
                "data": medicos
            }), 200
        except EntityNotFoundException as e:
            return self._handle_exception(e, "not found", 404)
        except Exception as e:
            return self._handle_exception(e, "Error retrieving doctors by specialty and state", 500)

    def post_doctor(self):
        try:
            data = request.get_json()
            validated_data = DoctorSchema().load(data)
            response = self.__service.create_doctor(validated_data)
            return jsonify({
                "status_code": 201,
                "message": "Doctor created successfully",
                "data": response
            }), 201
        except (ValidationError, AlreadExistsException) as err:
            return self._handle_exception(err, "Validation error", 400)
        except Exception as e:
            return self._handle_exception(e, "Error creating doctor", 500)

    def get_horarios_disponiveis(self, crm: str):
        try:
            horarios = self.__service.listar_horarios_por_medico(crm)
            if not horarios:
                raise EntityNotFoundException(f'Nenhum horário disponível para o médico com CRM {crm}')
            return jsonify({
                "status_code": 200,
                "message": "Available schedules retrieved successfully",
                "data": horarios
            }), 200
        except EntityNotFoundException as e:
            return self._handle_exception(e, str(e), 404)
        except Exception as e:
            return self._handle_exception(e, "Error retrieving available schedules", 500)

    def post_horario_disponivel(self, crm: str):
        try:
            data = request.get_json()
            validated_data = HorarioSchema().load(data)
            response = self.__service.criar_horario_disponivel(validated_data, crm)
            return jsonify({
                "status_code": 201,
                "message": "Available schedule created successfully",
                "data": response
            }), 201
        except ValidationError as err:
            return self._handle_exception(err, "Validation error", 400)
        except EntityNotFoundException as e:
            return self._handle_exception(e, 'not found', 404)
        except Exception as e:
            return self._handle_exception(e, "Error creating available schedule", 500)

    def patch_horario_disponivel(self, crm: str, horario_id: int):
        try:
            data = request.get_json()
            validated_data = HorarioSchema().load(data)
            response = self.__service.atualizar_horario_disponivel(validated_data, crm, horario_id)
            if 'message' in response and 'não encontrado' in response['message']:
                raise EntityNotFoundException(response['message'])
            return jsonify({
                "status_code": 200,
                "message": "Available schedule updated successfully",
                "data": response
            }), 200
        except ValidationError as err:
            return self._handle_exception(err, "Validation error", 400)
        except EntityNotFoundException as e:
            return self._handle_exception(e, 'not found', 404)
        except Exception as e:
            return self._handle_exception(e, "Error updating available schedule", 500)
