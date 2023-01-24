# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LibreriaLibro(models.Model):
    _name = 'libreria.libro'
    _description = 'libreria.libro'
    name = fields.Char('Título', required=True, help="Introduce el título del libro")
    precio = fields.Float('Precio')
    ejemplares = fields.Integer('Ejemplares')
    fecha = fields.Date("Fecha de compra")
    segmano = fields.Boolean("Segunda mano")
    estado = fields.Selection([('0','Bueno'),('1','Regular'),('2','Malo')],string="Estado",default="0")
    categoria_id = fields.Many2one('libreria.categoria', string='Categoría')

class LibreriaCategoria(models.Model):
    _name = 'libreria.categoria'
    _description = 'libreria.categoria'
    name = fields.Char('Nombre', required=True, help="Introduce el nombre de la categoría")
    description = fields.Text('Decripción')
    libros_ids = fields.One2many('libreria.libro', 'categoria_id', string='Libros')
