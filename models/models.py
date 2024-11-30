# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class project_task_custom(models.Model):
#     _name = 'project_task_custom.project_task_custom'
#     _description = 'project_task_custom.project_task_custom'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()

#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

from odoo import models, fields, api

class ProjectTask(models.Model):
    _inherit = 'project.task'

    is_field_service_project = fields.Boolean(
        string="Is Field Service Project",
        compute="_compute_is_field_service_project",
        store=True
    )

    @api.depends('project_id')
    @api.onchange('project_id')
    def _compute_is_field_service_project(self):
        for task in self:
            task.is_field_service_project = task.project_id.is_field_service if task.project_id else False
    
    def force_update_is_field_service_project(self):
        """
        Force update `is_field_service_project` for all tasks.
        This ensures the field is recalculated for existing tasks.
        """
        tasks = self.search([])
        for task in tasks:
            task.is_field_service_project = task.project_id.is_field_service

    
    # Computed phone number field
    assignee_phone = fields.Char(
        string="Assignee Phone",
        compute="_compute_assignee_phone",
        store=True,
        help="Phone number of the assigned user"
    )

    @api.depends('user_ids', 'project_id.is_field_service')
    def _compute_assignee_phone(self):
        """
        Compute the phone number of the assignee if the project is a Field Service project.
        """
        for task in self:
            if task.project_id.is_field_service and task.user_ids and task.user_ids.partner_id:
                task.assignee_phone = task.user_ids.partner_id.phone
            else:
                task.assignee_phone = False


    slot_sdate = fields.Date(
        string="Slot SDate",
        store=True,
        help="The start date of the selected slot"
    )
    slot_edate = fields.Datetime(
        string="Slot EDate",
        store=True,
        help="The end date of the selected slot"
    )

    slot_ids = fields.Many2many(
        'field.service.slot',
        string="Slots",
        help="Select one or more slots for this task."
    )
    estimated_slots = fields.Integer(
        string="Estimated Slots",
        help="Number of slots required for this task.",
        compute="_compute_estimated_slots",
        store=True
    )
    start_time = fields.Float(
        string="Start Time",
        compute="_compute_slot_times",
        store=True,
        help="The start time based on the selected slots."
    )
    end_time = fields.Float(
        string="End Time",
        compute="_compute_slot_times",
        store=True,
        help="The end time based on the selected slots."
    )
    slot_time_range = fields.Char(
        string="Slot Time Range",
        compute="_compute_slot_times",
        store=True,
        help="The computed time range for the selected slots."
    )

    @api.depends('allocated_hours')
    @api.onchange('allocated_hours')
    def _compute_estimated_slots(self):
        for task in self:
            if task.project_id.is_field_service:
                task.estimated_slots = round((task.allocated_hours or 0) / 2)  # Assuming each slot is 2 hours
            else:
                task.estimated_slots = 0
            # if task.slot_ids:
            #     sorted_slots = task.slot_ids.sorted(key=lambda s: s.start_time)
            #     task.start_time = sorted_slots[0].start_time
            #     task.end_time = sorted_slots[-1].end_time
            #     task.slot_time_range = f"{sorted_slots[0].start_time:02.0f}:00 - {sorted_slots[-1].end_time:02.0f}:00"
            # else:
            #     task.start_time = 0.0
            #     task.end_time = 0.0
            #     task.slot_time_range = "No slots selected"

    @api.depends('slot_ids')
    @api.onchange('slot_ids')
    def _compute_slot_times(self):
        for task in self:
            if task.project_id.is_field_service and task.slot_ids:
                sorted_slots = task.slot_ids.sorted(key=lambda s: s.start_time)
                task.start_time = sorted_slots[0].start_time
                task.end_time = sorted_slots[-1].end_time
                task.slot_time_range = f"{sorted_slots[0].start_time:02.0f}:00 - {sorted_slots[-1].end_time:02.0f}:00"
            else:
                task.start_time = 0.0
                task.end_time = 0.0
                task.slot_time_range = "No slots selected"

    
    @api.depends('slot_ids')
    @api.onchange('slot_ids')

    def _compute_allocated_hours(self):
        """
        Compute Allocated Hours based on the number of selected slots.
        Each slot is assumed to be 2 hours.
        """
        for task in self:
            # Calculate allocated hours as the number of slots multiplied by 2
            task.allocated_hours = len(task.slot_ids) * 2

    # @api.onchange('slot_ids')
    # def _onchange_slots(self):
    #     """Automatically update allocated hours based on slot selections."""
    #     self._compute_allocated_hours()
    #     self._compute_slot_times()


class ProjectProject(models.Model):
    _inherit = 'project.project'

    is_field_service = fields.Boolean(
        string="Field Service",
        help="Mark this project as a Field Service project."
    )


