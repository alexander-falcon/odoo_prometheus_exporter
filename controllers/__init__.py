# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request, Response
import time

class PrometheusMetricsController(http.Controller):

    @http.route('/metrics', type='http', auth='public', methods=['GET'], csrf=False)
    def metrics(self, **kwargs):
        # Ejemplo de métricas básicas
        metrics = []

        # Tiempo actual
        metrics.append(f'# HELP odoo_up Odoo service availability')
        metrics.append(f'# TYPE odoo_up gauge')
        metrics.append(f'odoo_up 1')

        # Número de usuarios activos
        user_count = request.env['res.users'].sudo().search_count([])
        metrics.append(f'# HELP odoo_users_total Total de usuarios en Odoo')
        metrics.append(f'# TYPE odoo_users_total gauge')
        metrics.append(f'odoo_users_total {user_count}')

        # Número de módulos instalados
        module_count = request.env['ir.module.module'].sudo().search_count([('state','=','installed')])
        metrics.append(f'# HELP odoo_modules_installed Número de módulos instalados')
        metrics.append(f'# TYPE odoo_modules_installed gauge')
        metrics.append(f'odoo_modules_installed {module_count}')

        # Tiempo de respuesta simulado
        metrics.append(f'# HELP odoo_response_time_seconds Tiempo de respuesta del endpoint')
        metrics.append(f'# TYPE odoo_response_time_seconds gauge')
        metrics.append(f'odoo_response_time_seconds {time.process_time()}')

        # Construir respuesta
        body = "\n".join(metrics)
        return Response(body, content_type='text/plain; charset=UTF-8')
