from odoo import models
import base64
import io

class PatientAppointmentXlsx(models.AbstractModel):
    _name = 'report.om_hospital.report_patient_id_card_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):
        # Many sheet make korar jonno sheet variable ti for loop ar modde dity hby and name dity hby obj.name
        sheet = workbook.add_worksheet('patient_id_card')
        bold = workbook.add_format({'bold': True})
        formet_1 = workbook.add_format({'bold':True, 'align':'center', 'bg_color':'yellow'})

        row = 3
        col = 3
        # column D ar width set kore dawa 50
        sheet.set_column('D:D',50)
        for obj in patients:
            row += 1
            # For Merge two column
            sheet.merge_range(row,col,row,col+1, "ID Card", formet_1)
            # For adding Image
            row+=1
            if obj.image:
                patient_image = io.BytesIO(base64.b64encode(obj.image))
                # insert image used for insert the image into the sheet
                sheet.insert_image(row,col,"image.png",{"image.png":patient_image,'x_scale': 0.5,'y_scale': 0.5})


            row += 1
            # .writ  for write the values
            sheet.write(row, col,'Name:',)
            sheet.write(row, col+1, obj.name, bold)
            row += 1
            sheet.write(row, col, 'Age:',)
            sheet.write(row, col+1, obj.age, bold)
            row += 1
            sheet.write(row, col, 'Reference', )
            sheet.write(row, col+1, obj.ref, bold)

            row+=2

    # def generate_xlsx_report(self, workbook, data, patients):
    #     for obj in patients:
    #         report_name = obj.name
    #         # One sheet by partner
    #         sheet = workbook.add_worksheet(report_name[:31])
    #         bold = workbook.add_format({'bold': True})
    #         sheet.write(0, 0, obj.name, bold)
