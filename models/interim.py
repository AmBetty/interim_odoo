# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo import models, fields, _, api
from datetime import date, datetime, timedelta

class Interim(models.Model):
    _inherit = 'res.partner'

    num_id_card = fields.Char(string = "Numéro carte d'identité")
    date_of_issu = fields.Date(string="Date de délivrance")
    start_time = fields.Date(string = "Ouvert :")
    end_time = fields.Date(string = "Jusqu'à :")
    society_type = fields.Many2one('society.type', string="Type de société")
    closing_time = fields.Date(string = "Heure de fermeture")
    beginning_hour = fields.Float('De :')
    ending_hour = fields.Float('A :')
    card_id_type = fields.Many2one('card_id.type', string = "Type de pièce d'identité")
    place_of_issu = fields.Char(string = "Lieu de délivrance")
    num_of_register = fields.Char(string="Numéro de régistre")
    country_of_residence = fields.Char(string="Pays de résidence")
    interimaire = fields.Boolean(string = "Est un intérimaire", readonly = True)
    stagiare = fields.Boolean(string = "Est un stagiaire", readonly = True)
    document_associated = fields.One2many('document.interim','res_partner_id')
    child_id = fields.One2many('res.partner','responsible_id', string = "Responsable")
    responsible_id = fields.Many2one('res.partner', string = "Responsable")
    fichier = fields.Many2many('ir.attachment', string = 'essai')
    fname = fields.Char(string ='datas fname')

    @api.model
    def create(self, values):
        res_partner = super(Interim, self).create(values)
        if res_partner.stagiare == True:
#            raise UserError(_('test 1'))
            all_directory_stagiaire = self.env['directory.interim'].search([('is_stagiaire', '=', True), ('obligatoire', '=', True)])
            if all_directory_stagiaire:

                for dir in all_directory_stagiaire:
                    self.env['document.interim'].create({
                        'directory_id' : dir.repository_id.id,
                        'res_partner_id' : res_partner.id,
                    })

        if res_partner.interimaire == True:
#            raise UserError(_('test 2'))
            all_directory_stagiaire = self.env['directory.interim'].search([('is_interim', '=', True), ('obligatoire', '=', True)])
            if all_directory_stagiaire:

                for dir in all_directory_stagiaire:
                    self.env['document.interim'].create({
                        'directory_id' : dir.repository_id.id,
                        'res_partner_id' : res_partner.id,
                    })
        if values.get('responsible_id'):
            res_partner.responsible_id = values.get('responsible_id')

        return res_partner

class Responsable(models.Model):
    _name = 'res.res'

    responsible_id = fields.Many2one('res.partner', string = "Responsable")

class Card_id_type(models.Model):
    _name = 'card_id.type'
    _rec_name = 'name'

    name = fields.Char(string = "Type de pièce d'identité")

class Society_type(models.Model):
    _name = 'society.type'
    _rec_name = 'name'

    name = fields.Char(string = "Type de société")

class Repertoire(models.Model):
    _name = 'directory.interim'
    _rec_name = "repository_id"

    obligatoire = fields.Boolean(string = "Obligatoire")
    is_interim = fields.Boolean(string = "Pour interim")
    is_stagiaire = fields.Boolean(string = "Pour stagiaire")
    repository_id = fields.Many2one('directory.directory', string = "Répértoire")
    document_associated_id = fields.One2many('document.interim', 'directory_id', string='Documents')

class Document_interim(models.Model):
    _name = 'document.interim'
    _rec_name = "directory_id"

    ir_attachement = fields.Many2one('ir.attachment',string = "Fichier")
    directory_id = fields.Many2one('directory.directory', string = "Document")
    res_partner_id = fields.Many2one('res.partner', string = "Tiers")
