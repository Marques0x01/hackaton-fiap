from flask import Flask, request, jsonify
from marshmallow import Schema, fields, ValidationError, validates_schema, validate
from src.services.agenda_service import AgendaService


class AgendaSchema(Schema):
    schedule_id = fields.Int(required=True)
    patient_document = fields.Str(
        required=True)


class AgendaUpdateSchema(Schema):
    appointment_id = fields.Int(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(
        ["PENDING", "ACCEPTED", "REFUSED"]))


class AgendaController():
    def __init__(self, agenda_service: AgendaService) -> None:
        self.__agenda_service = agenda_service

    def update_status_agenda(self):
        try:
            data = request.json
            register_schema = AgendaUpdateSchema()
            try:
                validated_data = register_schema.load(data)
            except ValidationError as err:
                return jsonify({
                    "status_code": 400,
                    "message": "Validation error",
                    "errors": err.messages
                }), 400

            response = self.__agenda_service.update_status_agenda(
                validated_data["appointment_id"], validated_data["status"])

            return jsonify({
                "status_code": 200,
                "message": "Appointment updated",
                "data": response
            }), 200
        except Exception as e:
            return jsonify({
                "status_code": 500,
                "message": "Error on updating appointment",
                "errors": e
            }), 500

    def create_agenda(self):
        try:
            data = request.json
            register_schema = AgendaSchema()
            try:
                validated_data = register_schema.load(data)
            except ValidationError as err:
                return jsonify({
                    "status_code": 400,
                    "message": "Validation error",
                    "errors": err.messages
                }), 400

            response = self.__agenda_service.save_agenda(
                validated_data["schedule_id"], validated_data["patient_document"])

            return jsonify({
                "status_code": 200,
                "message": "Appointment created",
                "data": response
            }), 200
        except Exception as e:
            return jsonify({
                "status_code": 500,
                "message": "Error on creating appointment",
                "errors": e
            }), 500
