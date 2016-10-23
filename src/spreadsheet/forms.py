from django import forms
from spreadsheet.models import SpreadSheetColumn, SpreadSheet2
from datetime import timedelta
from django.utils import timezone


class FileForm(forms.Form):
    csv_file = forms.FileField()

    def clean_csv_file(self):
        data = self.cleaned_data.get('csv_file')
        k = str(data.name)
        k = k.split('.')
        if k[1] != 'csv':
            raise forms.ValidationError("Please Upload a CSV file")
        return data


class NoOfColumnsForm(forms.Form):
    no_of_columns = forms.IntegerField(min_value=1)


class NoOfRowsForm(forms.Form):
    no_of_rows = forms.IntegerField(min_value=1)
    
    
class SpreadSheetForm(forms.ModelForm):
    class Meta:
        model = SpreadSheet2
        fields = ['name']
        

class ColumnForm(forms.ModelForm):
    class Meta:
        model = SpreadSheetColumn
        fields = ['name', 'sort_id']


class RowForm(forms.Form):

    @staticmethod
    def colToExcel(col):  # col is 1 based
        excelCol = str()
        div = col
        while div:
            (div, mod) = divmod(div-1, 26)  # will return (x, 0 .. 25)
            excelCol = chr(mod + 65) + excelCol
        return excelCol

    @staticmethod
    def get_field(label, disabled):
        return forms.CharField(max_length=1024, label=label, required=False, disabled=disabled)

    def __init__(self, *args, **kwargs):
        columns = kwargs.pop('columns', [])
        add = kwargs.pop('add', True)
        initial_data = kwargs.pop('initial_data', [])
        user = kwargs.pop('user', None)
        user_check_override = kwargs.pop('user_check_override', False)
        super(RowForm, self).__init__(*args, **kwargs)

        if add:
            for col_num, column in enumerate(columns, 1):
                self.fields['column_' + str(column.id)] = self.get_field(self.colToExcel(col_num), False)
        else:
            last_hour_date_time = timezone.now() - timedelta(hours=1)
            for col_num, data in enumerate(initial_data, 1):
                column, row = data
                if user.is_authenticated() and user.is_superuser and not user_check_override:
                    self.fields['column_' + str(column.id)] = self.get_field(self.colToExcel(col_num), False)
                else:
                    if row.update_time >= last_hour_date_time:
                        self.fields['column_' + str(column.id)] = self.get_field(self.colToExcel(col_num), False)
                    else:
                        self.fields['column_' + str(column.id)] = self.get_field(self.colToExcel(col_num), True)
