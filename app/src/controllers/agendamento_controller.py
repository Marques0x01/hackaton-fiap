from flask import request, jsonify
from marshmallow import Schema, fields, ValidationError, validate
from src.services.agendamento_service import AgendamentoService
from src.exception.CustomException import EntityNotFoundException

class AgendaSchema(Schema):
    schedule_id = fields.Int(required=True)
    patient_document = fields.Str(required=True)

class AgendaUpdateSchema(Schema):
    appointment_id = fields.Int(required=True)
    status = fields.Str(
        required=True, 
        validate=validate.OneOf(["PENDING", "ACCEPTED", "REFUSED"])
    )

class AgendamentoController:
    def __init__(self, agenda_service: AgendamentoService) -> None:
        self.__agenda_service = agenda_service

    def _handle_exception(self, e, message, status_code):
        return jsonify({
            "status_code": status_code,
            "message": message,
            "errors": str(e)
        }), status_code

    def update_status_agenda(self):
        try:
            data = request.json
            validated_data = AgendaUpdateSchema().load(data)
            response = self.__agenda_service.update_status_agenda(
                validated_data["appointment_id"], validated_data["status"]
            )
            return jsonify({
                "status_code": 200,
                "message": "Appointment updated",
                "data": response
            }), 200
        except ValidationError as err:
            return self._handle_exception(err, "Validation error", 400)
        except EntityNotFoundException as e:
            return self._handle_exception(e, "Appointment not found", 404)
        except Exception as e:
            return self._handle_exception(e, "Error on updating appointment", 500)

    def create_agenda(self):
        try:
            data = request.json
            validated_data = AgendaSchema().load(data)
            response = self.__agenda_service.save_agenda(
                validated_data["schedule_id"], validated_data["patient_document"]
            )
            return jsonify({
                "status_code": 200,
                "message": "Appointment created",
                "data": response
            }), 200
        except ValidationError as err:
            return self._handle_exception(err, "Validation error", 400)
        except EntityNotFoundException as e:
            return self._handle_exception(e, "Entity not found", 404)
        except Exception as e:
            return self._handle_exception(e, "Error on creating appointment", 500)
