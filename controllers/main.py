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

        # Correos no enviados
        failed_mails = request.env['mail.mail'].sudo().search_count([('state', 'in', ['exception','failed'])])
        metrics.append('# HELP odoo_mail_failed_total Total de correos que no pudieron enviarse')
        metrics.append('# TYPE odoo_mail_failed_total gauge')
        metrics.append(f'odoo_mail_failed_total {failed_mails}')

        # Errores y warnings en logs
        errors = request.env['ir.logging'].sudo().search_count([('level','=','ERROR')])
        warnings = request.env['ir.logging'].sudo().search_count([('level','=','WARNING')])
        metrics.append('# HELP odoo_log_errors_total Número de errores en logs')
        metrics.append('# TYPE odoo_log_errors_total gauge')
        metrics.append(f'odoo_log_errors_total {errors}')
        metrics.append('# HELP odoo_log_warnings_total Número de warnings en logs')
        metrics.append('# TYPE odoo_log_warnings_total gauge')
        metrics.append(f'odoo_log_warnings_total {warnings}')

        # Nuevos candidatos
        applicants = request.env['hr.applicant'].sudo().search_count([])
        metrics.append('# HELP odoo_applicants_total Total de candidatos registrados')
        metrics.append('# TYPE odoo_applicants_total gauge')
        metrics.append(f'odoo_applicants_total {applicants}')

        # Construir respuesta
        body = "\n".join(metrics)
        return Response(body, content_type='text/plain; charset=UTF-8')
