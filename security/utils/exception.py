from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Chama o handler padrão para obter a resposta
    response = exception_handler(exc, context)

    # Agora personalizamos a resposta
    if response is not None:
        customized_response = {
            'status_code': response.status_code,
        }

        # Se existir detalhes de erro, nós os pegamos e os ajustamos
        if 'detail' in response.data:
            customized_response['error'] = response.data['detail']
        elif 'non_field_errors' in response.data:
            # Para erros não associados a um campo específico
            customized_response['error'] = response.data['non_field_errors'][0]
        else:
            # Por padrão, pegamos a primeira chave do erro
            first_error_key = list(response.data.keys())[0]
            customized_response['error'] = response.data[first_error_key][0]

        response.data = customized_response

    return response
