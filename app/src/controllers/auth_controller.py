from flask import Flask, request, jsonify
from services.cognito_service import CognitoService
from services.medico_service import MedicoService
from services.paciente_service import PacienteService
from marshmallow import Schema, fields, ValidationError, validates_schema, validate


class LoginSchema(Schema):
    documento = fields.Str(required=True)
    password = fields.Str(required=True)
    tipo_usuario = fields.Str(
        required=True, validate=validate.OneOf(["DOCTOR", "PATIENT"]))


class AddressSchema(Schema):
    cep = fields.Str(required=True)
    numero = fields.Int(required=True)
    estado = fields.Str(required=True)
    municipio = fields.Str(required=True)
    bairro = fields.Str(required=True)
    rua = fields.Str(required=True)

class RegisterSchema(Schema):
    documento = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    tipo_usario = fields.Str(
        required=True, validate=validate.OneOf(["DOCTOR", "PATIENT"]))
    nome = fields.Str(required=True)
    data_nascimento = fields.Str(required=False)
    telefone = fields.Str(required=False)
    documento = fields.Str(required=True)
    cnpj = fields.Str(required=False)
    especialidade = fields.Str(required=False)
    endereco = fields.Nested(AddressSchema, required=True)


class AuthController():

    def __init__(self, cognito_service: CognitoService, medico_service: MedicoService, paciente_service: PacienteService) -> None:
        self.__cognito_service = cognito_service
        self.__medico_service = medico_service
        self.__paciente_service = paciente_service

    def register(self):
        try:
            data = request.json
            register_schema = RegisterSchema()
            try:
                validated_data = register_schema.load(data)
            except ValidationError as err:
                return jsonify({
                    "status_code": 400,
                    "message": "Validation error",
                    "errors": err.messages
                }), 400

            self.__cognito_service.register_user(
                validated_data['documento'], validated_data['email'], validated_data['password'], validated_data['tipo_usario'])

            response = None
            if validated_data['tipo_usario'] == "DOCTOR":
                response = self.__medico_service.cadastrar_medico(validated_data)

            if validated_data['tipo_usario'] == "PATIENT":
                response = self.__paciente_service.cadastrar_paciente(validated_data)

            return jsonify({
                'status_code': 201,
                'message': 'User created successfully',
                'data': response
            }), 200
        except Exception as e:
            return jsonify({
                "status_code": 500,
                "message": "Error on registering",
                "errors": e
            }), 500

    def login(self):
        try:
            data = request.json
            register_schema = LoginSchema()
            try:
                validated_data = register_schema.load(data)
            except ValidationError as err:
                return jsonify({
                    "status_code": 400,
                    "message": "Validation error",
                    "errors": err.messages
                }), 400

            response = self.__cognito_service.login(
                validated_data['documento'], validated_data['password'], validated_data['tipo_usuario'])

            return jsonify(response), 200
        except Exception as e:
            return jsonify({
                "status_code": 500,
                "message": "Error on login",
                "errors": e
            }), 500
